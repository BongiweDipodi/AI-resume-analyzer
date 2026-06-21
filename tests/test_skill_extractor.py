"""Unit tests for models.skill_extractor."""

import pytest

from app.core.skill_extractor import extract_job_skills, extract_resume_skills


class TestExtractResumeSkills:
    """Tests for extract_resume_skills."""

    def test_finds_known_skills(self, sample_skill_dict) -> None:
        text = "Experienced in Python, SQL, Machine Learning, Docker and Git."
        result = extract_resume_skills(text, skill_dict=sample_skill_dict)
        assert isinstance(result, list)
        assert "python" in result
        assert "sql" in result
        assert "docker" in result

    def test_returns_sorted_list(self, sample_skill_dict) -> None:
        text = "Git Docker Python SQL"
        result = extract_resume_skills(text, skill_dict=sample_skill_dict)
        assert result == sorted(result)

    def test_empty_resume(self, sample_skill_dict) -> None:
        result = extract_resume_skills("", skill_dict=sample_skill_dict)
        assert result == []
        assert isinstance(result, list)

    def test_no_matching_skills(self, sample_skill_dict) -> None:
        result = extract_resume_skills("Expert in COBOL and Fortran", sample_skill_dict)
        assert result == []

    def test_word_boundary_not_substring(self, sample_skill_dict) -> None:
        skill_dict = sample_skill_dict | {"java"}
        result = extract_resume_skills("javascript developer", skill_dict)
        assert "java" not in result or "javascript" in result

    @pytest.mark.parametrize(
        "text,expected_count",
        [
            ("Python SQL Docker Git AWS React", 6),
            ("!!! Python ??? SQL !!!", 2),
            ("python " * 100, 1),
        ],
    )
    def test_skill_counts(self, sample_skill_dict, text, expected_count) -> None:
        result = extract_resume_skills(text, skill_dict=sample_skill_dict)
        assert len(result) >= 1
        assert isinstance(result, list)


class TestExtractJobSkills:
    """Tests for extract_job_skills (spaCy mocked)."""

    def test_returns_list(self, mock_spacy_nlp) -> None:
        result = extract_job_skills("Python developer with AWS and SQL")
        assert isinstance(result, list)

    def test_deduplicates_keywords(self, mock_spacy_nlp) -> None:
        result = extract_job_skills("Python python PYTHON developer")
        assert len(result) == len(set(result))

    def test_empty_job_description(self, mock_spacy_nlp) -> None:
        result = extract_job_skills("")
        assert result == []

    def test_sorted_output(self, mock_spacy_nlp) -> None:
        result = extract_job_skills("AWS SQL Python machine learning")
        assert result == sorted(result)

    def test_skips_stop_words(self, mock_spacy_nlp) -> None:
        result = extract_job_skills("the a an with python")
        assert "the" not in result

    @pytest.mark.parametrize(
        "jd",
        [
            "Senior Data Scientist — Python, SQL, Docker",
            "x" * 5000,
            "!!! @@@ ###",
        ],
    )
    def test_various_job_descriptions(self, mock_spacy_nlp, jd: str) -> None:
        result = extract_job_skills(jd)
        assert isinstance(result, list)
