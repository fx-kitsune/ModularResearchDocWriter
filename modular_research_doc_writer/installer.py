"""Install the bundled ModularResearchDocWriter skill into a Codex skills folder."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path

DEFAULT_SKILL_NAME = "modular-research-doc-writer"


def default_skills_dir() -> Path:
    """Return the default Codex skills directory for the current user."""
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "skills"
    return Path.home() / ".codex" / "skills"


def bundled_skill_file() -> Path:
    """Return the filesystem path to the bundled SKILL.md file."""
    return Path(__file__).resolve().parent / "skills" / DEFAULT_SKILL_NAME / "SKILL.md"


def install_skill(target_dir: Path, skill_name: str = DEFAULT_SKILL_NAME, overwrite: bool = False) -> Path:
    """Copy the bundled skill to ``target_dir / skill_name / SKILL.md``.

    Args:
        target_dir: Parent directory that contains Codex skills.
        skill_name: Destination folder name for the skill.
        overwrite: Replace an existing destination SKILL.md when true.

    Returns:
        The installed SKILL.md path.
    """
    source = bundled_skill_file()
    destination_dir = target_dir.expanduser().resolve() / skill_name
    destination = destination_dir / "SKILL.md"

    if destination.exists() and not overwrite:
        raise FileExistsError(f"Skill already exists at {destination}; pass --overwrite to replace it.")

    destination_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    return destination


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install the ModularResearchDocWriter Codex skill from the pip package."
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=default_skills_dir(),
        help="Parent skills directory. Defaults to $CODEX_HOME/skills or ~/.codex/skills.",
    )
    parser.add_argument(
        "--name",
        default=DEFAULT_SKILL_NAME,
        help=f"Destination skill folder name. Defaults to {DEFAULT_SKILL_NAME}.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite an existing SKILL.md at the destination.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    destination = install_skill(args.target, skill_name=args.name, overwrite=args.overwrite)
    print(f"Installed ModularResearchDocWriter skill: {destination}")


if __name__ == "__main__":
    main()
