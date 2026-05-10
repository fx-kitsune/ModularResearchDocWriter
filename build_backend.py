"""Small dependency-free PEP 517 backend for the skill installer package."""

from __future__ import annotations

import base64
import csv
import hashlib
import os
import zipfile
from pathlib import Path
from typing import List, Tuple

NAME = "modular-research-doc-writer"
NORMALIZED = "modular_research_doc_writer"
VERSION = "1.0.0"
DIST_INFO = f"{NORMALIZED}-{VERSION}.dist-info"
WHEEL_NAME = f"{NORMALIZED}-{VERSION}-py3-none-any.whl"


def _metadata() -> str:
    return "\n".join(
        [
            "Metadata-Version: 2.1",
            f"Name: {NAME}",
            f"Version: {VERSION}",
            "Summary: Installable Codex skill package for ModularResearchDocWriter.",
            "Requires-Python: >=3.8",
            "License: MIT",
            "",
        ]
    )


def _wheel() -> str:
    return "\n".join(
        [
            "Wheel-Version: 1.0",
            "Generator: modular-research-doc-writer-build-backend",
            "Root-Is-Purelib: true",
            "Tag: py3-none-any",
            "",
        ]
    )


def _entry_points() -> str:
    return "\n".join(
        [
            "[console_scripts]",
            "mrm-skill-install = modular_research_doc_writer.installer:main",
            "",
        ]
    )


def _hash(data: bytes) -> str:
    digest = hashlib.sha256(data).digest()
    return "sha256=" + base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def _write_file(wheel: zipfile.ZipFile, records: List[Tuple[str, str, str]], arcname: str, data: bytes) -> None:
    wheel.writestr(arcname, data)
    records.append((arcname, _hash(data), str(len(data))))


def _iter_package_files(root: Path):
    package_root = root / NORMALIZED
    for path in sorted(package_root.rglob("*")):
        if path.is_file():
            yield path, path.relative_to(root).as_posix()


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    root = Path(__file__).resolve().parent
    wheel_path = Path(wheel_directory) / WHEEL_NAME
    records: List[Tuple[str, str, str]] = []

    with zipfile.ZipFile(wheel_path, "w", compression=zipfile.ZIP_DEFLATED) as wheel:
        for path, arcname in _iter_package_files(root):
            _write_file(wheel, records, arcname, path.read_bytes())

        _write_file(wheel, records, f"{DIST_INFO}/METADATA", _metadata().encode("utf-8"))
        _write_file(wheel, records, f"{DIST_INFO}/WHEEL", _wheel().encode("utf-8"))
        _write_file(wheel, records, f"{DIST_INFO}/entry_points.txt", _entry_points().encode("utf-8"))

        record_name = f"{DIST_INFO}/RECORD"
        rows = records + [(record_name, "", "")]
        record_text = _csv_rows(rows)
        wheel.writestr(record_name, record_text.encode("utf-8"))

    return os.fspath(wheel_path.name)


def _csv_rows(rows: List[Tuple[str, str, str]]) -> str:
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerows(rows)
    return output.getvalue()


def build_sdist(sdist_directory, config_settings=None):
    raise NotImplementedError("sdist builds are not supported by this minimal backend")


def get_requires_for_build_wheel(config_settings=None):
    return []


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    dist_info = Path(metadata_directory) / DIST_INFO
    dist_info.mkdir(parents=True, exist_ok=True)
    (dist_info / "METADATA").write_text(_metadata(), encoding="utf-8")
    (dist_info / "WHEEL").write_text(_wheel(), encoding="utf-8")
    (dist_info / "entry_points.txt").write_text(_entry_points(), encoding="utf-8")
    return DIST_INFO
