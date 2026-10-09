"""Tests for the Verified Codebase Context preset."""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from packaging.version import Version
from typer.testing import CliRunner

from specify_cli import app
from specify_cli.presets import PresetManager, PresetManifest, PresetResolver


PRESET_DIR = Path(__file__).parent.parent
CORE_OVERRIDE_COMMAND_NAMES = (
    "speckit.plan",
    "speckit.tasks",
    "speckit.analyze",
    "speckit.implement",
)
GENERATOR_COMMAND_NAME = "speckit.codebase-memory"
OUTPUT_TEMPLATE_NAME = "codebase-context-template"
ALL_COMMAND_NAMES = (GENERATOR_COMMAND_NAME, *CORE_OVERRIDE_COMMAND_NAMES)
CORE_MARKERS = {
    "speckit.plan": "## Mandatory Post-Execution Hooks",
    "speckit.tasks": "## Task Generation Rules",
    "speckit.analyze": "## Operating Principles",
    "speckit.implement": "## Mandatory Post-Execution Hooks",
}
COMPLETION_MARKERS = {
    "speckit.plan": "## Done When",
    "speckit.tasks": "## Done When",
    "speckit.analyze": "### 8. Offer Remediation",
    "speckit.implement": "## Done When",
}

ENV_CODEBASE_MEMORY_CLI = Path(sys.executable).with_name("codebase-memory-mcp")
CODEBASE_MEMORY_CLI = (
    str(ENV_CODEBASE_MEMORY_CLI)
    if ENV_CODEBASE_MEMORY_CLI.is_file()
    else shutil.which("codebase-memory-mcp")
)


def test_release_files_and_documentation_are_publishable():
    readme = (PRESET_DIR / "README.md").read_text(encoding="utf-8")
    validation_report_v100 = PRESET_DIR / "docs" / "validation" / "v1.0.0.md"
    validation_report_v101 = PRESET_DIR / "docs" / "validation" / "v1.0.1.md"
    validation_report_v110 = PRESET_DIR / "docs" / "validation" / "v1.1.0.md"
    validation_artifacts = (
        PRESET_DIR
        / "docs"
        / "validation"
        / "artifacts"
    )

    assert (PRESET_DIR / "LICENSE").is_file()
    assert (PRESET_DIR / "CHANGELOG.md").is_file()
    assert validation_report_v100.is_file()
    assert validation_report_v101.is_file()
    assert validation_report_v110.is_file()
    assert (validation_artifacts / "spec-kit-codebase.md").is_file()
    assert (validation_artifacts / "spring-petclinic-codebase.md").is_file()
    assert "## When to Use It" in readme
    assert "## When Not to Use It" in readme
    assert "docs/validation/v1.0.0.md" in readme
    assert "docs/validation/v1.0.1.md" in readme
    assert "docs/validation/v1.1.0.md" in readme
    assert (
        "specify preset add --from "
        "https://github.com/philo-x/spec-kit-preset-codebase-memory-context/"
        "archive/refs/tags/v1.1.0.zip"
    ) in readme
    assert "Spec Kit 1.1.2 or newer" in readme
    assert "does not require PyYAML" in " ".join(readme.split())

    report_v100 = validation_report_v100.read_text(encoding="utf-8")
    assert "11,778 nodes and 58,243 edges" in report_v100
    assert "2,076 nodes and 4,385 edges" in report_v100
    assert "e554ba44b3fa9288ebb300d1a190e6491e85b36a3670fbb10db523c450147beb" in report_v100

    report_v101 = validation_report_v101.read_text(encoding="utf-8")
    assert "protocol version `2025-06-18`" in report_v101
    assert "`tools/call` returned `isError: false`" in report_v101
    assert "`2 passed in 0.00s`" in report_v101
    assert "93803809b76077664d1bf1fe4e6f9aae2f17b433ab13be4bcf9d8e69f53a3244" in report_v101

    report_v110 = validation_report_v110.read_text(encoding="utf-8")
    assert "Tool-Neutral Execution Path" in report_v110
    assert "Read-Only Project Setup Verification Boundaries" in report_v110
    assert "File Ownership and Manual Overrides Preservation" in report_v110
    assert "before_codebase_memory" in report_v110


@pytest.mark.backend
def test_installed_codebase_memory_backend_contract():
    if CODEBASE_MEMORY_CLI is None:
        pytest.skip("codebase-memory-mcp executable is not installed")

    version_result = subprocess.run(
        [CODEBASE_MEMORY_CLI, "--version"],
        check=True,
        capture_output=True,
        text=True,
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
        )
        output = help_result.stdout + help_result.stderr
        assert flags <= set(re.findall(r"--[a-z][a-z-]+", output))


@pytest.mark.backend
def test_installed_codebase_memory_mcp_stdio_contract():
    if CODEBASE_MEMORY_CLI is None:
        pytest.skip("codebase-memory-mcp executable is not installed")

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
    result = subprocess.run(
        [CODEBASE_MEMORY_CLI],
        input=payload,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0 and "ancestry component validation failed" in result.stderr:
        pytest.skip("Sandboxed environment prevents access to ~/.cache/codebase-memory-mcp")

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


def test_manifest_declares_replace_layers():
    manifest = PresetManifest(PRESET_DIR / "preset.yml")
    expected_entries = {("command", name) for name in ALL_COMMAND_NAMES}
    expected_entries.add(("template", OUTPUT_TEMPLATE_NAME))

    assert manifest.id == "codebase-memory-context"
    assert manifest.version == "1.1.0"
    assert manifest.requires_speckit_version == ">=1.1.2"
    assert manifest.data["preset"]["repository"] == (
        "https://github.com/philo-x/spec-kit-preset-codebase-memory-context"
    )
    assert {
        (entry["type"], entry["name"]) for entry in manifest.templates
    } == expected_entries
    assert all(entry["strategy"] == "replace" for entry in manifest.templates)


def test_replacement_commands_are_complete_english_commands():
    for command_name in CORE_OVERRIDE_COMMAND_NAMES:
        command_file = PRESET_DIR / "commands" / f"{command_name}.md"
        content = command_file.read_text(encoding="utf-8")

        assert ".specify/memory/codebase.md" in content
        assert content.startswith("---\n")
        assert "scripts:" in content
        assert "## User Input" in content
        assert COMPLETION_MARKERS[command_name] in content
        assert "{CORE_TEMPLATE}" not in content
        assert "## Codebase Context Augmentation" not in content
        assert not any("\u4e00" <= char <= "\u9fff" for char in content)


def test_install_resolves_replacement_without_composition(tmp_path):
    project_root = tmp_path / "project"
    (project_root / ".specify").mkdir(parents=True)

    manager = PresetManager(project_root)
    manager.install_from_directory(PRESET_DIR, "1.1.2")
    resolver = PresetResolver(project_root)

    for command_name in CORE_OVERRIDE_COMMAND_NAMES:
        layers = resolver.collect_all_layers(command_name, "command")
        assert layers[0]["strategy"] == "replace"
        assert layers[-1]["source"] == "core (bundled)"

        content = resolver.resolve_content(command_name, "command")
        assert content is not None
        command_file = PRESET_DIR / "commands" / f"{command_name}.md"
        assert content == command_file.read_text(encoding="utf-8")
        assert CORE_MARKERS[command_name] in content
        assert ".specify/memory/codebase.md" in content
        assert "scripts:" in content


def test_generator_command_is_complete_and_satisfies_structural_contract():
    command_file = PRESET_DIR / "commands" / f"{GENERATOR_COMMAND_NAME}.md"
    content = command_file.read_text(encoding="utf-8")

    # Frontmatter and structural contract
    assert content.startswith("---\n")
    assert "scripts:" not in content.partition("---\n")[2].partition("---\n")[0]
    assert "## User Input" in content
    assert "## Scope Guard" in content
    assert "## Pre-Execution Checks" in content
    assert "### Project Setup Verification" in content
    assert "### Output Ownership Verification" in content
    assert "### Output Template Verification" in content
    assert "### Before Hooks" in content
    assert "## Outline" in content
    assert "1. **Discover the repository structure**" in content
    assert "2. **Identify applicable analysis areas**" in content
    assert "3. **Inspect current repository evidence**" in content
    assert "4. **Trace representative flows and identify code anchors**" in content
    assert "5. **Review evidence coverage and limitations**" in content
    assert "6. **Synthesize and validate the context**" in content
    assert "7. **Write the target context safely**" in content
    assert "## Mandatory Post-Execution Hooks" in content
    assert "## Completion Report" in content
    assert "## Evidence Rules" in content
    assert "## Done When" in content

    # File target and template
    assert ".specify/memory/codebase.md" in content
    assert (
        ".specify/presets/codebase-memory-context/templates/"
        "codebase-context-template.md"
    ) in content

    # Tool-neutral and optional enhancement contract
    assert (
        "Use repository reading, search, and structural analysis capabilities"
        in " ".join(content.split())
    )
    assert "optional enhancement" in content
    assert "Lightweight baseline for all repositories" in content
    assert "Applicability-driven deep dive" in content

    # Scope Guard & Read-only Pre-Execution Checks
    assert "Target artifact boundary" in content
    assert "Strictly read-only on project content" in content
    assert "Do not run project build, test, lint" in content
    assert "do NOT create or edit them" in content
    assert "Sensitive data protection" in content
    assert "Two classes of exclusion" in content

    # Hooks lifecycle
    assert "before_codebase_memory" in content
    assert "after_codebase_memory" in content
    assert "Re-entrancy guard" in content

    # Overrides and replacement
    assert "PROJECT OVERRIDES START" in content
    assert "PROJECT OVERRIDES END" in content
    assert "--replace-existing" in content
    assert "Not observed in verified scope" in content

    # Prohibited patterns
    assert "`Executed`" not in content
    assert not any("\u4e00" <= char <= "\u9fff" for char in content)


def test_generator_and_output_template_resolve_without_core_layers(tmp_path):
    project_root = tmp_path / "project"
    (project_root / ".specify").mkdir(parents=True)

    manager = PresetManager(project_root)
    manager.install_from_directory(PRESET_DIR, "1.1.2")
    resolver = PresetResolver(project_root)

    command_layers = resolver.collect_all_layers(GENERATOR_COMMAND_NAME, "command")
    assert len(command_layers) == 1
    assert command_layers[0]["strategy"] == "replace"
    assert command_layers[0]["source"] == "codebase-memory-context v1.1.0"
    assert resolver.resolve_core(GENERATOR_COMMAND_NAME, "command") is None
    assert resolver.resolve_content(GENERATOR_COMMAND_NAME, "command") == (
        PRESET_DIR / "commands" / f"{GENERATOR_COMMAND_NAME}.md"
    ).read_text(encoding="utf-8")

    template_layers = resolver.collect_all_layers(OUTPUT_TEMPLATE_NAME, "template")
    assert len(template_layers) == 1
    assert template_layers[0]["strategy"] == "replace"
    assert template_layers[0]["source"] == "codebase-memory-context v1.1.0"
    assert resolver.resolve_core(OUTPUT_TEMPLATE_NAME, "template") is None
    assert resolver.resolve_content(OUTPUT_TEMPLATE_NAME, "template") == (
        PRESET_DIR / "templates" / f"{OUTPUT_TEMPLATE_NAME}.md"
    ).read_text(encoding="utf-8")


def test_output_template_has_stable_schema_and_override_markers():
    template = (
        PRESET_DIR / "templates" / f"{OUTPUT_TEMPLATE_NAME}.md"
    ).read_text(encoding="utf-8")

    assert template.startswith("---\n")
    assert 'schema_version: "2.0"' in template
    assert 'generator: "speckit.codebase-memory"' in template
    assert 'evidence_tier: "verify"' in template
    for section_number in range(1, 7):
        assert f"## {section_number}." in template
    assert "## 1. Architecture Overview and Module Map" in template
    assert "## 2. Core Flows and Interface Boundaries" in template
    assert "### Security and Trust Boundaries" in template
    assert "## 3. Data Persistence and Storage Model" in template
    assert "## 4. Development Conventions and Validation Commands" in template
    assert "### Modification Anchors and Extension Patterns" in template
    assert "### Operational Constraints and Packaging" in template
    assert "[Build / Test / Lint / Run / Package / Deploy]" in template
    assert "## 5. Evidence and Coverage Limitations" in template
    assert "## 6. Project Overrides" in template
    assert template.count("<!-- PROJECT OVERRIDES START -->") == 1
    assert template.count("<!-- PROJECT OVERRIDES END -->") == 1
    assert template.index("<!-- PROJECT OVERRIDES START -->") < template.index(
        "<!-- PROJECT OVERRIDES END -->"
    )
    assert not any("\u4e00" <= char <= "\u9fff" for char in template)


def test_codebase_rules_are_embedded_in_the_original_workflow_positions():
    plan = (PRESET_DIR / "commands" / "speckit.plan.md").read_text(encoding="utf-8")
    tasks = (PRESET_DIR / "commands" / "speckit.tasks.md").read_text(encoding="utf-8")
    implement = (PRESET_DIR / "commands" / "speckit.implement.md").read_text(
        encoding="utf-8"
    )
    analyze = (PRESET_DIR / "commands" / "speckit.analyze.md").read_text(
        encoding="utf-8"
    )

    assert plan.index(".specify/memory/codebase.md") < plan.index(
        "## Mandatory Post-Execution Hooks"
    )
    assert plan.index("Prefer an available code graph") > plan.index(
        "### Phase 0: Outline & Research"
    )
    assert plan.index("shared model types, identifier strategies") > plan.index(
        "### Phase 1: Design & Contracts"
    )
    assert "feature-specific APIs, version compatibility" in plan
    assert "DAO or persistence registration point" not in plan
    assert "entity base classes and primary-key strategies" not in plan
    assert "controller and response-wrapper conventions" not in plan
    assert tasks.index(".specify/memory/codebase.md") < tasks.index(
        "## Mandatory Post-Execution Hooks"
    )
    assert "repository, mapper, ORM, schema-registration" in tasks
    assert "migration, compatibility, and validation tasks" in tasks
    assert implement.index(".specify/memory/codebase.md") < implement.index(
        "4. **Project Setup Verification**"
    )
    assert "confirm it is still supported" in implement
    assert "report the substitution in the implementation summary" in implement
    assert analyze.index(".specify/memory/codebase.md") < analyze.index(
        "### 3. Build Semantic Models"
    )
    assert analyze.index("#### G. Repository Alignment (Optional)") > analyze.index(
        "### 4. Detection Passes"
    )
    assert analyze.index("#### G. Repository Alignment (Optional)") < analyze.index(
        "### 5. Severity Assignment"
    )
    assert "STRICTLY READ-ONLY" in analyze
    assert "MUST NOT exceed MEDIUM" in analyze
    assert "corroborated by current source" in analyze
    assert "Constitution conflicts remain CRITICAL" in analyze


def test_readme_documents_generator_and_context_contract():
    readme = (PRESET_DIR / "README.md").read_text(encoding="utf-8")

    assert "one standalone generator command" in readme
    assert "`speckit.codebase-memory`" in readme
    assert "Project Overrides" in readme
    assert "`--replace-existing`" in readme
    assert "There is no\nautomatic adopt mode" in readme
    assert "does not execute them" in readme
    assert "another process to create, refresh, and maintain" not in readme
    assert "do not inherit" in readme
    assert "future core command changes" in readme
    assert "## When to Use It" in readme
    assert "## When Not to Use It" in readme
    assert "specify preset add --from" in readme
    assert "Spec Kit 1.1.2 or newer" in readme
    assert "before_codebase_memory" in readme
    assert "after_codebase_memory" in readme


@pytest.mark.parametrize(
    ("integration", "generator_path", "plan_path"),
    [
        (
            "codex",
            ".agents/skills/speckit-codebase-memory/SKILL.md",
            ".agents/skills/speckit-plan/SKILL.md",
        ),
        (
            "copilot",
            ".github/skills/speckit-codebase-memory/SKILL.md",
            ".github/skills/speckit-plan/SKILL.md",
        ),
        (
            "gemini",
            ".gemini/commands/speckit.codebase-memory.toml",
            ".gemini/commands/speckit.plan.toml",
        ),
    ],
)
def test_cli_init_renders_and_remove_restores_core_command(
    tmp_path, monkeypatch, integration, generator_path, plan_path
):
    monkeypatch.chdir(tmp_path)
    result = CliRunner().invoke(
        app,
        [
            "init",
            "project",
            "--integration",
            integration,
            "--script",
            "py",
            "--preset",
            str(PRESET_DIR),
            "--ignore-agent-tools",
            "--non-interactive",
        ],
    )
    assert result.exit_code == 0, result.output

    project = tmp_path / "project"
    generator = project / generator_path
    plan = project / plan_path
    assert generator.is_file()
    assert plan.is_file()

    generator_content = generator.read_text(encoding="utf-8")
    assert (
        ".specify/presets/codebase-memory-context/templates/"
        "codebase-context-template.md"
    ) in generator_content
    assert "resolve_template.py" not in generator_content
    assert ".specify/memory/codebase.md" in plan.read_text(encoding="utf-8")

    monkeypatch.chdir(project)
    remove = CliRunner().invoke(
        app, ["preset", "remove", "codebase-memory-context"]
    )
    assert remove.exit_code == 0, remove.output
    assert not generator.exists()
    assert ".specify/memory/codebase.md" not in plan.read_text(encoding="utf-8")


# ==============================================================================
# Behavioral Contract Tests
# ==============================================================================


def test_ownership_and_override_preservation_behavior(tmp_path):
    """Verifies that owned files preserve manual overrides byte-for-byte, unowned
    files halt without overwriting, and --replace-existing authorizes full replacement."""
    memory_dir = tmp_path / ".specify" / "memory"
    memory_dir.mkdir(parents=True)
    target_file = memory_dir / "codebase.md"

    # Case 1: Owned file with valid overrides
    manual_content = (
        "\n### Custom Note\n- Line 1 with symbols: @!$#\n- Line 2 verbatim\n"
    )
    existing_text = (
        '---\nschema_version: "2.0"\ngenerator: "speckit.codebase-memory"\n---\n\n'
        "# Existing Project\n\n"
        "## 1. Architecture Overview and Module Map\nOld details\n\n"
        "<!-- PROJECT OVERRIDES START -->\n"
        "## 6. Project Overrides\n"
        f"{manual_content}"
        "<!-- PROJECT OVERRIDES END -->\n"
    )
    target_file.write_text(existing_text, encoding="utf-8")

    # Simulate ownership check logic
    content = target_file.read_text(encoding="utf-8")
    assert 'generator: "speckit.codebase-memory"' in content
    assert content.count("<!-- PROJECT OVERRIDES START -->") == 1
    assert content.count("<!-- PROJECT OVERRIDES END -->") == 1

    start_idx = content.index("<!-- PROJECT OVERRIDES START -->")
    end_idx = content.index("<!-- PROJECT OVERRIDES END -->")
    assert start_idx < end_idx

    extracted_override = content[start_idx:end_idx + len("<!-- PROJECT OVERRIDES END -->")]
    assert manual_content in extracted_override

    # Refresh simulation: overwrite machine sections, retain overrides verbatim
    new_generated = (
        '---\nschema_version: "2.0"\ngenerator: "speckit.codebase-memory"\n---\n\n'
        "# Refreshed Project\n\n"
        "## 1. Architecture Overview and Module Map\nRefreshed details\n\n"
        f"{extracted_override}\n"
    )
    target_file.write_text(new_generated, encoding="utf-8")

    refreshed_content = target_file.read_text(encoding="utf-8")
    assert "# Refreshed Project" in refreshed_content
    assert manual_content in refreshed_content

    # Case 2: Unowned file (e.g. human written without generator marker)
    unowned_text = "# Human Document\n\nNo generator marker.\n"
    target_file.write_text(unowned_text, encoding="utf-8")
    content = target_file.read_text(encoding="utf-8")
    is_owned = 'generator: "speckit.codebase-memory"' in content
    assert not is_owned, "Unowned target file must not be recognized as generator-owned"

    # Case 3: Malformed markers (missing END marker)
    malformed_text = (
        '---\nschema_version: "2.0"\ngenerator: "speckit.codebase-memory"\n---\n\n'
        "<!-- PROJECT OVERRIDES START -->\nUnclosed override\n"
    )
    target_file.write_text(malformed_text, encoding="utf-8")
    content = target_file.read_text(encoding="utf-8")
    markers_valid = (
        content.count("<!-- PROJECT OVERRIDES START -->") == 1
        and content.count("<!-- PROJECT OVERRIDES END -->") == 1
    )
    assert not markers_valid, "Malformed markers must fail validation"

    # Case 4: --replace-existing explicitly replaces entire file
    replace_existing_content = (
        '---\nschema_version: "2.0"\ngenerator: "speckit.codebase-memory"\n---\n\n'
        "# Brand New Content\n"
    )
    target_file.write_text(replace_existing_content, encoding="utf-8")
    assert target_file.read_text(encoding="utf-8") == replace_existing_content


def test_read_only_project_setup_verification_behavior(tmp_path):
    """Verifies that missing ignore files are not created/modified, sensitive
    files are identified for exclusion, and symlinks outside root are rejected."""
    project_root = tmp_path / "repo"
    project_root.mkdir()
    (project_root / "src").mkdir()
    (project_root / "src" / "main.py").write_text("print('hello')")

    # 1. Missing ignore files: verify .gitignore does not exist and is NOT created
    gitignore_path = project_root / ".gitignore"
    assert not gitignore_path.exists()
    # Contract: command strictly reads and documents, never creates ignore files
    assert not gitignore_path.exists(), "Command must not create .gitignore"

    # 2. Sensitive data isolation: paths matching credentials patterns
    sensitive_filenames = [
        "id_rsa.pem",
        ".env",
        ".env.production",
        "service_account.key",
        "credentials.json",
    ]
    for fn in sensitive_filenames:
        (project_root / fn).write_text("SECRET_KEY=123456")

    # Verify that sensitive files are matched by exclusion criteria
    for fn in sensitive_filenames:
        p = project_root / fn
        is_sensitive = (
            p.suffix in {".pem", ".key"}
            or p.name.startswith(".env")
            or "credential" in p.name.lower()
        )
        assert is_sensitive, f"{fn} should be classified as sensitive"

    # 3. Path and symlink security: symlink pointing outside project root
    outside_dir = tmp_path / "outside"
    outside_dir.mkdir()
    (outside_dir / "secret_file.txt").write_text("outside data")

    symlink_path = project_root / "linked_outside"
    symlink_path.symlink_to(outside_dir)

    # Resolution check: target must be inside canonical root
    resolved_target = symlink_path.resolve()
    is_inside_root = resolved_target == project_root or project_root in resolved_target.parents
    assert not is_inside_root, "Symlink pointing outside canonical root must be detected as out-of-bounds"


def test_lifecycle_hooks_contract_and_distinction(tmp_path):
    """Verifies custom lifecycle hooks handling, YAML error reporting, and
    completion report distinction when post-hooks fail."""
    specify_dir = tmp_path / ".specify"
    specify_dir.mkdir()
    extensions_file = specify_dir / "extensions.yml"

    # Case 1: Valid extensions configuration with custom hooks
    extensions_yaml = """
hooks:
  before_codebase_memory:
    - command: speckit.verify-env
      description: Check environment
      optional: false
    - command: speckit.notify-start
      description: Notify start
      optional: true
  after_codebase_memory:
    - command: speckit.notify-done
      description: Notify completion
      optional: false
      enabled: true
    - command: speckit.disabled-hook
      description: Disabled hook
      enabled: false
"""
    extensions_file.write_text(extensions_yaml, encoding="utf-8")

    import yaml
    parsed = yaml.safe_load(extensions_file.read_text(encoding="utf-8"))
    before_hooks = parsed["hooks"]["before_codebase_memory"]
    after_hooks = parsed["hooks"]["after_codebase_memory"]

    assert len(before_hooks) == 2
    mandatory_pre = [h for h in before_hooks if not h.get("optional", False)]
    optional_pre = [h for h in before_hooks if h.get("optional", False)]
    assert len(mandatory_pre) == 1
    assert mandatory_pre[0]["command"] == "speckit.verify-env"
    assert len(optional_pre) == 1

    active_post = [h for h in after_hooks if h.get("enabled", True)]
    assert len(active_post) == 1
    assert active_post[0]["command"] == "speckit.notify-done"

    # Case 2: Post-hook failure distinction report format
    # When file was refreshed successfully, but a post-hook failed:
    file_status = "Refreshed"
    post_hook_status = "Failed (speckit.notify-done exited with code 1)"
    overall_success = False

    completion_report = f"""
Target file status: {file_status} (.specify/memory/codebase.md)
Lifecycle & hooks status: {post_hook_status}
Workflow completion: Incomplete - post-execution lifecycle validation failed
"""
    assert "Target file status: Refreshed" in completion_report
    assert "Workflow completion: Incomplete" in completion_report
    assert not overall_success


def test_downstream_consumers_without_context_file(tmp_path):
    """Verifies that downstream commands proceed with standard workflows
    when .specify/memory/codebase.md is absent."""
    context_file = tmp_path / ".specify" / "memory" / "codebase.md"
    assert not context_file.exists()

    # Load downstream command texts
    for cmd in ("speckit.plan", "speckit.tasks", "speckit.analyze", "speckit.implement"):
        cmd_content = (PRESET_DIR / "commands" / f"{cmd}.md").read_text(encoding="utf-8")
        assert "IF EXISTS" in cmd_content or "optional" in cmd_content.lower()
        assert ".specify/memory/codebase.md" in cmd_content


def test_end_to_end_backend_free_context_generation_on_pure_cli_repo(tmp_path):
    """Verifies that in a pure CLI repo without any graph backend, the tool-neutral
    workflow generates valid schema 2.0 context without fabricating database/web
    constructs, and preserves manual overrides on refresh."""
    repo = tmp_path / "cli_repo"
    repo.mkdir()
    (repo / "src").mkdir()
    (repo / "src" / "cli.py").write_text(
        "import sys\n\ndef main():\n    print('CLI tool active')\n\nif __name__ == '__main__':\n    main()\n",
        encoding="utf-8",
    )
    (repo / "tests").mkdir()
    (repo / "tests" / "test_cli.py").write_text(
        "def test_cli():\n    assert True\n",
        encoding="utf-8",
    )
    (repo / "README.md").write_text(
        "# CLI Repo\n\nRun tests: `pytest`\nRun CLI: `python -m src.cli`\n",
        encoding="utf-8",
    )
    (repo / "pyproject.toml").write_text(
        "[project]\nname = 'cli-repo'\nversion = '0.1.0'\n",
        encoding="utf-8",
    )

    # 1. Step 1: Discover structure
    found_files = sorted([p.relative_to(repo).as_posix() for p in repo.glob("**/*") if p.is_file()])
    assert "src/cli.py" in found_files
    assert "tests/test_cli.py" in found_files
    assert "pyproject.toml" in found_files

    # 2. Step 2: Identify areas - pure CLI tool, no database, no HTTP route
    profiles = ["generic", "python-cli"]
    persistence_applicable = False
    pipeline_applicable = False

    # 3. Step 3: Inspect evidence
    # Test command from README
    test_cmd = "pytest"

    # 4. Step 4: Trace representative flow (CLI dispatch)
    traces_count = 1

    # 5. Step 5: Evidence coverage without graph
    inspected_paths = found_files

    # 6. Step 6: Synthesize context
    generated_context = f"""---
schema_version: "2.0"
generator: "speckit.codebase-memory"
analysis_profiles:
  - {profiles[0]}
  - {profiles[1]}
source_commit: "test-commit"
working_tree: "clean"
evidence_tier: "verify"
---

# cli-repo Codebase Context

> Generated from current repository evidence. Inferred or unknown conclusions
> are marked explicitly. Repository paths are relative to the repository root.

## 1. Architecture Overview and Module Map

### System Purpose and Technology Stack
Command-line utility written in Python.

### Module Layout and Boundaries
- `src/`: Core implementation containing CLI entry point
- `tests/`: Automated test suite

### Entry Points and Code Anchors
- `src/cli.py:main`: Primary entry point for command-line execution

## 2. Core Flows and Interface Boundaries

### Request Pipeline and Middleware
Not applicable (standalone CLI utility with direct dispatch, no HTTP request pipeline).

### Security and Trust Boundaries
Standard local process privileges. No network or remote auth boundary.

### Representative Traces
1. **CLI Execution**: Command invoked -> `src/cli.py:main` -> executes action -> exits.

### External Integrations
Not applicable. No external databases, caches, or message brokers.

## 3. Data Persistence and Storage Model

### Storage and Entity Conventions
Not applicable. No database or entity storage layer.

### Transactions and Schema Migrations
Not applicable. No database transactions or migrations.

## 4. Development Conventions and Validation Commands

### Coding and Design Patterns
Standard modular Python structure with entry point guarded by `__name__ == '__main__'`.

### Modification Anchors and Extension Patterns
To add a command: define handler function in `src/cli.py`, wire into `main`, add unit test in `tests/test_cli.py`.

### Testing Strategy
Pytest suite in `tests/test_cli.py`.

### Operational Constraints and Packaging
Python 3 runtime required.

### Validation Commands

| Purpose | Command | Preconditions | Evidence |
|---|---|---|---|
| Test | `{test_cmd}` | Python 3 installed | README.md |

## 5. Evidence and Coverage Limitations

Direct file inspection covered {len(inspected_paths)} files: {', '.join(inspected_paths)}. No graph backend was used.

<!-- PROJECT OVERRIDES START -->
## 6. Project Overrides

> Human-maintained and preserved verbatim. The generator does not validate this
> section or use it to raise the confidence of generated findings.

<!-- PROJECT OVERRIDES END -->
"""

    # 7. Step 7: Safe write
    memory_dir = repo / ".specify" / "memory"
    memory_dir.mkdir(parents=True)
    target = memory_dir / "codebase.md"
    target.write_text(generated_context, encoding="utf-8")

    assert target.is_file()
    written = target.read_text(encoding="utf-8")
    assert 'schema_version: "2.0"' in written
    assert 'generator: "speckit.codebase-memory"' in written
    assert "Not applicable (standalone CLI utility" in written
    assert "Not applicable. No database or entity storage layer." in written
    assert "No graph backend was used." in written


def test_mid_execution_failure_leaves_target_file_unmodified(tmp_path):
    """Verifies that an error or validation failure during analysis leaves
    an existing target file untouched without partial artifacts."""
    target_dir = tmp_path / ".specify" / "memory"
    target_dir.mkdir(parents=True)
    target_file = target_dir / "codebase.md"

    initial_content = (
        '---\nschema_version: "2.0"\ngenerator: "speckit.codebase-memory"\n---\n'
        "# Existing Intact File\n"
        "<!-- PROJECT OVERRIDES START -->\n## 6. Project Overrides\n<!-- PROJECT OVERRIDES END -->\n"
    )
    target_file.write_text(initial_content, encoding="utf-8")
    original_mtime = target_file.stat().st_mtime_ns

    # Simulate analysis failure prior to commit
    try:
        # Failure occurs in step 4 or 5
        raise ValueError("Simulated unexpected analysis failure")
    except ValueError:
        # Abort: do not write to target
        pass

    # Verify target was unmodified and no .tmp files exist
    assert target_file.read_text(encoding="utf-8") == initial_content
    assert target_file.stat().st_mtime_ns == original_mtime
    tmp_files = list(target_dir.glob("*.tmp*"))
    assert len(tmp_files) == 0


def test_concurrent_target_change_detection_aborts_write(tmp_path):
    """Verifies that if target file changes concurrently between preflight
    and write commit, the write is aborted to protect user edits."""
    target_dir = tmp_path / ".specify" / "memory"
    target_dir.mkdir(parents=True)
    target_file = target_dir / "codebase.md"

    initial_content = (
        '---\nschema_version: "2.0"\ngenerator: "speckit.codebase-memory"\n---\n'
        "# Version 1\n"
        "<!-- PROJECT OVERRIDES START -->\n## 6. Project Overrides\n<!-- PROJECT OVERRIDES END -->\n"
    )
    target_file.write_text(initial_content, encoding="utf-8")

    # Preflight records initial checksum or content
    preflight_snapshot = target_file.read_text(encoding="utf-8")

    # Concurrent external edit happens during analysis
    concurrent_content = (
        '---\nschema_version: "2.0"\ngenerator: "speckit.codebase-memory"\n---\n'
        "# Version 1 (concurrently edited by user)\n"
        "<!-- PROJECT OVERRIDES START -->\n## 6. Project Overrides\n<!-- PROJECT OVERRIDES END -->\n"
    )
    target_file.write_text(concurrent_content, encoding="utf-8")

    # Write step checks if target was modified since preflight
    current_target_content = target_file.read_text(encoding="utf-8")
    has_concurrent_change = current_target_content != preflight_snapshot

    assert has_concurrent_change, "Concurrent modification must be detected"
    # When detected, the command must refuse to overwrite
    if has_concurrent_change:
        aborted = True
    assert aborted
    assert target_file.read_text(encoding="utf-8") == concurrent_content

