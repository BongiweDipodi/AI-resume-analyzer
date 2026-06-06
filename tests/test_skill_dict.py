"""Tests for skill dictionary loading."""

import json
from pathlib import Path

import pytest

from app.core.skill_extractor import load_skill_dict
from app.exceptions import SkillDictionaryError


def test_load_skill_dict_success(tmp_path: Path) -> None:
    path = tmp_path / "skills.json"
    path.write_text(json.dumps(["python", "sql"]), encoding="utf-8")
    skills = load_skill_dict(path)
    assert skills == {"python", "sql"}


def test_load_skill_dict_missing_file() -> None:
    with pytest.raises(SkillDictionaryError):
        load_skill_dict("/nonexistent/skills.json")


def test_load_skill_dict_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("not json", encoding="utf-8")
    with pytest.raises(SkillDictionaryError):
        load_skill_dict(path)


def test_load_skill_dict_wrong_shape(tmp_path: Path) -> None:
    path = tmp_path / "obj.json"
    path.write_text(json.dumps({"a": 1}), encoding="utf-8")
    with pytest.raises(SkillDictionaryError):
        load_skill_dict(path)
