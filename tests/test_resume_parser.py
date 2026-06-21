"""Unit tests for models.resume_parser."""

import pytest

from app.core.resume_parser import extract_resume_sections

SAMPLE_RESUME = """
JOHN DOE — Software Engineer

EDUCATION
BSc Computer Science, Unisa | 2020-2023

WORK EXPERIENCE
Junior Developer | StartupX | 2023-2024
- Built REST APIs with FastAPI

TECHNICAL SKILLS
Python, SQL, Docker, Git

PROJECTS
Resume Analyzer — Python + Streamlit
"""


class TestExtractResumeSections:
    """Tests for extract_resume_sections."""

    def test_returns_dict_with_expected_keys(self) -> None:
        result = extract_resume_sections(SAMPLE_RESUME)
        assert isinstance(result, dict)
        assert set(result.keys()) == {"education", "experience", "skills", "projects"}

    def test_education_section_populated(self) -> None:
        result = extract_resume_sections(SAMPLE_RESUME)
        assert (
            "bsc" in result["education"].lower()
            or "computer" in result["education"].lower()
        )

    def test_experience_section_populated(self) -> None:
        result = extract_resume_sections(SAMPLE_RESUME)
        assert (
            "developer" in result["experience"].lower()
            or "fastapi" in result["experience"].lower()
        )

    def test_skills_section_populated(self) -> None:
        result = extract_resume_sections(SAMPLE_RESUME)
        assert "python" in result["skills"].lower()

    def test_projects_section_populated(self) -> None:
        result = extract_resume_sections(SAMPLE_RESUME)
        assert (
            "resume" in result["projects"].lower()
            or "streamlit" in result["projects"].lower()
        )

    def test_empty_resume(self) -> None:
        result = extract_resume_sections("")
        assert all(v == "" for v in result.values())

    @pytest.mark.parametrize(
        "heading",
        [
            "ACADEMIC BACKGROUND\nBSc 2020",
            "EMPLOYMENT\nEngineer at Co",
            "CORE COMPETENCIES\nPython SQL",
            "PERSONAL PROJECTS\nApp — React",
        ],
    )
    def test_alternate_headings(self, heading: str) -> None:
        result = extract_resume_sections(heading)
        assert isinstance(result, dict)
        assert any(result.values()) or heading == ""

    def test_no_headings_returns_empty_sections(self) -> None:
        result = extract_resume_sections("Just a paragraph with no sections.")
        assert all(v == "" for v in result.values())

    def test_multiline_content_appended(self) -> None:
        resume = "SKILLS\nPython\nSQL\nDocker\n"
        result = extract_resume_sections(resume)
        assert "sql" in result["skills"].lower()
