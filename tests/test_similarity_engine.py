"""Unit tests for models.similarity_engine."""

import pytest
from unittest.mock import MagicMock, patch

from app.core.similarity_engine import calculate_resume_similarity


class TestCalculateResumeSimilarity:
    """Tests for calculate_resume_similarity."""

    def test_identical_resumes_high_similarity(self) -> None:
        text = "Python SQL Machine Learning Data Analysis"
        result = calculate_resume_similarity(text, text)
        assert isinstance(result, float)
        assert result == 1.0

    def test_different_resumes_lower_similarity(self) -> None:
        r1 = "Python SQL Machine Learning"
        r2 = "Java Spring Hibernate Oracle"
        result = calculate_resume_similarity(r1, r2)
        assert 0.0 <= result < 1.0

    def test_overlapping_resumes_moderate_similarity(self) -> None:
        r1 = "Python SQL Machine Learning Data Analysis"
        r2 = "Python SQL Deep Learning Data Science"
        result = calculate_resume_similarity(r1, r2)
        assert 0.0 < result <= 1.0

    def test_empty_strings(self) -> None:
        result = calculate_resume_similarity("", "")
        assert isinstance(result, float)
        assert result >= 0.0

    def test_rounded_to_four_decimals(self) -> None:
        r1 = "alpha beta gamma"
        r2 = "alpha beta delta"
        result = calculate_resume_similarity(r1, r2)
        assert result == round(result, 4)

    @pytest.mark.parametrize(
        "r1,r2",
        [
            ("python developer", "java engineer"),
            ("x" * 1000, "x" * 1000),
            ("!!! python ???", "python skills"),
        ],
    )
    def test_various_inputs(self, r1: str, r2: str) -> None:
        result = calculate_resume_similarity(r1, r2)
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    @patch("app.core.similarity_engine.cosine_similarity")
    @patch("app.core.similarity_engine.TfidfVectorizer")
    def test_uses_sklearn_pipeline(self, mock_vectorizer_cls, mock_cosine) -> None:
        mock_matrix = MagicMock()
        mock_vectorizer = MagicMock()
        mock_vectorizer.fit_transform.return_value = mock_matrix
        mock_vectorizer_cls.return_value = mock_vectorizer
        mock_cosine.return_value = [[0.42]]

        result = calculate_resume_similarity("resume a", "resume b")
        assert result == 0.42
        mock_vectorizer.fit_transform.assert_called_once()
