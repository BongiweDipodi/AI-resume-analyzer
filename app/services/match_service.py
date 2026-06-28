"""Central orchestrator for resume-job matching and analysis."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Set

from app import DEFAULT_SKILL_DICT_PATH
from app.core.education_parser import detect_education_level
from app.core.experience_analyzer import estimate_experience_years
from app.core.match_scoring import calculate_match_score, identify_skill_gap
from app.core.match_scoring import match_resume_to_job as match_skill_lists
from app.core.resume_parser import extract_resume_sections
from app.core.resume_ranker import rank_resumes
from app.core.similarity_engine import calculate_resume_similarity
from app.core.skill_extractor import (
    extract_job_skills,
    extract_resume_skills,
    load_skill_dict,
)
from app.core.strength_analyzer import analyze_resume_strength
from app.core.text_cleaner import clean_job_description, clean_resume_text
from app.exceptions import InvalidJobDescriptionError, InvalidResumeError
from app.services.feedback_service import (
    generate_cover_letter_draft,
    generate_keyword_suggestions,
    generate_resume_feedback,
)

logger = logging.getLogger(__name__)

BENCHMARKS: Dict[str, float] = {
    "data_science": 72.0,
    "software_engineering": 68.0,
    "general": 65.0,
}


class MatchEngine:
    """Orchestrates resume analysis, job matching, and ranking."""

    def __init__(self, skill_dict_path: str | Path | None = None) -> None:
        """Initialize engine with skill dictionary path.

        Args:
            skill_dict_path: Path to skills_list.json. Uses project default if None.
        """
        path = Path(skill_dict_path) if skill_dict_path else DEFAULT_SKILL_DICT_PATH
        self.skill_dict: Set[str] = load_skill_dict(path)
        logger.info("MatchEngine loaded %d skills", len(self.skill_dict))

    def _validate_resume(self, resume_text: str) -> str:
        if resume_text is None or not str(resume_text).strip():
            raise InvalidResumeError("Resume text cannot be empty.")
        return clean_resume_text(resume_text)

    def _validate_job(self, job_desc: str) -> str:
        if job_desc is None or not str(job_desc).strip():
            raise InvalidJobDescriptionError("Job description cannot be empty.")
        return clean_job_description(job_desc)

    def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """Extract structured insights from a resume.

        Args:
            resume_text: Raw resume text.

        Returns:
            Dict with skills, education, experience years, and sections.
        """
        cleaned = self._validate_resume(resume_text)
        return {
            "skills": extract_resume_skills(cleaned, self.skill_dict),
            "education": detect_education_level(cleaned),
            "experience_years": estimate_experience_years(cleaned),
            "sections": extract_resume_sections(resume_text),
        }

    def analyze_job(self, job_desc: str) -> Dict[str, Any]:
        """Extract skills and keywords from a job description.

        Args:
            job_desc: Raw job description text.

        Returns:
            Dict with cleaned text and extracted skills.
        """
        cleaned = self._validate_job(job_desc)
        resume_aligned = extract_resume_skills(cleaned, self.skill_dict)
        nlp_skills = extract_job_skills(job_desc)
        combined = sorted(set(resume_aligned) | set(nlp_skills))
        return {"cleaned_text": cleaned, "skills": combined}

    def match_resume_to_job(self, resume_text: str, job_desc: str) -> Dict[str, Any]:
        """Full match analysis between resume and job description.

        Args:
            resume_text: Raw resume text.
            job_desc: Raw job description.

        Returns:
            Match score, gaps, feedback, ATS score, and suggestions.
        """
        resume_analysis = self.analyze_resume(resume_text)
        job_analysis = self.analyze_job(job_desc)
        resume_skills = resume_analysis["skills"]
        job_skills = job_analysis["skills"]

        gap = identify_skill_gap(resume_skills, job_skills)
        match = match_skill_lists(resume_skills, job_skills)
        score = calculate_match_score(gap["matched"], job_skills)

        return {
            "match_score": score,
            "matched_skills": match["matched_skills"],
            "missing_skills": match["missing_skills"],
            "gap": gap,
            "resume_skills": resume_skills,
            "job_skills": job_skills,
            "education": resume_analysis["education"],
            "experience_years": resume_analysis["experience_years"],
            "feedback": generate_resume_feedback(match["missing_skills"]),
            "keyword_suggestions": generate_keyword_suggestions(
                match["missing_skills"]
            ),
            "ats_score": self.estimate_ats_score(resume_text, job_skills),
            "industry_benchmark": self.compare_to_benchmark(score),
            "cover_letter_draft": generate_cover_letter_draft(
                match["missing_skills"],
                job_title="the position",
            ),
        }

    def analyze_strength(self, resume_text: str) -> Dict[str, Any]:
        """Analyze overall resume strength.

        Args:
            resume_text: Raw resume text.

        Returns:
            Strength score and dimensional feedback.
        """
        self._validate_resume(resume_text)
        return analyze_resume_strength(resume_text)

    def compare_resumes(self, resume1: str, resume2: str) -> float:
        """Compute TF-IDF similarity between two resumes.

        Args:
            resume1: First resume text.
            resume2: Second resume text.

        Returns:
            Cosine similarity score 0.0–1.0.
        """
        return calculate_resume_similarity(resume1, resume2)

    def rank_resumes(self, resume_scores: Dict[str, float]) -> List[Dict[str, Any]]:
        """Rank candidates by match score.

        Args:
            resume_scores: Candidate name to score mapping.

        Returns:
            Sorted ranking entries.
        """
        return rank_resumes(resume_scores)

    def estimate_ats_score(self, resume_text: str, job_skills: List[str]) -> float:
        """Estimate ATS pass likelihood using rule-based scoring.

        Args:
            resume_text: Raw resume text.
            job_skills: Skills required by the job.

        Returns:
            ATS score from 0.0 to 100.0.
        """
        cleaned = clean_resume_text(resume_text).lower()
        score = 40.0
        if len(cleaned) > 200:
            score += 15.0
        if any(h in cleaned for h in ("experience", "education", "skills")):
            score += 15.0
        if job_skills:
            hits = sum(1 for s in job_skills if s in cleaned)
            score += min(30.0, (hits / len(job_skills)) * 30.0)
        if "@" in resume_text or "email" in cleaned:
            score += 5.0
        return round(min(score, 100.0), 2)

    def compare_to_benchmark(
        self,
        match_score: float,
        industry: str = "general",
    ) -> Dict[str, Any]:
        """Compare match score against a simulated industry benchmark.

        Args:
            match_score: Calculated match percentage.
            industry: Benchmark key (data_science, software_engineering, general).

        Returns:
            Benchmark comparison details.
        """
        benchmark = BENCHMARKS.get(industry, BENCHMARKS["general"])
        percentile = "Top 25%" if match_score >= benchmark + 10 else "Average"
        if match_score < benchmark - 10:
            percentile = "Below average"
        return {
            "industry": industry,
            "benchmark_score": benchmark,
            "your_score": match_score,
            "percentile_label": percentile,
        }
