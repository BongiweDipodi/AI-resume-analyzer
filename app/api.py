"""FastAPI endpoints for external integrations."""

from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.exceptions import InvalidJobDescriptionError, InvalidResumeError
from app.services.match_service import MatchEngine

app = FastAPI(
    title="ResumeMatch AI API",
    description="Analyze resumes and job descriptions programmatically.",
    version="1.0.0",
)
engine = MatchEngine()


class AnalyzeRequest(BaseModel):
    """Request body for resume analysis."""

    resume_text: str = Field(..., min_length=1)
    job_description: Optional[str] = None


@app.get("/health")
def health() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/api/analyze")
def analyze(payload: AnalyzeRequest) -> Dict[str, Any]:
    """Analyze resume, optionally against a job description.

    Args:
        payload: Resume text and optional job description.

    Returns:
        Analysis results.
    """
    try:
        if payload.job_description:
            return engine.match_resume_to_job(
                payload.resume_text,
                payload.job_description,
            )
        return engine.analyze_resume(payload.resume_text)
    except (InvalidResumeError, InvalidJobDescriptionError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
