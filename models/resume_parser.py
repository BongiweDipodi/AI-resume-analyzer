import re

def extract_resume_sections(resume_text):
    """
    Split resume into structured sections using heading keyword detection.

    Args:
        resume_text (str): Raw or cleaned resume text.

    Returns:
        dict: Keys = section names, values = section content strings.
    """
    sections = {"education": "", "experience": "", "skills": "", "projects": ""}

    section_keywords = {
        "education": ["education", "academic background", "qualifications"],
        "experience": ["experience", "work experience", "employment", "work history"],
        "skills":     ["skills", "technical skills", "core competencies"],
        "projects":   ["projects", "personal projects", "academic projects"],
    }

    lines = resume_text.split("\n")
    current_section = None

    for line in lines:
        stripped = line.strip()
        line_lower = stripped.lower()

        matched_heading = False
        for sec, keywords in section_keywords.items():
            if any(kw in line_lower for kw in keywords):
                current_section = sec
                matched_heading = True
                break

        if not matched_heading and current_section and stripped:
            sections[current_section] += stripped + "\n"

    for sec in sections:
        sections[sec] = sections[sec].strip()

    return sections

# ── Quick test ──
_test_resume = """
JOHN DOE — Software Engineer

EDUCATION
BSc Computer Science, Unisa | 2020-2023

WORK EXPERIENCE
Junior Developer | StartupX | 2023-2024
- Built REST APIs with FastAPI

TECHNICAL SKILLS
Python, SQL, Docker, Git

PROJECTS
Resume Analyzer — Python + Streamlit
"""

# _sections = extract_resume_sections(_test_resume)
# print("\n Resume_parser")
# for k, v in _sections.items():
#     print(f"\n[{k.upper()}]\n{v}")
