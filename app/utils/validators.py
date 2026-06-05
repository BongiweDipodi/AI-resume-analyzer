"""Input validation utilities."""

import re
from typing import Tuple

from app import MAX_FILE_SIZE
from app.exceptions import InvalidFileError

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


def sanitize_text(text: str, max_length: int = 100_000) -> str:
    """Sanitize user-provided text input.

    Args:
        text: Raw user text.
        max_length: Maximum allowed character length.

    Returns:
        Sanitized text string.
    """
    if text is None:
        return ""
    cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", str(text))
    return cleaned[:max_length].strip()


def validate_file_upload(
    filename: str,
    file_size: int,
    content_type: str | None = None,
) -> None:
    """Validate uploaded file metadata.

    Args:
        filename: Original filename.
        file_size: File size in bytes.
        content_type: Optional MIME type.

    Raises:
        InvalidFileError: If validation fails.
    """
    if not filename:
        raise InvalidFileError("Filename is required.")

    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise InvalidFileError("Only PDF and DOCX files are supported.")

    if file_size <= 0:
        raise InvalidFileError("File is empty.")

    if file_size > MAX_FILE_SIZE:
        raise InvalidFileError(
            f"File exceeds maximum size of {MAX_FILE_SIZE // (1024 * 1024)}MB"
        )

    if content_type and content_type not in ALLOWED_MIME_TYPES:
        raise InvalidFileError(f"Unsupported content type: {content_type}")


def validate_uploaded_bytes(data: bytes, filename: str) -> Tuple[bytes, str]:
    """Validate raw file bytes and return them with extension.

    Args:
        data: File content bytes.
        filename: Original filename.

    Returns:
        Tuple of (data, lowercase extension).

    Raises:
        InvalidFileError: If validation fails.
    """
    validate_file_upload(filename, len(data))
    ext = "." + filename.rsplit(".", 1)[-1].lower()
    return data, ext
