"""MRM Indexer — tự động sinh index.md từ cây thư mục MRM.

Sử dụng frontmatter đã cache trong ValidationResult để tránh đọc file lần 2.
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .models import ValidationResult
from .validator import MRMValidator


def generate_index(
    directory: str, output_path: Optional[str] = None
) -> str:
    """Tự động sinh index.md từ cây thư mục MRM.

    Args:
        directory: Thư mục chứa các file MRM.
        output_path: Đường dẫn file output. Mặc định là ``<directory>/index.md``.

    Returns:
        Nội dung index.md đã sinh.
    """
    md_count = len(list(Path(directory).rglob("*.md")))
    index_content = f"""---
id: index
title: "Mục lục Nghiên cứu"
status: auto-generated
tags: [index, navigation]
summary: "Mục lục tự động sinh từ cây thư mục MRM."
ai_context: "Dùng để điều hướng và hiểu cấu trúc tổng thể của dự án nghiên cứu."
---

# Mục lục Nghiên cứu

> **TL;DR**: Tổng quan cấu trúc tài liệu nghiên cứu với {md_count} file.

## Cấu trúc Thư mục

```
"""

    # Directory tree
    tree_lines: List[str] = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        level = root.replace(directory, "").count(os.sep)
        indent = "│   " * level
        tree_lines.append(f"{indent}📁 {os.path.basename(root)}/")
        subindent = "│   " * (level + 1)
        for file in sorted(files):
            if file.endswith(".md"):
                tree_lines.append(f"{subindent}📄 {file}")

    index_content += "\n".join(tree_lines)
    index_content += "\n```\n\n## Danh sách File theo Trạng thái\n\n"

    # Validate để lấy frontmatter (cached trong ValidationResult)
    validator = MRMValidator(verbose=False)
    results = validator.validate_directory(directory)

    status_groups: dict = {"draft": [], "review": [], "final": [], "unknown": []}

    for result in results:
        if "index.md" in result.file_path:
            continue

        # Dùng frontmatter đã cache — không đọc file lần 2
        fm = result.frontmatter
        if fm:
            status = str(fm.get("status", "unknown"))
            title = str(fm.get("title", os.path.basename(result.file_path)))
            file_id = str(fm.get("id", ""))
        else:
            status = "unknown"
            title = os.path.basename(result.file_path)
            file_id = ""

        target_group = status if status in status_groups else "unknown"
        status_groups[target_group].append((title, result.file_path, file_id))

    status_emoji = {"draft": "🟡", "review": "🟠", "final": "✅", "unknown": "⚪"}
    resolved_output = output_path or os.path.join(directory, "index.md")

    for status, files in status_groups.items():
        if not files:
            continue
        emoji = status_emoji.get(status, "")
        index_content += f"\n### {emoji} {status.upper()}\n\n"
        for title, path, file_id in sorted(files, key=lambda x: x[0]):
            rel_path = os.path.relpath(path, os.path.dirname(resolved_output))
            index_content += f"- [{title}]({rel_path})"
            if file_id:
                index_content += f" `[[{file_id}]]`"
            index_content += "\n"

    index_content += (
        f"\n---\n\n"
        f"*Tự động sinh bởi MRM Toolkit vào"
        f" {datetime.now().strftime('%Y-%m-%d %H:%M')}.*\n"
    )

    with open(resolved_output, "w", encoding="utf-8") as fh:
        fh.write(index_content)
    print(f"✅ Đã sinh index.md tại: {resolved_output}")

    return index_content
