"""Tests for MatchEngine orchestrator."""

import pytest

from app.exceptions import InvalidJobDescriptionError, InvalidResumeError
from app.services.match_service import MatchEngine


@pytest.fixture
def engine() -> MatchEngine:
    return MatchEngine()


class TestMatchEngine:
    """MatchEngine integration unit tests."""

    def test_analyze_resume(self, engine, sample_resume_1) -> None:
        result = engine.analyze_resume(sample_resume_1)
        assert isinstance(result["skills"], list)
        assert result["education"] == "Master"
        assert result["experience_years"] >= 1

    def test_analyze_job(self, engine, sample_job_desc) -> None:
        result = engine.analyze_job(sample_job_desc)
        assert isinstance(result["skills"], list)
        assert "cleaned_text" in result

    def test_match_resume_to_job(
        self, engine, sample_resume_1, sample_job_desc
    ) -> None:
        result = engine.match_resume_to_job(sample_resume_1, sample_job_desc)
        assert 0 <= result["match_score"] <= 100
        assert "ats_score" in result
        assert "keyword_suggestions" in result
        assert "cover_letter_draft" in result

    def test_analyze_strength(self, engine, sample_resume_1) -> None:
        result = engine.analyze_strength(sample_resume_1)
        assert 0 <= result["strength_score"] <= 100

    def test_compare_resumes(self, engine, sample_resume_1, sample_resume_2) -> None:
        score = engine.compare_resumes(sample_resume_1, sample_resume_2)
        assert 0.0 <= score <= 1.0

    def test_rank_resumes(self, engine) -> None:
        ranking = engine.rank_resumes({"A": 90, "B": 70})
        assert ranking[0]["candidate"] == "A"

    def test_empty_resume_raises(self, engine) -> None:
        with pytest.raises(InvalidResumeError):
            engine.analyze_resume("")

    def test_empty_job_raises(self, engine, sample_resume_1) -> None:
        with pytest.raises(InvalidJobDescriptionError):
            engine.match_resume_to_job(sample_resume_1, "")

    def test_benchmark_comparison(self, engine) -> None:
        bench = engine.compare_to_benchmark(85.0, industry="data_science")
        assert bench["percentile_label"] == "Top 25%"

    def test_benchmark_below_average(self, engine) -> None:
        bench = engine.compare_to_benchmark(40.0, industry="general")
        assert bench["percentile_label"] == "Below average"
