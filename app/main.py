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


def _check_rate_limit() -> bool:
    st.session_state.request_count += 1
    if st.session_state.request_count > RATE_LIMIT:
        st.error("Session rate limit reached. Please refresh the page.")
        return False
    return True


def _read_upload(uploaded_file) -> str:
    """Parse uploaded resume file to text."""
    data = uploaded_file.getvalue()
    return parse_uploaded_file(data, uploaded_file.name)


@st.cache_data(show_spinner=False)
def cached_match(resume_text: str, job_text: str) -> Dict[str, Any]:
    """Cached full match analysis."""
    return get_engine().match_resume_to_job(resume_text, job_text)


@st.cache_data(show_spinner=False)
def cached_strength(resume_text: str) -> Dict[str, Any]:
    """Cached strength analysis."""
    return get_engine().analyze_strength(resume_text)


@st.cache_data(show_spinner=False)
def cached_similarity(text_a: str, text_b: str) -> float:
    """Cached resume similarity."""
    return get_engine().compare_resumes(text_a, text_b)


def _skills_chart(matched: List[str], missing: List[str]) -> None:
    df = pd.DataFrame(
        {
            "Category": ["Matched", "Missing"],
            "Count": [len(matched), len(missing)],
        }
    )
    st.bar_chart(df.set_index("Category"))





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
