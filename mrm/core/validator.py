"""MRM Validator — kiểm định từng file và thư mục theo chuẩn MRM.

Dependency-free: không yêu cầu thư viện ngoài, chạy được trong mọi môi trường
agent kể cả khi PyYAML chưa được cài.
"""

from __future__ import annotations

import os
import re
from typing import Dict, List, Optional, Tuple

from .models import ValidationResult


class MRMValidator:
    """Bộ kiểm định chuẩn MRM cho file Markdown."""

    MAX_LINES = 300
    REQUIRED_FRONTMATTER_FIELDS = ["id", "title", "status", "tags", "summary", "ai_context"]
    VALID_STATUSES = ["draft", "review", "final", "auto-generated"]

    def __init__(self, verbose: bool = True) -> None:
        self.verbose = verbose

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    def log(self, message: str) -> None:
        if self.verbose:
            print(message)

    # ------------------------------------------------------------------
    # Frontmatter parsing
    # ------------------------------------------------------------------

    def parse_frontmatter_block(self, block: str) -> Optional[Dict]:
        """Parse the small YAML-frontmatter subset used by MRM.

        Supports scalar strings, inline lists (``tags: [a, b]``), block lists,
        and empty values.  Kept dependency-free for agent workspaces where
        PyYAML is not installed.
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
                self.log(f"⚠️  Bỏ qua dòng frontmatter không hợp lệ: {line}")
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
        """Tách YAML frontmatter khỏi nội dung Markdown.

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
        """Đếm số dòng nội dung (không tính frontmatter, comment, dòng trống liên tiếp)."""
        _, body = self.extract_frontmatter(content)
        lines = body.split("\n")
        content_lines: List[str] = []
        empty_count = 0

        for line in lines:
            if line.strip().startswith("<!--") or line.strip().endswith("-->"):
                continue
            if line.strip() == "":
                empty_count += 1
                if empty_count <= 2:  # Cho phép tối đa 2 dòng trống liên tiếp
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
        """Kiểm tra frontmatter có đủ trường bắt buộc và giá trị hợp lệ.

        Returns:
            (is_valid, errors, warnings)
        """
        errors: List[str] = []
        warnings: List[str] = []

        if frontmatter is None:
            errors.append("❌ Thiếu YAML frontmatter")
            return False, errors, warnings

        for field in self.REQUIRED_FRONTMATTER_FIELDS:
            if field not in frontmatter:
                errors.append(f"❌ Thiếu trường bắt buộc: {field}")

        if "status" in frontmatter and frontmatter["status"] not in self.VALID_STATUSES:
            errors.append(
                f"❌ Status '{frontmatter['status']}' không hợp lệ."
                f" Chỉ chấp nhận: {self.VALID_STATUSES}"
            )

        if "summary" in frontmatter:
            summary_sentences = frontmatter["summary"].split(".")
            if len([s for s in summary_sentences if s.strip()]) > 2:
                warnings.append(
                    f"⚠️  Summary nên ≤2 câu (hiện tại: {len(summary_sentences)} câu)"
                )

        if "ai_context" not in frontmatter:
            errors.append("❌ Thiếu trường ai_context — bắt buộc cho AI-Native Boundary")
        elif len(frontmatter.get("ai_context", "").strip()) < 10:
            warnings.append("⚠️  ai_context quá ngắn, nên mô tả rõ task downstream")

        if "tags" in frontmatter:
            if not isinstance(frontmatter["tags"], list):
                errors.append("❌ Tags phải là danh sách (list)")
            elif len(frontmatter["tags"]) == 0:
                warnings.append("⚠️  Nên có ít nhất 1 tag")

        return len(errors) == 0, errors, warnings

    def check_tldr(self, content: str) -> Tuple[bool, List[str], List[str]]:
        """Kiểm tra sự tồn tại của TL;DR section.

        Returns:
            (is_valid, errors, warnings)
        """
        errors: List[str] = []
        warnings: List[str] = []

        tldr_pattern = r"> *\*\*TL;DR\*\*:? *.+"
        if not re.search(tldr_pattern, content, re.IGNORECASE):
            errors.append("❌ Thiếu section TL;DR (bắt buộc theo Progressive Disclosure)")
            return False, errors, warnings

        tldr_matches = re.findall(r"> *\*\*TL;DR\*\*:? *(.+)", content, re.IGNORECASE)
        if tldr_matches:
            tldr_text = tldr_matches[0]
            if "\n" in tldr_text or len(tldr_text.split(".")) > 2:
                warnings.append("⚠️  TL;DR nên ngắn gọn, tối đa 1-2 câu")

        return len(errors) == 0, errors, warnings

    def check_cross_references(
        self, content: str, directory: str
    ) -> Tuple[bool, List[str], List[str]]:
        """Kiểm tra cross-references trỏ đến file tồn tại.

        Returns:
            (is_valid, errors, warnings)  — errors và warnings được tách riêng.
        """
        errors: List[str] = []
        warnings: List[str] = []

        wikilink_pattern = r"\[\[(.+?)\]\]"
        wikilinks = re.findall(wikilink_pattern, content)

        mdlink_pattern = r"\[([^\]]+)\]\((\.?/?[^\)]+\.(md|MD))\)"
        mdlinks = re.findall(mdlink_pattern, content)

        # Wikilinks — chỉ warning vì có thể là placeholder hợp lệ
        placeholder_ids = {
            "id", "id-file-goc", "id-lien-quan", "id-lien-quan-1", "id-lien-quan-2"
        }
        for link_id in wikilinks:
            if link_id in placeholder_ids:
                continue

            found = False
            for root, dirs, files in os.walk(directory):
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
                context_pattern = rf"\[\[{link_id}\]\].*\(sẽ tạo|placeholder|tương lai\)"
                if re.search(context_pattern, content, re.IGNORECASE):
                    continue
                warnings.append(
                    f"⚠️  Wikilink [[{link_id}]] không tìm thấy file đích"
                    f" (có thể là placeholder)"
                )

        # Markdown links — broken link là error thực sự
        for _link_text, link_path, _ in mdlinks:
            abs_path = os.path.abspath(os.path.join(directory, link_path))
            if not os.path.exists(abs_path):
                errors.append(f"❌ Broken link: [{_link_text}]({link_path})")

        return len(errors) == 0, errors, warnings

    def check_heading_structure(self, content: str) -> Tuple[bool, List[str]]:
        """Kiểm tra cấu trúc heading không bị lỗi.

        Bỏ qua các dòng nằm trong fenced code block (``` ... ```).
        """
        errors: List[str] = []
        _, body = self.extract_frontmatter(content)
        lines = body.split("\n")
        prev_level = 0
        in_code_fence = False

        for i, line in enumerate(lines):
            # Toggle code fence state
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
                    errors.append(f"❌ Heading rỗng ở dòng {i + 1}")
                if level > prev_level + 1 and prev_level > 0:
                    errors.append(
                        f"⚠️  Nhảy cấp heading từ H{prev_level} lên H{level} ở dòng {i + 1}"
                    )
                prev_level = level

        return len(errors) == 0, errors

    # ------------------------------------------------------------------
    # File & directory validation
    # ------------------------------------------------------------------

    def validate_file(self, file_path: str, check_links: bool = False) -> ValidationResult:
        """Kiểm định một file MRM đơn lẻ."""
        errors: List[str] = []
        warnings: List[str] = []

        try:
            with open(file_path, "r", encoding="utf-8") as fh:
                content = fh.read()
        except Exception as exc:
            return ValidationResult(
                file_path=file_path,
                is_valid=False,
                errors=[f"❌ Không đọc được file: {exc}"],
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
                f"❌ Vượt quá số dòng tối đa ({line_count}/{self.MAX_LINES})."
                f" Cần tách file."
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
        """Kiểm định tất cả file .md trong thư mục."""
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
        """In báo cáo kiểm định."""
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
