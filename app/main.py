"""Streamlit entry point for ResumeMatch AI."""

from __future__ import annotations

import io
import zipfile
from concurrent.futures import ProcessPoolExecutor
from typing import Any, Dict, List

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from fpdf import FPDF

from app.exceptions import (
    InvalidFileError,
    InvalidJobDescriptionError,
    InvalidResumeError,
)
from app.services.match_service import MatchEngine
from app.utils.file_handlers import parse_uploaded_file
from app.utils.validators import sanitize_text

GITHUB_URL = "https://github.com/BongiweDipodi/AI-resume-analyzer"
MAX_BATCH_WORKERS = 4
RATE_LIMIT = 50


@st.cache_resource
def get_engine() -> MatchEngine:
    """Cached MatchEngine instance."""
    return MatchEngine()


def _init_session_state() -> None:
    defaults = {
        "theme": "light",
        "request_count": 0,
        "last_resume_text": "",
        "last_job_text": "",
        "last_match_result": None,
        "last_strength_result": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value




def main() -> None:
    """Run Streamlit application."""
    st.set_page_config(
        page_title="ResumeMatch AI",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded",
    )


if __name__ == "__main__":
    main()
