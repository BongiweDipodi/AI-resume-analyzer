"""End-to-end integration tests across modules."""

import pytest

from app.core.education_parser import detect_education_level
from app.core.experience_analyzer import estimate_experience_years
from app.core.match_scoring import (
    calculate_match_score,
    identify_skill_gap,
    match_resume_to_job,
)
from app.core.resume_ranker import rank_resumes
from app.core.similarity_engine import calculate_resume_similarity
from app.core.skill_extractor import extract_resume_skills
from app.core.strength_analyzer import analyze_resume_strength


class TestResumeJobMatchFlow:
    """Full resume + job description → match score."""

    def test_end_to_end_match(
        self, sample_resume_1, sample_job_desc, sample_skill_dict
    ) -> None:
        resume_skills = extract_resume_skills(
            sample_resume_1, skill_dict=sample_skill_dict | {"pandas", "aws"}
        )
        job_skills = [
            "python",
            "sql",
            "docker",
            "aws",
            "machine learning",
            "data analysis",
        ]
        gap = identify_skill_gap(resume_skills, job_skills)
        match = match_resume_to_job(resume_skills, job_skills)
        score = calculate_match_score(gap["matched"], job_skills)

        assert isinstance(score, float)
        assert 0 <= score <= 100
        assert score == calculate_match_score(match["matched_skills"], job_skills)
        assert len(gap["matched"]) >= 1


class TestMultipleResumeRanking:
    """Multiple resumes → ranking."""

    def test_rank_two_candidates(
        self, sample_resume_1, sample_resume_2, sample_job_desc, sample_skill_dict
    ) -> None:
        job_skills = ["python", "sql", "git", "docker", "machine learning", "fastapi"]
        scores = {}
        for name, resume in [("Jane", sample_resume_1), ("John", sample_resume_2)]:
            skills = extract_resume_skills(
                resume, skill_dict=sample_skill_dict | {"fastapi", "java", "flask"}
            )
            gap = identify_skill_gap(skills, job_skills)
            scores[name] = calculate_match_score(gap["matched"], job_skills)

        ranking = rank_resumes(scores)
        assert len(ranking) == 2
        assert ranking[0]["rank"] == 1
        assert ranking[0]["score"] >= ranking[1]["score"]


class TestResumeStrengthFlow:
    """Complete strength analysis flow."""

    def test_strength_pipeline(self, sample_resume_1) -> None:
        result = analyze_resume_strength(sample_resume_1)
        edu = detect_education_level(sample_resume_1)
        years = estimate_experience_years(sample_resume_1)

        assert result["strength_score"] > 0
        assert edu == "Master"
        assert years >= 1
        assert len(result["feedback"]) >= 4


class TestResumeSimilarityFlow:
    """Compare two sample resumes."""

    def test_similarity_between_samples(self, sample_resume_1, sample_resume_2) -> None:
        sim = calculate_resume_similarity(sample_resume_1, sample_resume_2)
        assert isinstance(sim, float)
        assert 0.0 < sim < 1.0
