"""Tests for app.utils.file_handlers."""

import io
from unittest.mock import MagicMock, patch

import pytest

from app.exceptions import InvalidFileError
from app.utils.file_handlers import parse_docx, parse_pdf, parse_uploaded_file


class TestParsePdf:
    @patch("app.utils.file_handlers.pdfplumber.open")
    def test_extracts_text(self, mock_open) -> None:
        page = MagicMock()
        page.extract_text.return_value = "Python developer"
        pdf = MagicMock()
        pdf.pages = [page]
        mock_open.return_value.__enter__.return_value = pdf

        result = parse_pdf(b"%PDF", filename="resume.pdf")
        assert result == "Python developer"
        assert isinstance(result, str)

    @patch("app.utils.file_handlers.pdfplumber.open")
    def test_empty_pdf_raises(self, mock_open) -> None:
        page = MagicMock()
        page.extract_text.return_value = None
        pdf = MagicMock()
        pdf.pages = [page]
        mock_open.return_value.__enter__.return_value = pdf

        with pytest.raises(InvalidFileError):
            parse_pdf(b"%PDF", filename="resume.pdf")

    def test_corrupted_pdf_raises(self) -> None:
        with pytest.raises(InvalidFileError):
            parse_pdf(b"not-a-pdf", filename="resume.pdf")


class TestParseDocx:
    @patch("app.utils.file_handlers.Document")
    def test_extracts_paragraphs(self, mock_document) -> None:
        p1, p2 = MagicMock(), MagicMock()
        p1.text = "Line one"
        p2.text = "Line two"
        mock_document.return_value.paragraphs = [p1, p2]

        result = parse_docx(b"docx", filename="resume.docx")
        assert "Line one" in result
        assert "Line two" in result

    @patch("app.utils.file_handlers.Document")
    def test_empty_docx_raises(self, mock_document) -> None:
        mock_document.return_value.paragraphs = []
        with pytest.raises(InvalidFileError):
            parse_docx(b"docx", filename="resume.docx")

    @patch("app.utils.file_handlers.Document", side_effect=RuntimeError("bad"))
    def test_corrupted_docx_raises(self, _mock) -> None:
        with pytest.raises(InvalidFileError):
            parse_docx(b"bad", filename="resume.docx")


class TestParseUploadedFile:
    @patch("app.utils.file_handlers.parse_pdf", return_value="pdf text")
    def test_routes_pdf(self, _mock) -> None:
        assert parse_uploaded_file(io.BytesIO(b"x"), "a.pdf") == "pdf text"

    @patch("app.utils.file_handlers.parse_docx", return_value="docx text")
    def test_routes_docx(self, _mock) -> None:
        assert parse_uploaded_file(io.BytesIO(b"x"), "a.docx") == "docx text"

    def test_unsupported_extension(self) -> None:
        with pytest.raises(InvalidFileError):
            parse_uploaded_file(b"x", "a.txt")
