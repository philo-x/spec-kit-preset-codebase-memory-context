"""Prompt contracts and real Spec Kit installation tests.

These tests do not execute an LLM command or prove generator filesystem safety.
"""
import hashlib
import json
import os
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
import zipfile
from importlib.metadata import version
from pathlib import Path

import pytest
import specify_cli
from packaging.version import Version
from typer.testing import CliRunner
from specify_cli import app
from specify_cli.presets import PresetManager, PresetManifest, PresetResolver

PRESET_DIR = Path(__file__).resolve().parent.parent
UPSTREAM = PRESET_DIR / "tests/fixtures/upstream/spec-kit-v1.1.2"
CORE_NAMES = ("plan", "tasks", "analyze", "implement")
COMMAND_NAMES = ("speckit.codebase-memory", *(f"speckit.{n}" for n in CORE_NAMES))
OUTPUT_TEMPLATE = "codebase-context-template"
ENV_BACKEND = Path(sys.executable).with_name("codebase-memory-mcp")
CODEBASE_MEMORY_CLI = str(ENV_BACKEND) if ENV_BACKEND.is_file() else shutil.which("codebase-memory-mcp")


def require_backend():
    if CODEBASE_MEMORY_CLI is None:
        if os.environ.get("PRESET_REQUIRE_BACKEND") == "1":
            pytest.fail("Required backend contract job has no executable")
        pytest.skip("Optional backend not installed; contract not verified")


def read_command(name):
    return (PRESET_DIR / "commands" / f"{name}.md").read_text(encoding="utf-8")


def test_manifest_and_documentation_contract():
    manifest = PresetManifest(PRESET_DIR / "preset.yml")
    expected = {("command", n) for n in COMMAND_NAMES} | {("template", OUTPUT_TEMPLATE)}
    assert manifest.id == "codebase-memory-context"
    assert manifest.requires_speckit_version == ">=1.1.2"
    assert {(e["type"], e["name"]) for e in manifest.templates} == expected
    assert all(e["strategy"] == "replace" for e in manifest.templates)
    for entry in manifest.templates:
        assert (PRESET_DIR / entry["file"]).is_file()
    readme = (PRESET_DIR / "README.md").read_text()
    for heading in ("## When to Use It", "## When Not to Use It", "## Development and Validation"):
        assert heading in readme
    assert "specify preset add --dev" in readme
    assert "archive/refs/tags/v1.0.2.zip" in readme
    assert "optional" in readme.lower()
    assert (PRESET_DIR / "LICENSE").is_file()
    assert "Copyright GitHub, Inc." in (PRESET_DIR / "THIRD_PARTY_NOTICES.md").read_text()
    assert (PRESET_DIR / "CHANGELOG.md").is_file()
    assert 2 <= len(manifest.data["tags"]) <= 5
    assert len(manifest.data["preset"]["description"]) < 200


def test_catalog_candidate_matches_manifest():
    manifest = PresetManifest(PRESET_DIR / "preset.yml")
    entry = json.loads((PRESET_DIR / "docs/catalog-entry.v1.1.0.json").read_text())
    for key in ("id", "name", "version", "description", "repository", "license"):
        assert entry[key] == manifest.data["preset"][key]
    assert entry["requires"] == manifest.data["requires"]
    assert entry["tags"] == manifest.data["tags"]
    assert entry["provides"] == {
        "templates": sum(e["type"] == "template" for e in manifest.templates),
        "commands": sum(e["type"] == "command" for e in manifest.templates),
    }
    assert entry["download_url"] == f"{entry['repository']}/releases/download/v{entry['version']}/codebase-memory-context.zip"
    assert entry["documentation"] == f"{entry['repository']}/blob/v{entry['version']}/README.md"
    assert (PRESET_DIR / "docs/publishing.md").is_file()
    for target in re.findall(r"\]\(([^)]+)\)", (PRESET_DIR / "README.md").read_text()):
        if not target.startswith(("https://", "http://", "#")):
            assert (PRESET_DIR / target.split("#", 1)[0]).is_file(), target


@pytest.mark.parametrize("name", CORE_NAMES)
def test_upstream_baseline_preserved_outside_augmentation(name):
    metadata = json.loads((UPSTREAM / "provenance.json").read_text())
    baseline = (UPSTREAM / f"{name}.md").read_bytes()
    assert hashlib.sha256(baseline).hexdigest() == metadata["files"][f"{name}.md"]
    assert version("specify-cli") == "1.1.2"
    bundled = Path(specify_cli.__file__).parent / "core_pack/commands" / f"{name}.md"
    assert baseline == bundled.read_bytes()
    content = read_command(f"speckit.{name}")
    start, end = "<!-- CODEBASE CONTEXT START -->", "<!-- CODEBASE CONTEXT END -->"
    assert content.count(start) == content.count(end) > 0
    additions = re.findall(re.escape(start) + r"(.*?)" + re.escape(end), content, re.S)
    assert any(".specify/memory/codebase.md" in b for b in additions)
    stripped = re.sub(re.escape(start) + r".*?" + re.escape(end), "", content, flags=re.S)
    # Only inserted blocks and their adjacent blank lines differ from upstream.
    nonblank = lambda text: [line for line in text.splitlines() if line.strip()]
    assert nonblank(stripped) == nonblank(baseline.decode())
    assert "Context is optional" in content
    assert "Graph tools are optional" in content
    assert "Inferred" in content and "Unknown" in content


def test_generator_prompt_contract():
    content = read_command("speckit.codebase-memory")
    assert "scripts:" not in content.split("---", 2)[1]
    for heading in ("Scope Guard", "Pre-Execution Checks", "Evidence Rules", "Outline", "Mandatory Post-Execution Hooks", "Completion Report", "Done When"):
        assert f"## {heading}" in content
    steps = re.findall(r"^### (\d+)\. (.+)$", content, re.M)
    assert [number for number, _ in steps] == [str(n) for n in range(1, 8)]
    for rule in (
        "The target is the sole persistent output", "Never run project build",
        "never follow out-of-root links", "Reject target symlinks",
        "Missing optional tools or metadata do not block", "direct-source fallback",
        "Preserve every byte between markers", "--replace-existing",
        "before_codebase_memory", "after_codebase_memory", "optional=true",
        "pending", "not checked", "never directly or indirectly re-enter",
        "unchanged snapshot bytes and identity", "stop if safe commit is unavailable",
        "No edits or alternate templates", ".specify/.codebase-memory.lock",
        "hold it through after-hooks", "fsync", "os.replace",
        "non-cooperating writer", "Do not wait indefinitely, steal a lock",
    ):
        assert rule in content
    assert content.index("## Evidence Rules") < content.index("## Outline")
    assert ".specify/presets/codebase-memory-context/templates/codebase-context-template.md" in content


def test_output_template_contract():
    content = (PRESET_DIR / "templates" / f"{OUTPUT_TEMPLATE}.md").read_text()
    assert 'schema_version: "2.0"' in content
    assert 'generator: "speckit.codebase-memory"' in content
    assert re.findall(r"^## (\d+)\.", content, re.M) == [str(n) for n in range(1, 7)]
    for field in ("source_commit", "working_tree", "analysis_profiles", "evidence_tier"):
        assert f"{field}:" in content
    assert "Working Directory" in content and "Execution Status" in content
    assert "Not executed (discovered only)" in content
    start, end = "<!-- PROJECT OVERRIDES START -->", "<!-- PROJECT OVERRIDES END -->"
    assert content.count(start) == content.count(end) == 1
    assert content.index("## 6. Project Overrides") < content.index(start) < content.index(end)
    assert "secret safety" in content


@pytest.mark.parametrize("archive", [False, True], ids=["directory", "archive"])
def test_install_and_resolve_all_items(tmp_path, archive):
    project = tmp_path / "project"
    (project / ".specify").mkdir(parents=True)
    manager = PresetManager(project)
    clean, bundle = runpy.run_path(str(PRESET_DIR / "tools/package_preset.py"))["build"](PRESET_DIR, tmp_path / "distribution")
    if archive:
        manager.install_from_archive(bundle, "1.1.2")
    else:
        manager.install_from_directory(clean, "1.1.2")
    installed = project / ".specify/presets/codebase-memory-context"
    for noise in (".venv", ".git", "target", "dist", "__pycache__", ".pytest_cache"):
        assert not (installed / noise).exists()
    resolver = PresetResolver(project)
    for name in COMMAND_NAMES:
        assert resolver.resolve_content(name, "command") == read_command(name)
        assert resolver.collect_all_layers(name, "command")[0]["strategy"] == "replace"
    assert resolver.resolve_core("speckit.codebase-memory", "command") is None
    assert resolver.resolve_core(OUTPUT_TEMPLATE, "template") is None
    assert resolver.resolve_content(OUTPUT_TEMPLATE, "template") == (PRESET_DIR / "templates" / f"{OUTPUT_TEMPLATE}.md").read_text()
    assert not (project / ".specify/memory/codebase.md").exists()


@pytest.mark.parametrize("integration", ["codex", "claude", "copilot", "gemini"])
@pytest.mark.parametrize("script", ["py", "sh", "ps"])
def test_cli_renders_all_commands_and_remove_restores_core(tmp_path, monkeypatch, integration, script):
    monkeypatch.chdir(tmp_path)
    result = CliRunner().invoke(app, ["init", "project", "--integration", integration,
        "--script", script, "--preset", str(PRESET_DIR), "--ignore-agent-tools", "--non-interactive"])
    assert result.exit_code == 0, result.output
    project = tmp_path / "project"
    manifest = PresetManifest(PRESET_DIR / "preset.yml")
    def installed_path(name):
        if integration == "codex":
            return project / ".agents/skills" / name.replace(".", "-") / "SKILL.md"
        if integration == "copilot":
            return project / ".github/skills" / name.replace(".", "-") / "SKILL.md"
        if integration == "claude":
            return project / ".claude/skills" / name.replace(".", "-") / "SKILL.md"
        return project / ".gemini/commands" / f"{name}.toml"
    for name in COMMAND_NAMES:
        target = installed_path(name)
        assert target.is_file(), target
        rendered = target.read_text()
        assert ".specify/memory/codebase.md" in rendered
        assert "{SCRIPT}" not in rendered
        assert "__SPECKIT_COMMAND_" not in rendered
        if name != "speckit.codebase-memory":
            assert f"scripts/{ {'py': 'python', 'sh': 'bash', 'ps': 'powershell'}[script] }/" in rendered
        else:
            assert ".specify/presets/codebase-memory-context/templates/codebase-context-template.md" in rendered
    assert (project / ".specify/presets" / manifest.id / "templates" / f"{OUTPUT_TEMPLATE}.md").is_file()
    monkeypatch.chdir(project)
    result = CliRunner().invoke(app, ["preset", "remove", manifest.id])
    assert result.exit_code == 0, result.output
    assert not installed_path("speckit.codebase-memory").exists()
    for name in CORE_NAMES:
        restored = installed_path(f"speckit.{name}").read_text()
        assert ".specify/memory/codebase.md" not in restored
        assert "CODEBASE CONTEXT START" not in restored
        assert "{SCRIPT}" not in restored


@pytest.mark.backend
def test_installed_codebase_memory_backend_contract():
    require_backend()

    version_result = subprocess.run(
        [CODEBASE_MEMORY_CLI, "--version"],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    match = re.search(r"(\d+\.\d+\.\d+)", version_result.stdout)
    assert match is not None
    assert Version(match.group(1)) >= Version("0.10.8")

    required_flags = {
        "list_projects": {"--limit", "--offset"},
        "index_repository": {"--repo-path", "--mode", "--persistence"},
        "trace_path": {"--cursor", "--include-evidence", "--limit"},
        "check_index_coverage": {
            "--paths",
            "--scopes",
            "--scope-limit",
            "--scope-offset",
        },
        "get_architecture": {"--aspects"},
    }
    for tool, flags in required_flags.items():
        help_result = subprocess.run(
            [CODEBASE_MEMORY_CLI, "cli", tool, "--help"],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = help_result.stdout + help_result.stderr
        assert flags <= set(re.findall(r"--[a-z][a-z-]+", output))


@pytest.mark.backend
def test_installed_codebase_memory_mcp_stdio_contract():
    require_backend()

    requests = [
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {
                    "name": "preset-contract-test",
                    "version": "1.1.0",
                },
            },
        },
        {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {},
        },
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "list_projects",
                "arguments": {"limit": 1, "offset": 0},
            },
        },
    ]
    payload = "".join(json.dumps(request) + "\n" for request in requests)
    # A short private runtime avoids version conflicts with an active user backend
    # and macOS Unix-socket path limits. Never stop the user's running server.
    with tempfile.TemporaryDirectory(prefix="cbm-test-", dir="/tmp" if os.name != "nt" else None) as runtime:
        environment = os.environ.copy()
        environment["CBM_RUNTIME_DIR"] = runtime
        result = subprocess.run(
            [CODEBASE_MEMORY_CLI], input=payload, check=False,
            capture_output=True, text=True, timeout=30, env=environment,
        )
    cache_access_denied = (
        "ancestry component validation failed" in result.stderr
        or ("cache-private" in result.stderr and "chmod 0700 failed (errno 1)" in result.stderr)
    )
    if result.returncode != 0 and cache_access_denied:
        if os.environ.get("PRESET_REQUIRE_BACKEND") == "1":
            pytest.fail(result.stderr)
        pytest.skip("Sandbox prevents backend cache access; contract not verified")

    assert result.returncode == 0, result.stderr
    responses = {
        response["id"]: response
        for line in result.stdout.splitlines()
        if line.strip()
        for response in [json.loads(line)]
        if "id" in response
    }

    initialize = responses[1]["result"]
    assert initialize["protocolVersion"] == "2025-06-18"
    assert initialize["serverInfo"]["name"] == "codebase-memory-mcp"
    assert Version(initialize["serverInfo"]["version"]) >= Version("0.10.8")

    required_tools = {
        "index_repository",
        "search_graph",
        "trace_path",
        "get_code_snippet",
        "get_architecture",
        "list_projects",
        "index_status",
        "check_index_coverage",
    }
    listed_tools = {tool["name"] for tool in responses[2]["result"]["tools"]}
    assert required_tools <= listed_tools

    call_result = responses[3]["result"]
    assert call_result["isError"] is False
    assert "projects" in call_result["structuredContent"]


def test_clean_distribution_excludes_development_noise_and_is_reproducible(tmp_path):
    build = runpy.run_path(str(PRESET_DIR / "tools/package_preset.py"))["build"]
    source = tmp_path / "source"
    source.mkdir()
    for name in ("preset.yml", "README.md", "LICENSE", "THIRD_PARTY_NOTICES.md", "CHANGELOG.md"):
        shutil.copyfile(PRESET_DIR / name, source / name)
    for name in ("commands", "templates"):
        shutil.copytree(PRESET_DIR / name, source / name)
    for name in (".venv", ".git", "target", "dist", "__pycache__"):
        (source / name).mkdir()
        (source / name / "noise.txt").write_text("http://development-only.invalid")
    first, zip1 = build(source, tmp_path / "first")
    _, zip2 = build(source, tmp_path / "second")
    assert zip1.read_bytes() == zip2.read_bytes()
    with zipfile.ZipFile(zip1) as bundle:
        assert not any(any(part in name.split("/") for part in (".venv", ".git", "target", "dist", "__pycache__")) for name in bundle.namelist())
    manifest = PresetManifest(first / "preset.yml")
    assert all((first / item["file"]).is_file() for item in manifest.templates)
    with pytest.raises(FileExistsError):
        build(source, tmp_path / "first")
    (source / "commands/speckit.plan.md").unlink()
    (source / "commands/speckit.plan.md").symlink_to(PRESET_DIR / "commands/speckit.plan.md")
    with pytest.raises(ValueError, match="non-symlink"):
        build(source, tmp_path / "unsafe")
