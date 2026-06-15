"""Tests for feedback service extras."""

from app.services.feedback_service import (
    generate_cover_letter_draft,
    generate_keyword_suggestions,
)


def test_keyword_suggestions_empty() -> None:
    assert "already" in generate_keyword_suggestions([])[0].lower()


def test_cover_letter_with_skills() -> None:
    letter = generate_cover_letter_draft(["python", "aws"], job_title="Data Scientist")
    assert "Data Scientist" in letter
    assert "python" in letter
