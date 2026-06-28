"""Streamlit entry point for ResumeMatch AI."""

from __future__ import annotations

import io
import zipfile
from typing import Any, Dict, List
import unicodedata

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

GITHUB_URL = "https://github.com/dondolo2/AI-resume-analyzer"
RATE_LIMIT = 50


@st.cache_resource
def get_engine() -> MatchEngine:
    """Cached MatchEngine instance."""
    return MatchEngine()


def _init_session_state() -> None:
    defaults = {
        "theme": "dark",
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

    # Use basic Helvetica by default. Many resumes contain long dashes
    # and other Unicode characters which Helvetica doesn't support.
    # We'll normalize common problematic characters (em/en dashes, nbsp)
    # as a fallback so PDF generation doesn't raise on encode errors.
    pdf.set_font("Helvetica", "B", 16)
    # Title may contain safe characters; normalize it defensively too.
    safe_title = unicodedata.normalize("NFKD", title).replace("\u00A0", " ")
    safe_title = safe_title.replace("—", "-").replace("–", "-")
    pdf.cell(0, 10, safe_title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=11)

    def _sanitize_for_pdf(text: str) -> str:
        # Normalize and replace common unicode characters that default
        # PDF fonts don't support (em dash, en dash, non-breaking space).
        t = unicodedata.normalize("NFKD", text)
        t = t.replace("\u00A0", " ")
        t = t.replace("—", "-").replace("–", "-")
        # If other characters still can't be encoded by the PDF font,
        # fall back to replacing unencodable bytes with a placeholder.
        try:
            t.encode("latin-1")
            return t
        except UnicodeEncodeError:
            return t.encode("latin-1", errors="replace").decode("latin-1")

    for line in lines:
        safe_line = _sanitize_for_pdf(line)
        pdf.multi_cell(0, 8, safe_line)

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


def tab_strength() -> None:
    st.header("Resume Strength Checker")
    resume_file = st.file_uploader(
        "Upload resume",
        type=["pdf", "docx"],
        key="strength_resume",
    )
    if st.button("Check strength", type="primary"):
        if not resume_file:
            st.error("Upload a resume to continue.")
            return
        try:
            with st.spinner("Scoring resume strength..."):
                text = sanitize_text(_read_upload(resume_file))
                st.session_state.last_strength_result = cached_strength(text)
                st.session_state.last_resume_text = text
        except InvalidFileError as exc:
            st.error(str(exc))

    result = st.session_state.last_strength_result
    if not result:
        st.info("Upload a resume to see strength analysis.")
        return

    st.metric("Strength Score", f"{result['strength_score']}/100")
    _strength_radar(result, st.session_state.last_resume_text)
    for tip in result["feedback"]:
        if "Good" in tip or "Multiple" in tip:
            st.markdown(f"✅ {tip}")
        elif "No projects" in tip or "Quantify" in tip:
            st.markdown(f"❌ {tip}")
        else:
            st.markdown(f"💡 {tip}")

    report_lines = [f"Strength Score: {result['strength_score']}/100", ""] + result[
        "feedback"
    ]
    st.download_button(
        "Download PDF report",
        data=_pdf_report("Resume Strength Report", report_lines),
        file_name="resume_strength_report.pdf",
        mime="application/pdf",
    )


def tab_compare() -> None:
    st.header("Resume Comparison")
    col1, col2 = st.columns(2)
    with col1:
        f1 = st.file_uploader("Resume A", type=["pdf", "docx"], key="cmp_a")
    with col2:
        f2 = st.file_uploader("Resume B", type=["pdf", "docx"], key="cmp_b")
    if st.button("Compare resumes"):
        if not f1 or not f2:
            st.error("Upload both resumes.")
            return
        try:
            t1 = sanitize_text(_read_upload(f1))
            t2 = sanitize_text(_read_upload(f2))
            sim = cached_similarity(t1, t2)
            st.metric("Similarity", f"{sim:.2%}")
            table = pd.DataFrame(
                {
                    "Resume A": [len(t1.split()), len(set(t1.split()))],
                    "Resume B": [len(t2.split()), len(set(t2.split()))],
                },
                index=["Word count", "Unique words"],
            )
            st.dataframe(table, use_container_width=True)
        except InvalidFileError as exc:
            st.error(str(exc))


def tab_batch() -> None:
    st.header("Batch Ranking")
    files = st.file_uploader(
        "Upload resumes (multiple files or ZIP)",
        type=["pdf", "docx", "zip"],
        accept_multiple_files=True,
    )
    job_text = st.text_area("Job description", height=150, key="batch_job")
    if st.button("Rank candidates", type="primary"):
        if not files or not job_text.strip():
            st.error("Provide resumes and a job description.")
            return
        job_clean = sanitize_text(job_text)
        payloads: List[tuple] = []
        progress = st.progress(0.0)
        try:
            for uploaded in files:
                if uploaded.name.lower().endswith(".zip"):
                    zf = zipfile.ZipFile(io.BytesIO(uploaded.getvalue()))
                    for name in zf.namelist():
                        if name.lower().endswith((".pdf", ".docx")):
                            text = parse_uploaded_file(zf.read(name), name)
                            payloads.append((name, sanitize_text(text), job_clean))
                else:
                    text = sanitize_text(_read_upload(uploaded))
                    payloads.append((uploaded.name, text, job_clean))
        except InvalidFileError as exc:
            st.error(str(exc))
            return

        if not payloads:
            st.warning("No valid resumes found in upload.")
            return

        scores: Dict[str, float] = {}
        engine = get_engine()
        for i, (name, text, job) in enumerate(payloads, start=1):
            scores[name] = engine.match_resume_to_job(text, job)["match_score"]
            progress.progress(i / len(payloads))

        ranking = get_engine().rank_resumes(scores)
        df = pd.DataFrame(ranking)
        st.dataframe(df, use_container_width=True)
        if ranking:
            top = ranking[0]
            st.success(
                f"Top candidate: **{top['candidate']}** with {top['score']}% match"
            )


def main() -> None:
    """Run Streamlit application."""
    st.set_page_config(
        page_title="ResumeMatch AI",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _init_session_state()
    _render_sidebar()

    st.title("🎯 ResumeMatch AI")
    st.caption("Production-grade resume analysis, matching, and ranking")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Single Match",
            "Strength Checker",
            "Compare Resumes",
            "Batch Ranking",
        ]
    )
    with tab1:
        tab_single_match()
    with tab2:
        tab_strength()
    with tab3:
        tab_compare()
    with tab4:
        tab_batch()


if __name__ == "__main__":
    main()
