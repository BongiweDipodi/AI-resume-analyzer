"""Shared pytest fixtures and path setup."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATA_DIR = Path(__file__).resolve().parent / "data"


@pytest.fixture
def sample_skill_dict() -> set:
    """Small skill dictionary for isolated skill extraction tests."""
    return {
        "python",
        "sql",
        "machine learning",
        "docker",
        "git",
        "javascript",
        "react",
        "aws",
    }


@pytest.fixture
def mock_spacy_nlp(monkeypatch):
    """Replace spaCy nlp with a mock that returns predictable tokens."""

    class MockToken:
        def __init__(self, text, pos_, lemma_=None, is_stop=False, is_punct=False):
            self.text = text
            self.pos_ = pos_
            self.lemma_ = lemma_ if lemma_ is not None else text.lower()
            self.is_stop = is_stop
            self.is_punct = is_punct

    class MockDoc:
        def __init__(self, tokens):
            self._tokens = tokens

        def __iter__(self):
            return iter(self._tokens)

    def make_doc(text):
        tokens = []
        for word in text.split():
            lower = word.lower().strip(".,;")
            if not lower:
                continue
            if lower in {"the", "a", "an", "with", "and", "of"}:
                tokens.append(MockToken(lower, "DET", is_stop=True))
            elif lower in {"aws", "sql"}:
                tokens.append(MockToken(lower, "PROPN"))
            else:
                tokens.append(MockToken(lower, "NOUN"))
        return MockDoc(tokens)

    mock_nlp = MagicMock(side_effect=make_doc)
    import app.core.skill_extractor as skill_extractor

    monkeypatch.setattr(skill_extractor, "_nlp", mock_nlp)
    return mock_nlp


@pytest.fixture
def sample_resume_1() -> str:
    path = DATA_DIR / "sample_resume_1.txt"
    return path.read_text(encoding="utf-8")


@pytest.fixture
def sample_resume_2() -> str:
    path = DATA_DIR / "sample_resume_2.txt"
    return path.read_text(encoding="utf-8")


@pytest.fixture
def sample_job_desc() -> str:
    path = DATA_DIR / "sample_job_desc.txt"
    return path.read_text(encoding="utf-8")
