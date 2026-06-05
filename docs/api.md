# API Reference

## MatchEngine (`app.services.match_service`)

Central orchestrator for all analysis workflows.

| Method | Description |
|--------|-------------|
| `analyze_resume(resume_text)` | Skills, education, experience, sections |
| `analyze_job(job_desc)` | Job skills and cleaned text |
| `match_resume_to_job(resume_text, job_desc)` | Full match score, gaps, ATS, feedback |
| `analyze_strength(resume_text)` | 4-dimension strength score |
| `compare_resumes(r1, r2)` | TF-IDF cosine similarity (0–1) |
| `rank_resumes(scores)` | Sorted candidate leaderboard |
| `estimate_ats_score(resume_text, job_skills)` | Rule-based ATS simulation |
| `compare_to_benchmark(score, industry)` | Industry percentile label |

## Core modules (`app.core`)

| Module | Functions |
|--------|-----------|
| `text_cleaner` | `clean_resume_text`, `clean_job_description` |
| `skill_extractor` | `load_skill_dict`, `extract_resume_skills`, `extract_job_skills` |
| `education_parser` | `detect_education_level` |
| `experience_analyzer` | `estimate_experience_years` |
| `resume_parser` | `extract_resume_sections` |
| `match_scoring` | `calculate_match_score`, `match_resume_to_job`, `identify_skill_gap` |
| `similarity_engine` | `calculate_resume_similarity` |
| `resume_ranker` | `rank_resumes` |
| `strength_analyzer` | `analyze_resume_strength` |
| `vectorizer` | `vectorize_skills` |

## Feedback (`app.services.feedback_service`)

- `generate_resume_feedback(missing_skills)`
- `generate_keyword_suggestions(missing_skills)`
- `generate_cover_letter_draft(missing_skills, job_title)`

## File utilities (`app.utils`)

- `parse_pdf(file, filename)` / `parse_docx(file, filename)`
- `parse_uploaded_file(file, filename)`
- `validate_file_upload(filename, file_size, content_type)`
- `sanitize_text(text, max_length)`

## REST API (`app.api`)

### `GET /health`

Returns `{ "status": "ok" }`.

### `POST /api/analyze`

**Body:**

```json
{
  "resume_text": "string (required)",
  "job_description": "string (optional)"
}
```

If `job_description` is omitted, returns resume analysis only. Otherwise returns full match payload (score, gaps, ATS, suggestions).

## Exceptions (`app.exceptions`)

- `InvalidResumeError`
- `InvalidJobDescriptionError`
- `InvalidFileError`
- `SkillDictionaryError`
