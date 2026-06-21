"""Tests for app.utils.validators."""

import pytest

from app.exceptions import InvalidFileError
from app.utils.validators import (
    sanitize_text,
    validate_file_upload,
    validate_uploaded_bytes,
)


class TestSanitizeText:
    def test_none_returns_empty(self) -> None:
        assert sanitize_text(None) == ""

    def test_strips_control_chars(self) -> None:
        assert "\x00" not in sanitize_text("hello\x00world")

    def test_truncates_long_text(self) -> None:
        assert len(sanitize_text("a" * 200_000, max_length=100)) == 100


class TestValidateFileUpload:
    def test_valid_pdf(self) -> None:
        validate_file_upload("resume.pdf", 1024)

    def test_invalid_extension(self) -> None:
        with pytest.raises(InvalidFileError):
            validate_file_upload("resume.exe", 1024)

    def test_empty_file(self) -> None:
        with pytest.raises(InvalidFileError):
            validate_file_upload("resume.pdf", 0)

    def test_file_too_large(self) -> None:
        with pytest.raises(InvalidFileError):
            validate_file_upload("resume.pdf", 20 * 1024 * 1024)

    def test_invalid_mime(self) -> None:
        with pytest.raises(InvalidFileError):
            validate_file_upload(
                "resume.pdf",
                100,
                content_type="text/plain",
            )


class TestValidateUploadedBytes:
    def test_returns_extension(self) -> None:
        data, ext = validate_uploaded_bytes(b"content", "file.docx")
        assert data == b"content"
        assert ext == ".docx"
