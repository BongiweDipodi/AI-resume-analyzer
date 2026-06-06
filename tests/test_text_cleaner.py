"""Unit tests for utils.text_cleaner."""

import pytest

from app.core.text_cleaner import clean_job_description, clean_resume_text


class TestCleanResumeText:
    """Tests for clean_resume_text."""

    def test_lowercases_text(self) -> None:
        result = clean_resume_text("Python SQL")
        assert result == "python sql"
        assert isinstance(result, str)

    def test_removes_special_characters(self) -> None:
        result = clean_resume_text("Python!!! @#$ SQL")
        assert "!" not in result
        assert "python" in result
        assert "sql" in result

    def test_collapses_whitespace(self) -> None:
        result = clean_resume_text("Python    SQL   Data")
        assert result == "python sql data"

    def test_preserves_allowed_punctuation(self) -> None:
        result = clean_resume_text("Node.js, C++: API-dev")
        assert "." in result or "node" in result

    @pytest.mark.parametrize(
        "raw,expected_fragment",
        [
            ("", ""),
            ("   ", ""),
            ("A" * 5000 + " PYTHON ", "python"),
        ],
    )
    def test_edge_cases(self, raw: str, expected_fragment: str) -> None:
        result = clean_resume_text(raw)
        assert isinstance(result, str)
        assert expected_fragment in result

    def test_none_like_empty_string(self) -> None:
        result = clean_resume_text("")
        assert result == ""

    def test_none_input_returns_empty(self) -> None:
        assert clean_resume_text(None) == ""


class TestCleanJobDescription:
    """Tests for clean_job_description."""

    def test_lowercases_and_strips(self) -> None:
        result = clean_job_description("  PYTHON Developer  ")
        assert result == "python developer"
        assert isinstance(result, str)

    def test_removes_punctuation(self) -> None:
        result = clean_job_description("Python, SQL & AWS!")
        assert "," not in result
        assert "&" not in result
        assert "python" in result

    def test_normalizes_spaces(self) -> None:
        result = clean_job_description("Python\n\nSQL\t\tDocker")
        assert "  " not in result
        assert result.count(" ") >= 2

    def test_empty_string(self) -> None:
        result = clean_job_description("")
        assert result == ""

    @pytest.mark.parametrize(
        "text,token",
        [
            ("C++ required", "c"),
            ("Machine-Learning role", "machine"),
            ("!!!URGENT!!!", "urgent"),
            ("a" * 3000, "a"),
        ],
    )
    def test_various_inputs(self, text: str, token: str) -> None:
        result = clean_job_description(text)
        assert isinstance(result, str)
        assert token in result

    def test_only_special_characters(self) -> None:
        result = clean_job_description("!@#$%^&*()")
        assert result == "" or result.strip() == ""

    def test_none_input_returns_empty(self) -> None:
        assert clean_job_description(None) == ""
