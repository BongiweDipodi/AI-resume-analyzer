import json
from pathlib import Path

import pytest

from app.core.education_parser import detect_education_level
from app.core.experience_analyzer import estimate_experience_years
from app.core.resume_parser import extract_resume_sections
from app.core.skill_extractor import (
    extract_job_skills,
    extract_resume_skills,
    load_skill_dict,
)
from app.core.strength_analyzer import analyze_resume_strength
from app.core.text_cleaner import clean_job_description, clean_resume_text
from app.core.vectorizer import vectorize_skills
from app.exceptions import InvalidFileError, SkillDictionaryError
from app.services.match_service import MatchEngine
from app.utils.validators import validate_file_upload, validate_uploaded_bytes


def test_clean_text_functions() -> None:
    assert clean_job_description("Python developer, fastapi!") == "python developer fastapi"
    assert clean_resume_text("Hello\nWORLD!!!") == "hello world"


def test_extract_resume_sections_with_headings() -> None:
    resume_text = "EDUCATION\nMaster of Science\nEXPERIENCE\nData Scientist at Acme\nSKILLS\nPython, SQL\nPROJECTS\nResume Analyzer"
    sections = extract_resume_sections(resume_text)
    assert sections["education"] == "Master of Science"
    assert sections["experience"] == "Data Scientist at Acme"
    assert sections["skills"] == "Python, SQL"
    assert sections["projects"] == "Resume Analyzer"


def test_extract_resume_sections_empty_returns_all_keys() -> None:
    sections = extract_resume_sections("")
    assert sections == {"education": "", "experience": "", "skills": "", "projects": ""}


def test_vectorize_skills_empty_and_with_vocabulary() -> None:
    assert vectorize_skills([]) == []
    assert vectorize_skills(["python", "aws"], vocabulary=["python", "aws", "sql"]) == [1, 1, 0]


def test_load_skill_dict_and_invalid(tmp_path: Path) -> None:
    skill_file = tmp_path / "skills.json"
    skill_file.write_text(json.dumps(["python", "docker"]), encoding="utf-8")

    skills = load_skill_dict(skill_file)
    assert skills == {"python", "docker"}

    missing = tmp_path / "missing.json"
    with pytest.raises(SkillDictionaryError, match="Skill dictionary not found"):
        load_skill_dict(missing)


def test_extract_job_skills_uses_spacy(mock_spacy_nlp) -> None:
    skills = extract_job_skills("AWS SQL engineering")
    assert sorted(skills) == ["aws", "engineering", "sql"]


def test_extract_resume_skills_with_custom_skill_dict() -> None:
    text = "Experienced Python developer with Docker and AWS experience."
    skills = extract_resume_skills(text, skill_dict={"python", "docker", "aws", "java"})
    assert skills == ["aws", "docker", "python"]


def test_strength_analyzer_feedback_and_scoring() -> None:
    resume_text = "Master of Science\n3 years experience\nProject — AI model"
    result = analyze_resume_strength(resume_text)
    assert result["strength_score"] > 0
    assert "Education level detected" in " ".join(result["feedback"])
    assert any("projects" in item.lower() for item in result["feedback"])


def test_match_engine_methods(mock_spacy_nlp) -> None:
    engine = MatchEngine()
    resume_text = "Python developer with AWS and Docker."
    job_desc = "Looking for AWS Python engineer"

    resume_analysis = engine.analyze_resume(resume_text)
    assert "python" in resume_analysis["skills"]
    assert resume_analysis["education"] == "Unknown"

    job_analysis = engine.analyze_job(job_desc)
    assert "aws" in job_analysis["skills"]

    result = engine.match_resume_to_job(resume_text, job_desc)
    assert result["match_score"] >= 0
    assert result["missing_skills"] == [] or isinstance(result["missing_skills"], list)
    assert "feedback" in result

    benchmark = engine.compare_to_benchmark(result["match_score"], industry="data_science")
    assert benchmark["industry"] == "data_science"

    ats_score = engine.estimate_ats_score(resume_text, ["python", "aws"])
    assert 0 <= ats_score <= 100


def test_validate_file_upload_and_uploaded_bytes() -> None:
    validate_file_upload("resume.pdf", 1024, "application/pdf")
    data, ext = validate_uploaded_bytes(b"hello", "resume.pdf")
    assert data == b"hello"
    assert ext == ".pdf"

    with pytest.raises(InvalidFileError, match="Only PDF and DOCX files are supported"):
        validate_file_upload("resume.txt", 1024)

    with pytest.raises(InvalidFileError, match="File exceeds maximum size"):
        validate_file_upload("resume.pdf", 11 * 1024 * 1024)

    with pytest.raises(InvalidFileError, match="Unsupported content type"):
        validate_file_upload("resume.pdf", 1024, "text/plain")


def test_education_and_experience_detection() -> None:
    assert detect_education_level("Master of Science") == "Master"
    assert detect_education_level("graduated in 2019") == "Unknown"
    assert estimate_experience_years("5 years of work experience") == 5
    assert estimate_experience_years("2018-2022") == 4
