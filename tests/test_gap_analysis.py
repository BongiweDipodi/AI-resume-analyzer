"""Unit tests for resume feedback generation."""

import pytest

from app.services.feedback_service import generate_resume_feedback


class TestGenerateResumeFeedback:
    """Tests for generate_resume_feedback."""

    def test_no_missing_skills_positive_message(self) -> None:
        result = generate_resume_feedback([])
        assert isinstance(result, list)
        assert len(result) == 1
        assert "Great match" in result[0]

    def test_missing_skills_suggestion(self) -> None:
        result = generate_resume_feedback(["sql", "docker"])
        assert len(result) >= 1
        assert "sql" in result[0].lower()
        assert "docker" in result[0].lower()

    def test_single_missing_skill(self) -> None:
        result = generate_resume_feedback(["aws"])
        assert "aws" in result[0].lower()

    def test_many_missing_skills(self) -> None:
        missing = [f"skill{i}" for i in range(10)]
        result = generate_resume_feedback(missing)
        assert isinstance(result[0], str)
        assert "skill0" in result[0]

    @pytest.mark.parametrize(
        "missing,fragment",
        [
            (["python"], "python"),
            (["C++", "SQL"], "c++"),
            (["machine learning"], "machine learning"),
        ],
    )
    def test_lists_skills_in_message(self, missing, fragment) -> None:
        result = generate_resume_feedback(missing)
        assert fragment.lower() in result[0].lower()

    def test_return_type_is_list_of_strings(self) -> None:
        result = generate_resume_feedback(["git"])
        assert all(isinstance(item, str) for item in result)
