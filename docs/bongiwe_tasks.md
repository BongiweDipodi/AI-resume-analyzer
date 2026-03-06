# Bongiwe's Task Guide: Job Matching & Resume Analysis

**Goal:** Build the matching engine that compares extracted resume skills with job requirements, produces a match score, and displays results in an interactive dashboard.

**Duration:** 2 Weeks

---

# Week 1: Job Description Processing

## Task 1: Job Description Cleaner

Reuse the existing text cleaning logic to normalize job descriptions before skill extraction.

**File:** `utils/text_cleaner.py`

```python
from utils.text_cleaner import clean_resume_text

def clean_job_description(text):
    """Clean and normalize job description text."""
    return clean_resume_text(text)
```

**Purpose**

* Normalize job descriptions
* Remove punctuation and symbols
* Prepare text for NLP processing

---

## Task 2: Job Skill Extraction

Extract required skills from the job description using the same NLP pipeline used for resumes.

**File:** `models/job_matcher.py`

```python
from utils.text_cleaner import clean_resume_text
from models.skill_extractor import extract_resume_skills

def extract_job_skills(job_description):
    """Extract skills from a job description."""
    
    cleaned_jd = clean_resume_text(job_description)
    job_skills = extract_resume_skills(cleaned_jd)

    return job_skills
```

**Purpose**

* Convert job description into normalized text
* Reuse the existing skill extraction module
* Return detected job skills

---

## Task 3: Skill Matching Engine

This function compares resume skills with job skills.

**File:** `models/job_matcher.py`

```python
def match_resume_to_job(resume_skills, job_skills):
    """Compare resume skills against job requirements."""

    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched_skills = list(resume_set.intersection(job_set))
    missing_skills = list(job_set.difference(resume_set))

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }
```

**Purpose**

* Identify overlapping skills
* Detect missing skills
* Return structured comparison data

---

## Task 4: Remove Duplicate Skills

Ensure the final skills list does not contain duplicates.

**File:** `models/job_matcher.py`

```python
def remove_duplicate_skills(skills):
    """Ensure skills list contains unique values."""
    return list(set(skills))
```

**Purpose**

* Improve accuracy of comparisons
* Avoid duplicate skill matches
* Clean up output

---

## Task 5: Sort Skills for Display

Sort matched and missing skills alphabetically to improve readability.

```python
def sort_skills(skills):
    """Sort skills alphabetically."""
    return sorted(skills)
```

**Purpose**

* Improve UI presentation
* Ensure consistent results

---

# Week 2: Scoring & Analysis

## Task 6: Match Score Calculation

Calculate how well the resume matches the job.

**File:** `models/job_matcher.py`

```python
def calculate_match_score(matched_skills, job_skills):
    """Calculate match percentage."""

    if len(job_skills) == 0:
        return 0

    score = (len(matched_skills) / len(job_skills)) * 100
    return round(score, 2)
```

**Purpose**

* Provide a numeric measure of resume-job compatibility
* Convert matching skills into a percentage score

---

## Task 7: Resume Feedback Generator

Generate suggestions for improving the resume.

**File:** `models/resume_scorer.py`

```python
def generate_resume_feedback(missing_skills):
    """Generate suggestions for resume improvement."""

    suggestions = []

    if not missing_skills:
        suggestions.append(
            "Excellent match. Your resume covers all required skills."
        )
    else:
        for skill in missing_skills[:5]:
            suggestions.append(
                f"Consider adding experience with {skill}"
            )

    return suggestions
```

**Purpose**

* Provide actionable suggestions
* Highlight missing skills

---

## Task 8: Resume Strength Analysis

Identify the strongest areas of the resume.

**File:** `models/resume_scorer.py`

```python
def identify_strengths(matched_skills):
    """Identify strongest skills in the resume."""

    if not matched_skills:
        return ["No strong skill matches found"]

    return matched_skills[:5]
```

**Purpose**

* Show candidates what they already do well
* Reinforce positive feedback

---

## Task 9: Resume Weakness Analysis

Highlight missing capabilities.

```python
def identify_weaknesses(missing_skills):
    """Highlight missing required skills."""

    if not missing_skills:
        return ["No major skill gaps detected"]

    return missing_skills[:5]
```

**Purpose**

* Identify gaps between resume and job requirements
* Support targeted resume improvement

---

# Week 2: Streamlit Dashboard

## Task 10: Display Match Results

Create the UI components that display the analysis.

**File:** `app.py`

```python
import streamlit as st

st.title("AI Resume Analyzer")

st.metric("Match Score", f"{match_score}%")

st.progress(match_score / 100)

st.subheader("Matched Skills")
st.write(matched_skills)

st.subheader("Missing Skills")
st.write(missing_skills)

st.subheader("Suggestions")
st.write(feedback)
```

---

## Task 11: Skill Visualization

Display skill counts using simple charts.

```python
st.subheader("Skill Comparison")

skill_data = {
    "Matched Skills": len(matched_skills),
    "Missing Skills": len(missing_skills)
}

st.bar_chart(skill_data)
```

**Purpose**

* Provide visual insight into the match quality
* Make results easier to interpret

---

## Task 12: User Input Interface

Add inputs for uploading resumes and entering job descriptions.

```python
uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

job_description = st.text_area("Paste Job Description")
```

**Purpose**

* Allow user interaction
* Capture inputs for analysis

---

# Final Output

The system should generate structured analysis results:

```python
{
    "match_score": 82.5,
    "matched_skills": ["python", "sql", "machine learning"],
    "missing_skills": ["docker", "aws"],
    "suggestions": [
        "Consider adding experience with docker",
        "Consider adding experience with aws"
    ]
}
```

---

# Shared Variable Naming Convention

| Variable         | Type  | Description                               |
| ---------------- | ----- | ----------------------------------------- |
| `resume_skills`  | list  | Skills extracted from resume              |
| `job_skills`     | list  | Skills extracted from job description     |
| `matched_skills` | list  | Skills present in both resume and job     |
| `missing_skills` | list  | Skills required but not present in resume |
| `match_score`    | float | Resume-job match percentage               |
| `feedback`       | list  | Suggestions for improving the resume      |
