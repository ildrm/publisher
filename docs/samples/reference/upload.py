"""Bounded upload inspection example, not a malware scanner or complete DOCX sanitizer."""
from dataclasses import dataclass
from io import BytesIO
from pathlib import PurePosixPath
from zipfile import BadZipFile, ZipFile
import re
import stat


@dataclass(frozen=True)
class UploadPolicy:
    max_bytes: int = 2_000_000
    max_members: int = 100
    max_expanded: int = 5_000_000
    max_ratio: int = 100


def inspect_upload(name: str, data: bytes, policy: UploadPolicy = UploadPolicy()) -> str:
    if not isinstance(data, bytes) or not data or len(data) > policy.max_bytes:
        raise ValueError("empty or oversized upload")
    if not name or "/" in name or "\\" in name:
        raise ValueError("unsafe upload name")
    suffix = name.lower().rsplit(".", 1)[-1]
    if suffix == "md":
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("markdown must be UTF-8") from exc
        if "\x00" in text:
            raise ValueError("NUL not allowed")
        return "markdown"
    if suffix != "docx" or not data.startswith(b"PK\x03\x04"):
        raise ValueError("unsupported type or signature")
    try:
        with ZipFile(BytesIO(data)) as archive:
            members = archive.infolist()
            if not members or len(members) > policy.max_members:
                raise ValueError("archive member limit")
            names: set[str] = set()
            total = 0
            for item in members:
                name_in_zip = item.filename
                path = PurePosixPath(name_in_zip)
                if (not name_in_zip or "\\" in name_in_zip or path.is_absolute()
                    or ".." in path.parts or re.match(r"^[A-Za-z]:", name_in_zip)
                    or name_in_zip in names or stat.S_ISLNK(item.external_attr >> 16)):
                    raise ValueError("unsafe archive path")
                names.add(name_in_zip)
                if item.flag_bits & 1 or name_in_zip.lower().endswith((".bin", ".exe", ".js")):
                    raise ValueError("encrypted or active content rejected")
                total += item.file_size
                if total > policy.max_expanded or item.file_size > policy.max_expanded:
                    raise ValueError("archive expansion limit")
                if item.file_size and item.file_size > max(1, item.compress_size) * policy.max_ratio:
                    raise ValueError("archive compression ratio limit")
                if not item.is_dir():
                    with archive.open(item) as member:
                        content = member.read(policy.max_expanded + 1)
                    if len(content) != item.file_size or len(content) > policy.max_expanded:
                        raise ValueError("invalid member size")
                    if name_in_zip.lower().endswith((".xml", ".rels")):
                        upper = content.upper()
                        if b"<!DOCTYPE" in upper or b"<!ENTITY" in upper or b'TARGETMODE="EXTERNAL"' in upper or b"TARGETMODE='EXTERNAL'" in upper:
                            raise ValueError("unsafe XML or external relationship")
            if not {"[Content_Types].xml", "word/document.xml"}.issubset(names):
                raise ValueError("missing required DOCX parts")
    except (BadZipFile, RuntimeError, EOFError) as exc:
        raise ValueError("invalid archive") from exc
    return "docx"
