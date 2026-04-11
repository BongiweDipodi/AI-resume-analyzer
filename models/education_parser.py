def detect_education_level(resume_text: str) -> str:
    """
    Detect the highest education level mentioned in a resume.

    Args:
        resume_text (str): Raw or cleaned resume text.

    Returns:
        str: One of "PhD", "Master", "Bachelor", "High School", or "Unknown".
    """
    text_lower = resume_text.lower()

    levels = {
        "PhD":         ["phd", "ph.d", "doctorate", "doctoral"],
        "Master":      ["master", "msc", "m.sc", "mba", "m.eng", "honours"],
        "Bachelor":    ["bachelor", "bsc", "b.sc", "btech", "b.tech",
                        "undergraduate", "degree"],
        "High School": ["matric", "high school", "grade 12", "secondary school"],
    }

    for level, keywords in levels.items():
        if any(kw in text_lower for kw in keywords):
            return level

    return "Unknown"


# ── Quick test ──
_edu_cases = [
    "Completed a Master of Science in Data Science at Wits University.",
    "BSc Computer Science, Unisa 2023",
    "Matric Certificate, Benoni High School 2018",
    "PhD in Artificial Intelligence, UCT",
]
# print("\n[Task 5 - education_parser]")
# for case in _edu_cases:
#     print(f"  Input : {case}")
#     print(f"  Output: {detect_education_level(case)}\n")
