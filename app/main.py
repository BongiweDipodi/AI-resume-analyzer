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


def _strength_radar(result: Dict[str, Any], resume_text: str) -> None:
    engine = get_engine()
    skills = engine.analyze_resume(resume_text)
    years = skills["experience_years"]
    edu_map = {
        "PhD": 100,
        "Master": 80,
        "Bachelor": 60,
        "High School": 40,
        "Unknown": 20,
    }
    edu_score = edu_map.get(skills["education"], 20)
    skill_score = min(len(skills["skills"]) * 10, 100)
    exp_score = min(years * 15, 100)
    project_score = 100 if "—" in resume_text or "–" in resume_text else 40

    fig = go.Figure(
        data=go.Scatterpolar(
            r=[skill_score, exp_score, edu_score, project_score],
            theta=["Skills", "Experience", "Education", "Projects"],
            fill="toself",
            name="Resume",
        )
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)


def _pdf_report(title: str, lines: List[str]) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=11)
    for line in lines:
        pdf.multi_cell(0, 8, line)
    return bytes(pdf.output())


def _render_sidebar() -> None:
    with st.sidebar:
        st.title("ResumeMatch AI")
        theme = st.toggle("Dark mode", value=st.session_state.theme == "dark")
        st.session_state.theme = "dark" if theme else "light"
        st.markdown(f"[GitHub Repository]({GITHUB_URL})")
        with st.expander("About"):
            st.markdown("""
                **Tech stack:** Python, Streamlit, spaCy, scikit-learn,
                pandas, pdfplumber, Plotly, pytest, GitHub Actions
                """)
        st.caption(f"Session requests: {st.session_state.request_count}/{RATE_LIMIT}")


def tab_single_match() -> None:
    st.header("Single Resume Analysis")
    resume_file = st.file_uploader(
        "Upload resume (PDF/DOCX)",
        type=["pdf", "docx"],
        key="single_resume",
    )
    job_text = st.text_area(
        "Job description",
        height=180,
        placeholder="Paste the job description here...",
    )
    if st.button("Analyze", type="primary", use_container_width=True):
        if not _check_rate_limit():
            return
        if not resume_file:
            st.error("Please upload a resume file.")
            return
        if not job_text.strip():
            st.error("Please paste a job description.")
            return
        try:
            with st.spinner("Analyzing resume against job description..."):
                resume_text = _read_upload(resume_file)
                resume_text = sanitize_text(resume_text)
                job_clean = sanitize_text(job_text)
                result = cached_match(resume_text, job_clean)
                st.session_state.last_match_result = result
                st.session_state.last_resume_text = resume_text
                st.session_state.last_job_text = job_clean
        except (
            InvalidFileError,
            InvalidResumeError,
            InvalidJobDescriptionError,
        ) as exc:
            st.error(str(exc))
            return

    result = st.session_state.last_match_result
    if not result:
        st.info("Upload a resume and job description, then click Analyze.")
        return

    score = result["match_score"]
    st.metric(
        "Match Score", f"{score}%", help="Percentage of job skills found on resume"
    )
    st.progress(min(score / 100.0, 1.0))
    if score > 90:
        st.balloons()
        st.success("Excellent match! You are a top candidate for this role.")
    elif score >= 70:
        st.info("Solid match — consider addressing missing skills below.")
    else:
        st.warning("Low match — focus on the missing skills and ATS tips.")

    _skills_chart(result["matched_skills"], result["missing_skills"])

    with st.expander("Detected skills"):
        st.dataframe(
            pd.DataFrame({"skill": result["resume_skills"]}),
            use_container_width=True,
        )
    with st.expander("Education & experience"):
        st.write(f"**Education:** {result['education']}")
        st.write(f"**Experience:** ~{result['experience_years']} year(s)")
    with st.expander("Resume strength & ATS"):
        st.write(f"**ATS simulation score:** {result['ats_score']}%")
        bench = result["industry_benchmark"]
        st.write(
            f"**Industry benchmark:** {bench['percentile_label']} "
            f"(benchmark {bench['benchmark_score']}%)"
        )
        for tip in result["feedback"]:
            st.markdown(f"- {tip}")
        st.markdown("**Keyword suggestions**")
        for kw in result["keyword_suggestions"]:
            st.markdown(f"- {kw}")
    with st.expander("Cover letter draft"):
        st.text_area("Draft", result["cover_letter_draft"], height=200)



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
