"""MRM Validator — validates files and directories according to MRM standards.

Dependency-free: avoids external libraries to run in restricted agent environments.
"""

from __future__ import annotations

import logging
import os
import re
from typing import Dict, List, Optional, Tuple

from .models import ValidationResult

logger = logging.getLogger(__name__)


class MRMValidator:
    """MRM standard validator for Markdown files."""

    MAX_LINES = 300
    REQUIRED_FRONTMATTER_FIELDS = ["id", "title", "status", "tags", "summary", "ai_context"]
    VALID_STATUSES = ["draft", "review", "final", "auto-generated"]

    def __init__(self, verbose: bool = True) -> None:
        self.verbose = verbose
        if verbose:
            logging.basicConfig(level=logging.INFO, format="%(message)s")

    # ------------------------------------------------------------------
    # Frontmatter parsing
    # ------------------------------------------------------------------

    def parse_frontmatter_block(self, block: str) -> Optional[Dict]:
        """Parse the small YAML-frontmatter subset used by MRM.

        Supports scalar strings, inline lists (``tags: [a, b]``), block lists,
        and empty values.
        """
        data: Dict[str, object] = {}
        current_key: Optional[str] = None

        for raw_line in block.splitlines():
            line = raw_line.rstrip()
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            # Block list item
            if stripped.startswith("- ") and current_key:
                if current_key not in data or not isinstance(data[current_key], list):
                    data[current_key] = []
                data[current_key].append(stripped[2:].strip().strip("\"'"))
                continue

            if ":" not in line:
                logger.warning(f"Ignoring invalid frontmatter line: {line}")
                continue

            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key

            if value == "":
                data[key] = ""
            elif value.startswith("[") and value.endswith("]"):
                items = value[1:-1].strip()
                data[key] = (
                    []
                    if not items
                    else [item.strip().strip("\"'") for item in items.split(",")]
                )
            elif (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                data[key] = value[1:-1]
            else:
                data[key] = value

        return data if data else None

    def extract_frontmatter(self, content: str) -> Tuple[Optional[Dict], str]:
        """Separate YAML frontmatter from Markdown body.

        Returns:
            (frontmatter_dict | None, body_str)
        """
        pattern = r"^---\n(.*?)\n---\n(.*)"
        match = re.match(pattern, content, re.DOTALL)
        if not match:
            return None, content
        frontmatter = self.parse_frontmatter_block(match.group(1))
        body = match.group(2)
        return frontmatter, body

    # ------------------------------------------------------------------
    # Content metrics
    # ------------------------------------------------------------------

    def count_content_lines(self, content: str) -> int:
        """Count content lines (excluding frontmatter, comments, excessive blank lines)."""
        _, body = self.extract_frontmatter(content)
        lines = body.split("\n")
        content_lines: List[str] = []
        empty_count = 0

        for line in lines:
            if line.strip().startswith("<!--") or line.strip().endswith("-->"):
                continue
            if line.strip() == "":
                empty_count += 1
                if empty_count <= 2:  # Allow max 2 consecutive blank lines
                    content_lines.append(line)
            else:
                empty_count = 0
                content_lines.append(line)

        return len(content_lines)

    # ------------------------------------------------------------------
    # Individual checks
    # ------------------------------------------------------------------

    def validate_frontmatter(
        self, frontmatter: Optional[Dict]
    ) -> Tuple[bool, List[str], List[str]]:
        """Check frontmatter for required fields and valid values."""
        errors: List[str] = []
        warnings: List[str] = []

        if frontmatter is None:
            errors.append("❌ Missing YAML frontmatter")
            return False, errors, warnings

        for field in self.REQUIRED_FRONTMATTER_FIELDS:
            if field not in frontmatter:
                errors.append(f"❌ Missing required field: {field}")

        if "status" in frontmatter and frontmatter["status"] not in self.VALID_STATUSES:
            errors.append(
                f"❌ Invalid status '{frontmatter['status']}'."
                f" Expected one of: {self.VALID_STATUSES}"
            )

        if "summary" in frontmatter:
            summary_sentences = frontmatter["summary"].split(".")
            if len([s for s in summary_sentences if s.strip()]) > 2:
                warnings.append(
                    f"⚠️  Summary should be ≤2 sentences (found {len(summary_sentences)})"
                )

        if "ai_context" not in frontmatter:
            errors.append("❌ Missing ai_context — required for AI-Native Boundary")
        elif len(frontmatter.get("ai_context", "").strip()) < 10:
            warnings.append("⚠️  ai_context is too short; describe the downstream task clearly")

        if "tags" in frontmatter:
            if not isinstance(frontmatter["tags"], list):
                errors.append("❌ Tags must be a list")
            elif len(frontmatter["tags"]) == 0:
                warnings.append("⚠️  Should have at least one tag")

        return len(errors) == 0, errors, warnings

    def check_tldr(self, content: str) -> Tuple[bool, List[str], List[str]]:
        """Check for the existence of a TL;DR section."""
        errors: List[str] = []
        warnings: List[str] = []

        tldr_pattern = r"> *\*\*TL;DR\*\*:? *.+"
        if not re.search(tldr_pattern, content, re.IGNORECASE):
            errors.append("❌ Missing TL;DR section (required by Progressive Disclosure)")
            return False, errors, warnings

        tldr_matches = re.findall(r"> *\*\*TL;DR\*\*:? *(.+)", content, re.IGNORECASE)
        if tldr_matches:
            tldr_text = tldr_matches[0]
            if "\n" in tldr_text or len(tldr_text.split(".")) > 2:
                warnings.append("⚠️  TL;DR should be concise (max 1-2 sentences)")

        return len(errors) == 0, errors, warnings

    def check_cross_references(
        self, content: str, directory: str
    ) -> Tuple[bool, List[str], List[str]]:
        """Verify cross-references point to existing files."""
        errors: List[str] = []
        warnings: List[str] = []

        wikilink_pattern = r"\[\[(.+?)\]\]"
        wikilinks = re.findall(wikilink_pattern, content)

        mdlink_pattern = r"\[([^\]]+)\]\((\.?/?[^\)]+\.(md|MD))\)"
        mdlinks = re.findall(mdlink_pattern, content)

        # Wikilinks — warnings only as they might be placeholders
        placeholder_ids = {
            "id", "id-file-goc", "id-lien-quan", "id-lien-quan-1", "id-lien-quan-2"
        }
        for link_id in wikilinks:
            if link_id in placeholder_ids:
                continue

            found = False
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith(".md"):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, "r", encoding="utf-8") as fh:
                                file_content = fh.read()
                            fm, _ = self.extract_frontmatter(file_content)
                            if fm and fm.get("id") == link_id:
                                found = True
                                break
                        except Exception:
                            pass
                if found:
                    break

            if not found:
                context_pattern = rf"\[\[{link_id}\]\].*\(sẽ tạo|placeholder|future|tương lai\)"
                if re.search(context_pattern, content, re.IGNORECASE):
                    continue
                warnings.append(
                    f"⚠️  Wikilink [[{link_id}]] target not found (might be a placeholder)"
                )

        # Markdown links — broken links are actual errors
        for _link_text, link_path, _ in mdlinks:
            abs_path = os.path.abspath(os.path.join(directory, link_path))
            if not os.path.exists(abs_path):
                errors.append(f"❌ Broken link: [{_link_text}]({link_path})")

        return len(errors) == 0, errors, warnings

    def check_heading_structure(self, content: str) -> Tuple[bool, List[str]]:
        """Check heading hierarchy and integrity."""
        errors: List[str] = []
        _, body = self.extract_frontmatter(content)
        lines = body.split("\n")
        prev_level = 0
        in_code_fence = False

        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_code_fence = not in_code_fence
                continue
            if in_code_fence:
                continue

            heading_match = re.match(r"^(#{1,6})\s*(.*)", line)
            if heading_match:
                level = len(heading_match.group(1))
                text = heading_match.group(2).strip()
                if not text:
                    errors.append(f"❌ Empty heading at line {i + 1}")
                if level > prev_level + 1 and prev_level > 0:
                    errors.append(
                        f"⚠️  Heading jump from H{prev_level} to H{level} at line {i + 1}"
                    )
                prev_level = level

        return len(errors) == 0, errors

    # ------------------------------------------------------------------
    # File & directory validation
    # ------------------------------------------------------------------

    def validate_file(self, file_path: str, check_links: bool = False) -> ValidationResult:
        """Validate a single MRM file."""
        errors: List[str] = []
        warnings: List[str] = []

        try:
            with open(file_path, "r", encoding="utf-8") as fh:
                content = fh.read()
        except Exception as exc:
            return ValidationResult(
                file_path=file_path,
                is_valid=False,
                errors=[f"❌ Cannot read file: {exc}"],
                warnings=[],
                line_count=0,
                has_frontmatter=False,
                has_ai_context=False,
                frontmatter=None,
            )

        frontmatter, _ = self.extract_frontmatter(content)
        has_frontmatter = frontmatter is not None
        has_ai_context = has_frontmatter and "ai_context" in frontmatter

        fm_valid, fm_errors, fm_warnings = self.validate_frontmatter(frontmatter)
        errors.extend(fm_errors)
        warnings.extend(fm_warnings)

        line_count = self.count_content_lines(content)
        if line_count > self.MAX_LINES:
            errors.append(
                f"❌ Content exceeds limit ({line_count}/{self.MAX_LINES}). Split the file."
            )

        _tldr_valid, tldr_errors, tldr_warnings = self.check_tldr(content)
        errors.extend(tldr_errors)
        warnings.extend(tldr_warnings)

        _heading_valid, heading_errors = self.check_heading_structure(content)
        errors.extend(heading_errors)

        if check_links:
            directory = os.path.dirname(file_path) or "."
            _link_valid, link_errors, link_warnings = self.check_cross_references(
                content, directory
            )
            errors.extend(link_errors)
            warnings.extend(link_warnings)

        return ValidationResult(
            file_path=file_path,
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            line_count=line_count,
            has_frontmatter=has_frontmatter,
            has_ai_context=has_ai_context,
            frontmatter=frontmatter,
        )

    def validate_directory(self, directory: str) -> List[ValidationResult]:
        """Validate all .md files in a directory."""
        results: List[ValidationResult] = []

        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "outputs"]
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    results.append(self.validate_file(file_path, check_links=True))

        return results

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def print_report(self, results: List[ValidationResult]) -> None:
        """Print validation report (Vietnamese output for CLI users)."""
        total = len(results)
        valid = sum(1 for r in results if r.is_valid)
        invalid = total - valid

        print("\n" + "=" * 60)
        print("📊 BÁO CÁO KIỂM ĐỊNH MRM")
        print("=" * 60)
        print(f"Tổng số file: {total}")
        print(f"✅ Hợp lệ: {valid}")
        print(f"❌ Không hợp lệ: {invalid}")
        print(f"Tỷ lệ đạt: {valid / total * 100:.1f}%" if total else "Tỷ lệ đạt: N/A")
        print("=" * 60)

        error_files = [r for r in results if not r.is_valid]
        if error_files:
            print("\n🔴 FILE CÓ LỖI:")
            for result in error_files:
                print(f"\n📄 {result.file_path}")
                print(f"   Dòng nội dung: {result.line_count}")
                print(f"   Có frontmatter: {'✅' if result.has_frontmatter else '❌'}")
                print(f"   Có ai_context: {'✅' if result.has_ai_context else '❌'}")
                if result.errors:
                    print("   Lỗi:")
                    for err in result.errors:
                        print(f"     - {err}")
                if result.warnings:
                    print("   Cảnh báo:")
                    for warn in result.warnings:
                        print(f"     - {warn}")

        valid_files = [r for r in results if r.is_valid]
        if valid_files:
            print(f"\n✅ FILE HỢP LỆ ({len(valid_files)}):")
            for result in valid_files:
                print(f"   ✓ {result.file_path} ({result.line_count} dòng)")

        print("\n" + "=" * 60)
