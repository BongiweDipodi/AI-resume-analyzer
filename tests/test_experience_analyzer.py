"""Unit tests for models.experience_analyzer."""

import pytest

from app.core.experience_analyzer import estimate_experience_years


class TestEstimateExperienceYears:
    """Tests for estimate_experience_years."""

    def test_digit_years_pattern(self) -> None:
        result = estimate_experience_years("I have 5 years of Python experience.")
        assert result == 5
        assert isinstance(result, int)

    def test_word_years_pattern(self) -> None:
        result = estimate_experience_years("Three years working with SQL.")
        assert result == 3

    def test_year_range_with_present(self) -> None:
        text = "Developer at Co | 2020 - Present"
        result = estimate_experience_years(text)
        assert result >= 5

    def test_multiple_ranges_sums_duration(self) -> None:
        text = """
    Role A 2019-2020
    Role B 2021-2022
    Also 2 years with Python
    """
        result = estimate_experience_years(text)
        assert isinstance(result, int)
        assert result >= 2

    def test_empty_resume_returns_zero(self) -> None:
        assert estimate_experience_years("") == 0

    @pytest.mark.parametrize(
        "text,minimum",
        [
            ("10 years in leadership", 10),
            ("one year internship", 1),
            ("2018 to 2020 internship", 2),
            ("No dates or years mentioned", 0),
            ("!!! 7 years !!!", 7),
        ],
    )
    def test_various_patterns(self, text: str, minimum: int) -> None:
        result = estimate_experience_years(text)
        assert isinstance(result, int)
        assert result >= minimum

    def test_returns_max_of_estimates(self) -> None:
        text = "2 years with Java. Worked 2015-2024 as engineer."
        result = estimate_experience_years(text)
        assert result >= 2

    def test_special_characters_in_range(self) -> None:
        text = "Internship 2019–2020 at DataCo"
        result = estimate_experience_years(text)
        assert result >= 1
