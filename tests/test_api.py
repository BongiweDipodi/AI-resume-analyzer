"""Tests for FastAPI endpoints."""

from fastapi.testclient import TestClient

from app.api import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_resume_only() -> None:
    response = client.post(
        "/api/analyze",
        json={"resume_text": "Python SQL Docker. Master degree. 3 years experience."},
    )
    assert response.status_code == 200
    data = response.json()
    assert "skills" in data


def test_analyze_with_job() -> None:
    response = client.post(
        "/api/analyze",
        json={
            "resume_text": "Python SQL Docker Git. 4 years experience.",
            "job_description": "Python SQL AWS Docker required.",
        },
    )
    assert response.status_code == 200
    assert "match_score" in response.json()


def test_analyze_empty_resume_validation() -> None:
    response = client.post("/api/analyze", json={"resume_text": ""})
    assert response.status_code == 422


def test_analyze_whitespace_resume() -> None:
    response = client.post(
        "/api/analyze",
        json={"resume_text": "   ", "job_description": "Python SQL"},
    )
    assert response.status_code == 400
