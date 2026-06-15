"""Unit tests for models.vectorizer."""

import pytest
from unittest.mock import patch, MagicMock

from app.core.vectorizer import vectorize_skills

VOCAB = ["python", "sql", "ml", "docker", "git"]


class TestVectorizeSkills:
    """Tests for vectorize_skills."""

    def test_with_fixed_vocabulary(self) -> None:
        result = vectorize_skills(["python", "ml", "git"], vocabulary=VOCAB)
        assert isinstance(result, list)
        assert result == [1, 0, 1, 0, 1]

    def test_empty_skill_list(self) -> None:
        result = vectorize_skills([])
        assert result == []

    def test_single_skill(self) -> None:
        result = vectorize_skills(["python"], vocabulary=VOCAB)
        assert result[0] == 1
        assert sum(result) == 1

    def test_unknown_skills_zero_vector(self) -> None:
        result = vectorize_skills(["cobol"], vocabulary=VOCAB)
        assert isinstance(result, list)
        assert sum(result) == 0

    def test_without_vocabulary_builds_from_input(self) -> None:
        result = vectorize_skills(["alpha", "beta"])
        assert isinstance(result, list)
        assert len(result) >= 1
        assert all(v in (0, 1) for v in result)

    @pytest.mark.parametrize(
        "skills,expected_sum",
        [
            (["python", "sql"], 2),
            (["docker"], 1),
            ([], 0),
        ],
    )
    def test_vector_sums(self, skills, expected_sum) -> None:
        if not skills:
            assert vectorize_skills(skills) == []
        else:
            result = vectorize_skills(skills, vocabulary=VOCAB)
            assert sum(result) == expected_sum

    @patch("app.core.vectorizer.CountVectorizer")
    def test_uses_count_vectorizer_with_vocab(self, mock_cv_cls) -> None:
        import numpy as np

        mock_instance = MagicMock()
        mock_matrix = MagicMock()
        mock_matrix.toarray.return_value = np.array([[1, 0, 1]])
        mock_instance.fit_transform.return_value = mock_matrix
        mock_cv_cls.return_value = mock_instance

        result = vectorize_skills(["python", "ml"], vocabulary=["python", "ml", "x"])
        assert result == [1, 0, 1]
        mock_cv_cls.assert_called_once()
