"""Unit tests for match scoring and job matching."""

import pytest

from app.core.match_scoring import (
    calculate_match_score,
    identify_skill_gap,
    match_resume_to_job,
)


class TestCalculateMatchScore:
    """Tests for calculate_match_score."""

    def test_full_match(self) -> None:
        job = ["python", "sql", "docker"]
        matched = ["python", "sql", "docker"]
        result = calculate_match_score(matched, job)
        assert result == 100.0
        assert isinstance(result, float)

    def test_partial_match(self) -> None:
        result = calculate_match_score(["python"], ["python", "sql", "docker", "aws"])
        assert result == 25.0

    def test_no_match(self) -> None:
        result = calculate_match_score([], ["python", "sql"])
        assert result == 0.0

    def test_empty_job_skills(self) -> None:
        result = calculate_match_score(["python"], [])
        assert result == 0.0

    @pytest.mark.parametrize(
        "matched,job,expected",
        [
            (["a", "b"], ["a", "b", "c", "d"], 50.0),
            (["x"], ["x"], 100.0),
            ([], ["only"], 0.0),
        ],
    )
    def test_parametrized_scores(self, matched, job, expected) -> None:
        assert calculate_match_score(matched, job) == expected

    def test_rounded_two_decimals(self) -> None:
        result = calculate_match_score(["a"], ["a", "b", "c"])
        assert result == round(result, 2)


class TestMatchResumeToJob:
    """Tests for match_resume_to_job."""

    def test_returns_dict_with_keys(self) -> None:
        result = match_resume_to_job(["Python", "Java"], ["Python", "SQL"])
        assert isinstance(result, dict)
        assert "matched_skills" in result
        assert "missing_skills" in result

    def test_case_insensitive_matching(self) -> None:
        result = match_resume_to_job(["PYTHON"], ["python", "sql"])
        assert "python" in result["matched_skills"]
        assert "sql" in result["missing_skills"]

    def test_no_overlap(self) -> None:
        result = match_resume_to_job(["java"], ["python", "sql"])
        assert result["matched_skills"] == []
        assert set(result["missing_skills"]) == {"python", "sql"}

    def test_empty_resume_skills(self) -> None:
        result = match_resume_to_job([], ["python"])
        assert result["matched_skills"] == []
        assert "python" in result["missing_skills"]

    def test_empty_job_skills(self) -> None:
        result = match_resume_to_job(["python"], [])
        assert result["matched_skills"] == []
        assert result["missing_skills"] == []

    @pytest.mark.parametrize(
        "resume,job,matched_count",
        [
            (["Python", "AWS"], ["Python", "AWS", "SQL"], 2),
            (["a", "b", "c"], ["a", "b", "c"], 3),
            (["X"], ["x"], 1),
        ],
    )
    def test_match_counts(self, resume, job, matched_count) -> None:
        result = match_resume_to_job(resume, job)
        assert len(result["matched_skills"]) == matched_count


class TestIdentifySkillGap:
    """Tests for identify_skill_gap."""

    def test_matched_and_missing(self) -> None:
        result = identify_skill_gap(
            ["python", "sql", "machine learning", "git"],
            ["python", "sql", "docker", "aws", "machine learning"],
        )
        assert isinstance(result, dict)
        assert result["matched"] == ["machine learning", "python", "sql"]
        assert result["missing"] == ["aws", "docker"]

    def test_case_insensitive(self) -> None:
        result = identify_skill_gap(["PYTHON"], ["python"])
        assert result["matched"] == ["python"]
        assert result["missing"] == []

    def test_empty_candidate(self) -> None:
        result = identify_skill_gap([], ["python", "sql"])
        assert result["matched"] == []
        assert result["missing"] == ["python", "sql"]

    def test_empty_job(self) -> None:
        result = identify_skill_gap(["python"], [])
        assert result["matched"] == []
        assert result["missing"] == []

    def test_full_overlap(self) -> None:
        skills = ["python", "sql"]
        result = identify_skill_gap(skills, skills)
        assert result["missing"] == []

    @pytest.mark.parametrize(
        "candidate,job",
        [
            (["A"], ["a"]),
            (["docker", "docker"], ["docker"]),
            (["x" * 50], ["x" * 50, "y"]),
        ],
    )
    def test_various_gaps(self, candidate, job) -> None:
        result = identify_skill_gap(candidate, job)
        assert isinstance(result["matched"], list)
        assert isinstance(result["missing"], list)
