"""Unit tests for models.education_parser."""

import pytest

from app.core.education_parser import detect_education_level


@pytest.mark.parametrize(
    "text,expected",
    [
        ("PhD in Artificial Intelligence, UCT", "PhD"),
        ("Completed doctoral research in NLP", "PhD"),
        ("Doctorate in Physics", "PhD"),
        ("Master of Science in Data Science", "Master"),
        ("MBA graduate from Wits", "Master"),
        ("M.Sc. Statistics", "Master"),
        ("Bachelor of Science in Computer Science", "Bachelor"),
        ("BSc Computer Science 2023", "Bachelor"),
        ("B.Tech Information Technology", "Bachelor"),
        ("Undergraduate degree in Engineering", "Bachelor"),
        ("Matric Certificate, Benoni High School", "High School"),
        ("Grade 12 completed 2018", "High School"),
        ("Secondary school diploma", "High School"),
        ("Self-taught programmer with portfolio", "Unknown"),
        ("", "Unknown"),
    ],
)
def test_detect_education_level_parametrized(text: str, expected: str) -> None:
    result = detect_education_level(text)
    assert result == expected
    assert isinstance(result, str)


class TestDetectEducationLevel:
    """Additional edge-case tests for detect_education_level."""

    def test_phd_takes_priority_over_bachelor(self) -> None:
        text = "BSc then PhD in Machine Learning"
        assert detect_education_level(text) == "PhD"

    def test_case_insensitive(self) -> None:
        assert detect_education_level("MASTER DEGREE IN CS") == "Master"

    def test_special_characters(self) -> None:
        result = detect_education_level("M.Sc!!! @@@ Data Science")
        assert result == "Master"

    def test_very_long_text(self) -> None:
        padding = "word " * 2000
        result = detect_education_level(padding + " bachelor degree ")
        assert result == "Bachelor"

    def test_unknown_returns_string(self) -> None:
        result = detect_education_level("No formal education listed")
        assert result == "Unknown"
        assert result in {"PhD", "Master", "Bachelor", "High School", "Unknown"}
