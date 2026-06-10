"""Resume Match AI application package."""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_SKILL_DICT_PATH = DATA_DIR / "skills_list.json"

SPACY_MODEL = os.getenv("SPACY_MODEL", "en_core_web_sm")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))

__all__ = [
    "DATA_DIR",
    "DEFAULT_SKILL_DICT_PATH",
    "MAX_FILE_SIZE",
    "PROJECT_ROOT",
    "SPACY_MODEL",
]
