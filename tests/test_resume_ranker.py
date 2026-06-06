"""Unit tests for models.resume_ranker."""

import pytest

from app.core.resume_ranker import rank_resumes


class TestRankResumes:
    """Tests for rank_resumes."""

    def test_ranks_descending_by_score(self) -> None:
        scores = {"Alice": 82, "Bob": 65, "Carol": 91, "Dave": 74}
        result = rank_resumes(scores)
        assert isinstance(result, list)
        assert result[0]["candidate"] == "Carol"
        assert result[0]["score"] == 91
        assert result[-1]["candidate"] == "Bob"

    def test_rank_numbers_start_at_one(self) -> None:
        result = rank_resumes({"A": 50, "B": 60})
        assert result[0]["rank"] == 1
        assert result[1]["rank"] == 2

    def test_empty_dict(self) -> None:
        result = rank_resumes({})
        assert result == []
        assert isinstance(result, list)

    def test_single_candidate(self) -> None:
        result = rank_resumes({"Solo": 88.5})
        assert len(result) == 1
        assert result[0] == {"rank": 1, "candidate": "Solo", "score": 88.5}

    def test_tie_preserves_stable_order(self) -> None:
        result = rank_resumes({"X": 70, "Y": 70, "Z": 70})
        assert len(result) == 3
        assert all(entry["score"] == 70 for entry in result)

    @pytest.mark.parametrize(
        "scores,top_name",
        [
            ({"a": 0, "b": 100}, "b"),
            ({"low": -5, "high": 200}, "high"),
            ({"only": 42.42}, "only"),
        ],
    )
    def test_various_score_maps(self, scores: dict, top_name: str) -> None:
        result = rank_resumes(scores)
        assert result[0]["candidate"] == top_name

    def test_return_structure_types(self) -> None:
        result = rank_resumes({"A": 1})
        entry = result[0]
        assert isinstance(entry["rank"], int)
        assert isinstance(entry["candidate"], str)
        assert isinstance(entry["score"], (int, float))
