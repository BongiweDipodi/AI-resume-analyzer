import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from skill_extractor import extract_resume_skills
    from experience_analyzer import estimate_experience_years
    from education_parser import detect_education_level
except ImportError:
    from .skill_extractor import extract_resume_skills
    from .experience_analyzer import estimate_experience_years
    from .education_parser import detect_education_level
import re

def analyze_resume_strength(resume_text: str) -> dict:
    """
    Score a resume's overall strength across four dimensions.

    Scoring breakdown (100 points total):
        • Skill diversity  - up to 40 pts (4 pts per unique skill, max 10)
        • Experience       - up to 30 pts (5 pts per year detected, max 6 yrs)
        • Education        - up to 20 pts (PhD=20, Master=16, Bachelor=12,
                                           High School=6, Unknown=0)
        • Projects         - up to 10 pts (5 pts if mentioned, +5 if 2+ found)

    Args:
        resume_text (str): Raw resume text.

    Returns:
        dict: {"strength_score": int (0-100), "feedback": [str, ...]}
    """
    
    feedback = []
    score = 0
    
    # Skill diversity (40 pts)
    skills = extract_resume_skills(resume_text)
    skill_pts = min(len(skills), 10) * 4
    score += skill_pts
    if len(skills) < 5:
        feedback.append("Add more technical skills to strengthen your profile.")
    else:
        feedback.append(f"Good skill diversity — {len(skills)} skills detected.")

    # Experience (30 pts)
    years = estimate_experience_years(resume_text)
    exp_pts = min(years, 6) * 5
    score += exp_pts
    if years == 0:
        feedback.append("Quantify your experience (e.g. '2 years of Python').")
    else:
        feedback.append(f"Experience detected: ~{years} year(s).")

    # Education (20 pts)
    edu = detect_education_level(resume_text)
    edu_points = {"PhD": 20, "Master": 16, "Bachelor": 12, "High School": 6, "Unknown": 0}
    score += edu_points[edu]
    feedback.append(f"Education level detected: {edu}.")

    # Projects (10 pts)
    # Count actual project entries (lines with em-dashes or similar separators)
    project_entries = len(re.findall(r"—|–", resume_text))  # Count em-dashes or en-dashes
    if project_entries >= 2:
        score += 10
        feedback.append("Multiple projects found - great for showcasing work.")
    elif project_entries >= 1:
        score += 5
        feedback.append("Consider adding more projects to your resume.")
    else:
        feedback.append("No projects section detected - consider adding one.")

    return {"strength_score": min(score, 100), "feedback": feedback}


# ── Quick test ──
_strength_resume = """
John Doe — BSc Computer Science

EXPERIENCE
Developer at TechCo 2022-2024 (2 years experience with Python)
Intern at DataLab 2021-2022

TECHNICAL SKILLS
Python, SQL, Machine Learning, Docker, Git, Flask

PROJECTS
Resume Analyzer — Streamlit + Python
Data Dashboard — Pandas + Plotly
"""
_strength = analyze_resume_strength(_strength_resume)
print("\n[Task 10 - resume_strength]")
print("Strength Score:", _strength["strength_score"])
print("Feedback:")
for tip in _strength["feedback"]:
    print(" •", tip)
