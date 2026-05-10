"""MRM CLI — entry point cho mrm_validator.py.

Sử dụng dispatch dict thay vì if-elif chain.
"""

from __future__ import annotations

import sys
from typing import Dict, List

from .adapter import ADAPTER_TARGETS, install_adapter
from .assembler import assemble_report
from .indexer import generate_index
from .validator import MRMValidator

# ---------------------------------------------------------------------------
# Docstring dùng cho --help và khi gọi không có argument
# ---------------------------------------------------------------------------
USAGE = """\
MRM Toolkit — Validation & Automation CLI

Các lệnh:
  validate <directory>                          Kiểm định tất cả .md trong thư mục
  validate-file <file.md>                       Kiểm định một file đơn lẻ
  count-lines <file.md>                         Đếm dòng nội dung
  generate-index <directory> [output_path]      Sinh index.md
  assemble <input_dir> <output_path>            Ghép modules thành báo cáo
  install-adapter <adapter> <project_root>      Cài adapter agent
             [--overwrite]

Adapter hợp lệ: {adapters}
"""


def _cmd_validate(args: List[str], validator: MRMValidator) -> int:
    if len(args) < 1:
        print("Usage: mrm_validator.py validate <directory>")
        return 1
    results = validator.validate_directory(args[0])
    validator.print_report(results)
    return 0 if all(r.is_valid for r in results) else 1


def _cmd_validate_file(args: List[str], validator: MRMValidator) -> int:
    if len(args) < 1:
        print("Usage: mrm_validator.py validate-file <file.md>")
        return 1
    result = validator.validate_file(args[0], check_links=True)

    print(f"\n📄 {result.file_path}")
    print(f"Dòng nội dung: {result.line_count}")
    print(f"Có frontmatter: {'✅' if result.has_frontmatter else '❌'}")
    print(f"Có ai_context: {'✅' if result.has_ai_context else '❌'}")

    if result.errors:
        print("\nLỗi:")
        for err in result.errors:
            print(f"  - {err}")
    if result.warnings:
        print("\nCảnh báo:")
        for warn in result.warnings:
            print(f"  - {warn}")

    return 0 if result.is_valid else 1


def _cmd_count_lines(args: List[str], validator: MRMValidator) -> int:
    if len(args) < 1:
        print("Usage: mrm_validator.py count-lines <file.md>")
        return 1
    try:
        with open(args[0], "r", encoding="utf-8") as fh:
            content = fh.read()
        line_count = validator.count_content_lines(content)
        print(f"📊 Số dòng nội dung: {line_count}/{validator.MAX_LINES}")
        if line_count > validator.MAX_LINES:
            print("⚠️  Vượt quá giới hạn! Cần tách file.")
            return 1
        print("✅ Đạt giới hạn dòng.")
        return 0
    except Exception as exc:
        print(f"❌ Lỗi: {exc}")
        return 1


def _cmd_generate_index(args: List[str], _validator: MRMValidator) -> int:
    if len(args) < 1:
        print("Usage: mrm_validator.py generate-index <directory> [output_path]")
        return 1
    output_path = args[1] if len(args) > 1 else None
    generate_index(args[0], output_path)
    return 0


def _cmd_assemble(args: List[str], _validator: MRMValidator) -> int:
    if len(args) < 2:
        print("Usage: mrm_validator.py assemble <input_dir> <output_path>")
        return 1
    assemble_report(args[0], args[1])
    return 0


def _cmd_install_adapter(args: List[str], _validator: MRMValidator) -> int:
    if len(args) < 2:
        print("Usage: mrm_validator.py install-adapter <adapter> <project_root> [--overwrite]")
        print(f"Adapters: {', '.join(sorted(ADAPTER_TARGETS))}")
        return 1
    adapter = args[0]
    project_root = args[1]
    overwrite = "--overwrite" in args[2:]
    try:
        target = install_adapter(adapter, project_root, overwrite=overwrite)
        print(f"✅ Đã cài adapter {adapter}: {target}")
        return 0
    except Exception as exc:
        print(f"❌ Không cài được adapter: {exc}")
        return 1


# Dispatch table: command → handler
_COMMANDS: Dict[str, object] = {
    "validate": _cmd_validate,
    "validate-file": _cmd_validate_file,
    "count-lines": _cmd_count_lines,
    "generate-index": _cmd_generate_index,
    "assemble": _cmd_assemble,
    "install-adapter": _cmd_install_adapter,
}


def main() -> None:
    """CLI entry point."""
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(USAGE.format(adapters=", ".join(sorted(ADAPTER_TARGETS))))
        sys.exit(0 if len(sys.argv) >= 2 else 1)

    command = sys.argv[1]
    handler = _COMMANDS.get(command)

    if handler is None:
        print(f"❌ Command không hợp lệ: {command}")
        print(USAGE.format(adapters=", ".join(sorted(ADAPTER_TARGETS))))
        sys.exit(1)

    validator = MRMValidator()
    exit_code = handler(sys.argv[2:], validator)  # type: ignore[call-arg]
    sys.exit(exit_code)
