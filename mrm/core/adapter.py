"""MRM Adapter Installer — installs agent instructions into project directories."""

from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import Dict, Tuple

from ..installer import bundled_toolkit_dir

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Sync note: keys and paths below correspond to manifest.yaml:
#
#   adapters:
#     <key>:
#       file: <source_rel>          ← first column in tuple
#       install_target: <target_rel> ← second column in tuple
# ---------------------------------------------------------------------------
ADAPTER_TARGETS: Dict[str, Tuple[str, str]] = {
    # key               (source rel to toolkit root,                       install target rel to project root)
    "codex":            ("adapters/codex/AGENTS.md",           "AGENTS.md"),
    "claude":           ("adapters/claude/CLAUDE.md",          "CLAUDE.md"),
    "claude_code":      ("adapters/claude/CLAUDE.md",          "CLAUDE.md"),
    "gemini":           ("adapters/gemini/GEMINI.md",          "GEMINI.md"),
    "copilot":          ("adapters/copilot/copilot-instructions.md",
                         ".github/copilot-instructions.md"),
    "cursor":           ("adapters/cursor/mrm.mdc",            ".cursor/rules/mrm.mdc"),
    "agent_ide":        ("adapters/agent-ide/AGENT-RULES.md",  ".agent/rules/mrm.md"),
}


def install_adapter(
    adapter: str, project_root: str, overwrite: bool = False
) -> Path:
    """Install agent instruction files into a project directory.

    Args:
        adapter: Adapter name (see ADAPTER_TARGETS).
        project_root: Target project root directory.
        overwrite: Overwrite destination if it exists.

    Returns:
        Absolute path to the installed file.
    """
    adapter_key = adapter.strip().lower().replace("-", "_")
    if adapter_key not in ADAPTER_TARGETS:
        available = ", ".join(sorted(ADAPTER_TARGETS))
        raise ValueError(
            f"Invalid adapter: {adapter}. Supported adapters: {available}"
        )

    toolkit_root = bundled_toolkit_dir()
    if toolkit_root is None:
        raise FileNotFoundError("Could not find MRM toolkit resources.")

    source_rel, target_rel = ADAPTER_TARGETS[adapter_key]
    source = toolkit_root / source_rel
    target = Path(project_root).resolve() / target_rel

    if not source.exists():
        raise FileNotFoundError(f"Adapter source not found: {source}")
    if target.exists() and not overwrite:
        raise FileExistsError(
            f"Target already exists: {target}. Use --overwrite to replace."
        )

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return target
