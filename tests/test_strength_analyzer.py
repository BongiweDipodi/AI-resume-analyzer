"""Unit tests for models.resume_strength."""

import pytest
from unittest.mock import patch

from app.core.strength_analyzer import analyze_resume_strength

STRENGTH_RESUME = """
John Doe — BSc Computer Science

EXPERIENCE
Developer at TechCo 2022-2024 (2 years experience with Python)
Intern at DataLab 2021-2022

TECHNICAL SKILLS
Python, SQL, Machine Learning, Docker, Git, Flask

PROJECTS
Resume Analyzer — Streamlit + Python
Data Dashboard — Pandas + Plotly
"""


class TestAnalyzeResumeStrength:
    """Tests for analyze_resume_strength."""

    def test_returns_dict_with_required_keys(self) -> None:
        result = analyze_resume_strength(STRENGTH_RESUME)
        assert isinstance(result, dict)
        assert "strength_score" in result
        assert "feedback" in result

    def test_score_in_valid_range(self) -> None:
        result = analyze_resume_strength(STRENGTH_RESUME)
        assert isinstance(result["strength_score"], int)
        assert 0 <= result["strength_score"] <= 100

    def test_feedback_is_list_of_strings(self) -> None:
        result = analyze_resume_strength(STRENGTH_RESUME)
        assert isinstance(result["feedback"], list)
        assert all(isinstance(tip, str) for tip in result["feedback"])

    def test_empty_resume_low_score(self) -> None:
        result = analyze_resume_strength("")
        assert result["strength_score"] <= 30

    def test_education_mentioned_in_feedback(self) -> None:
        result = analyze_resume_strength("Master degree in Statistics. Python SQL.")
        assert any("Education" in tip for tip in result["feedback"])

    @patch("app.core.strength_analyzer.extract_resume_skills", return_value=[])
    @patch("app.core.strength_analyzer.estimate_experience_years", return_value=0)
    @patch("app.core.strength_analyzer.detect_education_level", return_value="Unknown")
    def test_mocked_dependencies_minimal_score(self, _edu, _exp, _skills) -> None:
        result = analyze_resume_strength("minimal text")
        assert result["strength_score"] >= 0
        assert len(result["feedback"]) >= 3

    @pytest.mark.parametrize(
        "resume,minimum_score",
        [
            (STRENGTH_RESUME, 40),
            ("PhD holder with 10 years Python SQL Docker Git AWS Java", 20),
            ("No skills no education", 0),
        ],
    )
    def test_various_resumes(self, resume: str, minimum_score: int) -> None:
        result = analyze_resume_strength(resume)
        assert result["strength_score"] >= minimum_score

    def test_single_project_partial_credit(self) -> None:
        resume = "SKILLS\nPython\nPROJECTS\nApp — built with Flask\n"
        result = analyze_resume_strength(resume)
        assert any("more projects" in tip.lower() for tip in result["feedback"])

    def test_projects_boost_score(self) -> None:
        with_projects = STRENGTH_RESUME
        without = "Python SQL. No projects here."
        score_with = analyze_resume_strength(with_projects)["strength_score"]
        score_without = analyze_resume_strength(without)["strength_score"]
        assert score_with >= score_without
