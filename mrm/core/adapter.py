"""MRM Adapter Installer — cài file hướng dẫn agent vào thư mục dự án.

ADAPTER_TARGETS phải đồng bộ với ``mrm-toolkit/manifest.yaml`` section ``adapters``.
Khi thêm adapter mới vào manifest.yaml, hãy cập nhật dict này cùng lúc.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Dict, Optional, Tuple

# ---------------------------------------------------------------------------
# Sync note: keys và paths dưới đây tương ứng trực tiếp với manifest.yaml:
#
#   adapters:
#     <key>:
#       file: <source_rel>          ← cột 0 trong tuple
#       install_target: <target_rel> ← cột 1 trong tuple
#
# Khi thêm / đổi tên adapter trong manifest.yaml, cập nhật dict này cùng lúc.
# ---------------------------------------------------------------------------
ADAPTER_TARGETS: Dict[str, Tuple[str, str]] = {
    # key               (source rel to repo root,                          install target rel to project root)
    "codex":            ("mrm-toolkit/adapters/codex/AGENTS.md",           "AGENTS.md"),
    "claude":           ("mrm-toolkit/adapters/claude/CLAUDE.md",          "CLAUDE.md"),
    "claude_code":      ("mrm-toolkit/adapters/claude/CLAUDE.md",          "CLAUDE.md"),
    "gemini":           ("mrm-toolkit/adapters/gemini/GEMINI.md",          "GEMINI.md"),
    "copilot":          ("mrm-toolkit/adapters/copilot/copilot-instructions.md",
                         ".github/copilot-instructions.md"),
    "cursor":           ("mrm-toolkit/adapters/cursor/mrm.mdc",            ".cursor/rules/mrm.mdc"),
    "agent_ide":        ("mrm-toolkit/adapters/agent-ide/AGENT-RULES.md",  ".agent/rules/mrm.md"),
}


def find_toolkit_root(start: Optional[Path] = None) -> Path:
    """Tìm mrm-toolkit root từ script hiện tại hoặc working directory.

    Thứ tự kiểm tra:
    1. ``start`` (nếu được truyền)
    2. Thư mục cha của file này (``scripts/mrm/``) → lên 2 cấp → ``mrm-toolkit/``
    3. ``<cwd>/mrm-toolkit``
    4. ``cwd``

    Raises:
        FileNotFoundError: Nếu không tìm thấy mrm-toolkit root hợp lệ.
    """
    candidates = []
    if start:
        candidates.append(start.resolve())

    # __file__ là mrm-toolkit/scripts/mrm/adapter.py → parent.parent.parent = mrm-toolkit/
    candidates.append(Path(__file__).resolve().parent.parent.parent)
    candidates.append(Path.cwd() / "mrm-toolkit")
    candidates.append(Path.cwd())

    for candidate in candidates:
        if (candidate / "manifest.yaml").exists() and (candidate / "adapters").exists():
            return candidate

    raise FileNotFoundError(
        "Không tìm thấy mrm-toolkit root chứa manifest.yaml và adapters/"
    )


def install_adapter(
    adapter: str, project_root: str, overwrite: bool = False
) -> Path:
    """Cài file hướng dẫn agent vào thư mục dự án.

    Args:
        adapter: Tên adapter (xem ADAPTER_TARGETS).
        project_root: Thư mục gốc của dự án đích.
        overwrite: Ghi đè file đích nếu đã tồn tại.

    Returns:
        Đường dẫn tuyệt đối của file đích đã cài.

    Raises:
        ValueError: Tên adapter không hợp lệ.
        FileNotFoundError: Adapter source không tồn tại.
        FileExistsError: File đích đã tồn tại và ``overwrite=False``.
    """
    adapter_key = adapter.strip().lower().replace("-", "_")
    if adapter_key not in ADAPTER_TARGETS:
        available = ", ".join(sorted(ADAPTER_TARGETS))
        raise ValueError(
            f"Adapter không hợp lệ: {adapter}. Các adapter hỗ trợ: {available}"
        )

    toolkit_root = find_toolkit_root()
    source_rel, target_rel = ADAPTER_TARGETS[adapter_key]
    source = toolkit_root.parent / source_rel
    target = Path(project_root).resolve() / target_rel

    if not source.exists():
        raise FileNotFoundError(f"Không tìm thấy adapter source: {source}")
    if target.exists() and not overwrite:
        raise FileExistsError(
            f"File đích đã tồn tại: {target}. Thêm --overwrite để ghi đè."
        )

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return target
