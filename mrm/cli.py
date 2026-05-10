"""Unified CLI entry point for MRM Toolkit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

from .core.adapter import ADAPTER_TARGETS, install_adapter
from .core.assembler import assemble_report
from .core.indexer import generate_index
from .core.validator import MRMValidator
from .installer import install, default_skills_dir, default_toolkit_dir, DEFAULT_SKILL_NAME

def _cmd_validate(args):
    validator = MRMValidator(verbose=not args.quiet)
    if args.path.is_file():
        result = validator.validate_file(str(args.path), check_links=True)
        print(f"\n📄 {result.file_path}")
        print(f"Dòng nội dung: {result.line_count}")
        print(f"Có frontmatter: {'✅' if result.has_frontmatter else '❌'}")
        print(f"Có ai_context: {'✅' if result.has_ai_context else '❌'}")
        if result.errors:
            print("\nLỗi:")
            for err in result.errors:
                print(f"  - {err}")
        return 0 if result.is_valid else 1
    else:
        results = validator.validate_directory(str(args.path))
        validator.print_report(results)
        return 0 if all(r.is_valid for r in results) else 1

def _cmd_install_skill(args):
    try:
        skill_path, toolkit_path = install(
            args.target,
            args.toolkit_target,
            skill_name=args.name,
            overwrite=args.overwrite,
        )
        print(f"✅ Installed ModularResearchDocWriter skill: {skill_path}")
        print(f"✅ Installed MRM toolkit: {toolkit_path}")
        return 0
    except Exception as e:
        print(f"❌ Error during installation: {e}")
        return 1

def _cmd_install_adapter(args):
    try:
        target = install_adapter(args.adapter, str(args.project_root), overwrite=args.overwrite)
        print(f"✅ Đã cài adapter {args.adapter}: {target}")
        return 0
    except Exception as exc:
        print(f"❌ Không cài được adapter: {exc}")
        return 1

def _cmd_assemble(args):
    try:
        assemble_report(str(args.input_dir), str(args.output_path))
        print(f"✅ Đã ghép báo cáo tại: {args.output_path}")
        return 0
    except Exception as e:
        print(f"❌ Lỗi khi ghép báo cáo: {e}")
        return 1

def _cmd_generate_index(args):
    try:
        generate_index(str(args.directory), str(args.output) if args.output else None)
        print(f"✅ Đã sinh index tại thư mục: {args.directory}")
        return 0
    except Exception as e:
        print(f"❌ Lỗi khi sinh index: {e}")
        return 1

def _cmd_count_lines(args):
    validator = MRMValidator(verbose=not args.quiet)
    try:
        if not args.path.is_file():
            print(f"❌ Đường dẫn không phải là file: {args.path}")
            return 1
        with open(args.path, "r", encoding="utf-8") as fh:
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

def main():
    # Fix for Windows terminal encoding issues with emojis
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (AttributeError, TypeError):
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8")
        except (AttributeError, TypeError):
            pass

    parser = argparse.ArgumentParser(description="MRM Toolkit — Unified CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Validate
    val_parser = subparsers.add_parser("validate", help="Kiểm định file hoặc thư mục MRM")
    val_parser.add_argument("path", type=Path, help="Đường dẫn file hoặc thư mục")
    val_parser.add_argument("--quiet", action="store_true", help="Giảm thiểu output")

    # Count Lines
    cnt_parser = subparsers.add_parser("count-lines", help="Đếm số dòng nội dung của file")
    cnt_parser.add_argument("path", type=Path, help="Đường dẫn file .md")
    cnt_parser.add_argument("--quiet", action="store_true", help="Giảm thiểu output")

    # Install Skill
    ins_parser = subparsers.add_parser("install-skill", help="Cài đặt Codex skill và toolkit")
    ins_parser.add_argument("--target", type=Path, default=default_skills_dir(), help="Thư mục cha của skills")
    ins_parser.add_argument("--toolkit-target", type=Path, default=default_toolkit_dir(), help="Thư mục cài toolkit")
    ins_parser.add_argument("--name", default=DEFAULT_SKILL_NAME, help="Tên thư mục skill")
    ins_parser.add_argument("--overwrite", action="store_true", help="Ghi đè nếu đã tồn tại")

    # Install Adapter
    adp_parser = subparsers.add_parser("install-adapter", help="Cài đặt agent adapter")
    adp_parser.add_argument("adapter", choices=sorted(ADAPTER_TARGETS), help="Loại adapter")
    adp_parser.add_argument("project_root", type=Path, help="Thư mục gốc của project")
    adp_parser.add_argument("--overwrite", action="store_true", help="Ghi đè nếu đã tồn tại")

    # Assemble
    asm_parser = subparsers.add_parser("assemble", help="Ghép các module thành báo cáo hoàn chỉnh")
    asm_parser.add_argument("input_dir", type=Path, help="Thư mục chứa các module")
    asm_parser.add_argument("output_path", type=Path, help="Đường dẫn file báo cáo đầu ra")

    # Generate Index
    idx_parser = subparsers.add_parser("generate-index", help="Sinh file index.md cho thư mục module")
    idx_parser.add_argument("directory", type=Path, help="Thư mục cần đánh chỉ mục")
    idx_parser.add_argument("--output", type=Path, help="Đường dẫn file đầu ra (tùy chọn)")

    args = parser.parse_args()

    if args.command == "validate":
        sys.exit(_cmd_validate(args))
    elif args.command == "count-lines":
        sys.exit(_cmd_count_lines(args))
    elif args.command == "install-skill":
        sys.exit(_cmd_install_skill(args))
    elif args.command == "install-adapter":
        sys.exit(_cmd_install_adapter(args))
    elif args.command == "assemble":
        sys.exit(_cmd_assemble(args))
    elif args.command == "generate-index":
        sys.exit(_cmd_generate_index(args))
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
