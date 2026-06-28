"""Application package entry point and shared constants."""

from __future__ import annotations

from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_ROOT.parent
DEFAULT_SKILL_DICT_PATH = PROJECT_ROOT / "data" / "skills_list.json"
SPACY_MODEL = "en_core_web_sm"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

__all__ = [
    "DEFAULT_SKILL_DICT_PATH",
    "SPACY_MODEL",
    "MAX_FILE_SIZE",
]
