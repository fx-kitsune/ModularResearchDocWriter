"""Install the bundled ModularResearchDocWriter skill and toolkit."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path
from typing import Optional, Tuple

DEFAULT_SKILL_NAME = "modular-research-doc-writer"
TOOLKIT_DIR_NAME = "mrm-toolkit"
TOOLKIT_HOME_ENV = "MRM_TOOLKIT_HOME"


def default_skills_dir() -> Path:
    """Return the default agent skills directory for the current user."""
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "skills"
    return Path.home() / ".codex" / "skills"


def default_toolkit_dir() -> Path:
    """Return the cross-platform per-user MRM toolkit directory."""
    toolkit_home = os.environ.get(TOOLKIT_HOME_ENV)
    if toolkit_home:
        return Path(toolkit_home).expanduser()
    return Path.home() / ".mrm-toolkit"


def package_root() -> Path:
    """Return the filesystem path to this Python package."""
    return Path(__file__).resolve().parent


def bundled_skill_file() -> Path:
    """Return the SKILL.md from the bundled mrm-toolkit directory.

    The skill file lives inside the toolkit tree, not duplicated in the
    Python package.  Falls back to the package-local path when the toolkit
    directory is not found (e.g. editable installs during development).
    """
    toolkit = bundled_toolkit_dir()
    if toolkit is not None:
        candidate = toolkit / "skills" / DEFAULT_SKILL_NAME / "SKILL.md"
        if candidate.is_file():
            return candidate
    # Fallback: package-local copy (development / legacy layout)
    return package_root() / "skills" / DEFAULT_SKILL_NAME / "SKILL.md"


def bundled_toolkit_dir() -> Optional[Path]:
    """Return the bundled toolkit path from a wheel or source checkout."""
    packaged_toolkit = package_root() / TOOLKIT_DIR_NAME
    if packaged_toolkit.is_dir():
        return packaged_toolkit

    for parent in package_root().parents:
        candidate = parent / TOOLKIT_DIR_NAME
        if candidate.is_dir():
            return candidate
    return None


def copy_tree_contents(source_dir: Path, destination_dir: Path) -> None:
    """Merge-copy all files and subdirectories from one directory to another."""
    destination_dir.mkdir(parents=True, exist_ok=True)
    for source_path in source_dir.iterdir():
        destination_path = destination_dir / source_path.name
        if source_path.is_dir():
            shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
        else:
            shutil.copy2(source_path, destination_path)


def install_toolkit(toolkit_target: Path) -> Path:
    """Install or update the MRM toolkit in a per-user directory.

    Existing files with the same names are overwritten, but the target directory
    is not deleted so user-local additions under ``~/.mrm-toolkit`` are kept.

    Args:
        toolkit_target: Directory that should contain the toolkit files.

    Returns:
        The resolved toolkit directory path.
    """
    source_dir = bundled_toolkit_dir()
    if source_dir is None:
        raise FileNotFoundError("Bundled mrm-toolkit directory was not found in the package or source checkout.")

    destination_dir = toolkit_target.expanduser().resolve()
    copy_tree_contents(source_dir, destination_dir)
    return destination_dir


def install_skill(target_dir: Path, skill_name: str = DEFAULT_SKILL_NAME, overwrite: bool = False) -> Path:
    """Copy the bundled ``SKILL.md`` to ``target_dir / skill_name``.

    Toolkit reference files are installed separately to ``~/.mrm-toolkit`` (or
    ``MRM_TOOLKIT_HOME`` / ``--toolkit-target``), so the Codex skill directory
    stays small and only needs the prompt file.

    Args:
        target_dir: Parent directory that contains Codex skills.
        skill_name: Destination folder name for the skill.
        overwrite: Replace an existing destination skill directory when true.

    Returns:
        The installed SKILL.md path.
    """
    source_file = bundled_skill_file()
    destination_dir = target_dir.expanduser().resolve() / skill_name
    destination = destination_dir / "SKILL.md"

    if not source_file.is_file():
        raise FileNotFoundError(
            f"Bundled skill file was not found: {source_file}\n"
            "Make sure the mrm-toolkit directory is present alongside the package."
        )

    if destination_dir.exists() and overwrite:
        shutil.rmtree(destination_dir)
    elif destination.exists():
        raise FileExistsError(
            f"Skill already exists at {destination}; pass --overwrite to replace it."
        )

    destination_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_file, destination)
    return destination


def install(
    target_dir: Path,
    toolkit_target: Path,
    skill_name: str = DEFAULT_SKILL_NAME,
    overwrite: bool = False,
) -> Tuple[Path, Path]:
    """Install the Codex skill prompt and the per-user MRM toolkit."""
    skill_path = install_skill(target_dir, skill_name=skill_name, overwrite=overwrite)
    toolkit_path = install_toolkit(toolkit_target)
    return skill_path, toolkit_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install the ModularResearchDocWriter Codex skill and per-user MRM toolkit."
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=default_skills_dir(),
        help="Parent skills directory. Defaults to $CODEX_HOME/skills or ~/.codex/skills.",
    )
    parser.add_argument(
        "--toolkit-target",
        type=Path,
        default=default_toolkit_dir(),
        help="MRM toolkit directory. Defaults to $MRM_TOOLKIT_HOME or ~/.mrm-toolkit.",
    )
    parser.add_argument(
        "--name",
        default=DEFAULT_SKILL_NAME,
        help=f"Destination skill folder name. Defaults to {DEFAULT_SKILL_NAME}.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite an existing skill directory at the destination.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    skill_path, toolkit_path = install(
        args.target,
        args.toolkit_target,
        skill_name=args.name,
        overwrite=args.overwrite,
    )
    print(f"Installed ModularResearchDocWriter skill: {skill_path}")
    print(f"Installed MRM toolkit: {toolkit_path}")


if __name__ == "__main__":
    main()
