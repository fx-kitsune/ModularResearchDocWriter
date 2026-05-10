#!/usr/bin/env python3
"""MRM Toolkit — entry point.

File này là thin wrapper. Toàn bộ logic nằm trong package mrm/:
  mrm/models.py    — ValidationResult dataclass
  mrm/validator.py — MRMValidator class
  mrm/indexer.py   — generate_index()
  mrm/assembler.py — assemble_report()
  mrm/adapter.py   — install_adapter(), ADAPTER_TARGETS
  mrm/cli.py       — main() CLI với dispatch dict

Usage:
    python mrm_validator.py validate <path>
    python mrm_validator.py validate-file <file.md>
    python mrm_validator.py count-lines <file.md>
    python mrm_validator.py generate-index <directory> [output_path]
    python mrm_validator.py assemble <input_dir> <output_path>
    python mrm_validator.py install-adapter <adapter> <project_root> [--overwrite]
    python mrm_validator.py --help
"""

from __future__ import annotations

import sys
from pathlib import Path

# Đảm bảo stdout/stderr dùng UTF-8 trên Windows (tránh UnicodeEncodeError với emoji)
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]

# Thêm thư mục scripts/ vào sys.path để import package mrm/
sys.path.insert(0, str(Path(__file__).resolve().parent))

from mrm.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
