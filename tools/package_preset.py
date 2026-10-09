"""Build a clean local install directory and reproducible ZIP using only release files."""
import argparse
import posixpath
import re
import tempfile
import zipfile
from pathlib import Path

ROOT_FILES = ("preset.yml", "README.md", "LICENSE", "THIRD_PARTY_NOTICES.md", "CHANGELOG.md")


def build(source: Path, output: Path) -> tuple[Path, Path]:
    source = source.resolve()
    output.mkdir(parents=True, exist_ok=True)
    directory = output / "codebase-memory-context"
    archive = output / "codebase-memory-context.zip"
    if directory.exists() or directory.is_symlink() or archive.exists() or archive.is_symlink():
        raise FileExistsError("Output already exists; choose a fresh output directory")
    files = [source / name for name in ROOT_FILES]
    for folder, patterns in (("commands", ("*.md",)), ("templates", ("*.md",)),
                             ("docs", ("*.md", "*.json")),
                             ("tests/fixtures/upstream", ("*.md", "*.json"))):
        for pattern in patterns:
            files.extend(p for p in (source / folder).rglob(pattern) if "artifacts" not in p.relative_to(source).parts)
    excluded = {".git", ".venv", "__pycache__", ".pytest_cache", "target", "dist", "artifacts"}
    files = sorted({p for p in files if not excluded.intersection(p.relative_to(source).parts)})
    for path in files:
        if not path.is_file() or path.is_symlink() or any(p.is_symlink() for p in path.parents if p != source.parent):
            raise ValueError(f"Release input must be a regular non-symlink file: {path}")
        path.resolve().relative_to(source)
    # Stage completely before exposing a directory to the installer.
    with tempfile.TemporaryDirectory(dir=output) as staging:
        stage = Path(staging) / "codebase-memory-context"
        stage.mkdir()
        for path in files:
            relative = path.relative_to(source)
            dest = stage / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            content = path.read_bytes()
            # Evidence logs and build artifacts stay in the source repository.
            # Keep documentation navigation usable when a linked file is not shipped.
            if relative.suffix == ".md" and relative.parts[0] not in ("commands", "templates"):
                selected = {p.relative_to(source).as_posix() for p in files}
                def link(match):
                    url = match.group(1)
                    if ":" in url or url.startswith("#"):
                        return match.group(0)
                    target = posixpath.normpath(posixpath.join(relative.parent.as_posix(), url.split("#", 1)[0]))
                    if target in selected:
                        return match.group(0)
                    fragment = "#" + url.split("#", 1)[1] if "#" in url else ""
                    return "](https://github.com/philo-x/spec-kit-preset-codebase-memory-context/blob/main/" + target + fragment + ")"
                content = re.sub(r"\]\(([^)]+)\)", link, content.decode("utf-8")).encode("utf-8")
            dest.write_bytes(content)
        # Exclusive archive creation refuses accidental overwrite.
        with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as bundle:
            for path in files:
                relative = path.relative_to(source)
                info = zipfile.ZipInfo(f"codebase-memory-context/{relative.as_posix()}", (1980, 1, 1, 0, 0, 0))
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                bundle.writestr(info, (stage / relative).read_bytes())
        stage.rename(directory)
    return directory, archive


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("dist"))
    args = parser.parse_args()
    for path in build(Path(__file__).resolve().parents[1], args.output_dir):
        print(path.resolve())
