"""Data models cho MRM Toolkit."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ValidationResult:
    """Kết quả kiểm định một file MRM."""

    file_path: str
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    line_count: int
    has_frontmatter: bool
    has_ai_context: bool
    # Frontmatter đã parse, tránh đọc file lần 2 trong indexer/assembler
    frontmatter: Optional[Dict] = field(default=None, repr=False)
