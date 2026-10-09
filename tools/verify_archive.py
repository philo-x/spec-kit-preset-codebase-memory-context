"""Verify a downloaded clean ZIP with real Spec Kit install, resolve and remove."""
import argparse
import tempfile
from pathlib import Path
from specify_cli.presets import PresetManager, PresetResolver


def verify(archive: Path):
    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory)
        (project / ".specify").mkdir()
        manager = PresetManager(project)
        manifest = manager.install_from_archive(archive.resolve(), "1.1.2")
        resolver = PresetResolver(project)
        for item in manifest.templates:
            assert resolver.resolve_content(item["name"], item["type"]), item["name"]
        installed = project / ".specify/presets" / manifest.id
        excluded = {".git", ".venv", "__pycache__", ".pytest_cache", "target", "dist", "artifacts"}
        assert not any(excluded.intersection(p.relative_to(installed).parts) for p in installed.rglob("*"))
        manager.remove(manifest.id)
        assert not installed.exists()
        print(f"Verified {manifest.id} {manifest.version}: {len(manifest.templates)} items; removal succeeded")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    verify(parser.parse_args().archive)
