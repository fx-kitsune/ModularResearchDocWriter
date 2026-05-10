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

def main():
    parser = argparse.ArgumentParser(description="MRM Toolkit — Unified CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Validate
    val_parser = subparsers.add_parser("validate", help="Validate MRM files or directory")
    val_parser.add_argument("path", type=Path, help="Path to file or directory to validate")
    val_parser.add_argument("--quiet", action="store_true", help="Minimize output")

    # Install Skill
    ins_parser = subparsers.add_parser("install-skill", help="Install Codex skill and toolkit")
    ins_parser.add_argument("--target", type=Path, default=default_skills_dir(), help="Parent skills directory")
    ins_parser.add_argument("--toolkit-target", type=Path, default=default_toolkit_dir(), help="MRM toolkit directory")
    ins_parser.add_argument("--name", default=DEFAULT_SKILL_NAME, help="Skill folder name")
    ins_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing skill")

    # Install Adapter
    adp_parser = subparsers.add_parser("install-adapter", help="Install agent adapter")
    adp_parser.add_argument("adapter", choices=sorted(ADAPTER_TARGETS), help="Target adapter")
    adp_parser.add_argument("project_root", type=Path, help="Project root directory")
    adp_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing adapter")

    # Assemble
    asm_parser = subparsers.add_parser("assemble", help="Assemble modules into a report")
    asm_parser.add_argument("input_dir", type=Path, help="Directory containing modules")
    asm_parser.add_argument("output_path", type=Path, help="Path to final report")

    # Generate Index
    idx_parser = subparsers.add_parser("generate-index", help="Generate index.md for modules")
    idx_parser.add_argument("directory", type=Path, help="Directory to index")
    idx_parser.add_argument("--output", type=Path, help="Optional output path")

    args = parser.parse_args()

    if args.command == "validate":
        sys.exit(_cmd_validate(args))
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
