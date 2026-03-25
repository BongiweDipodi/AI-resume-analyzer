def calculate_match_score(matched_skills: list, job_skills: list) -> float:
    """
    Calculates match percentage between resume and job skills.
    """
    if not job_skills:
        return 0.0

    score = (len(matched_skills) / len(job_skills)) * 100
    return round(score, 2)

def generate_resume_feedback(missing_skills: list) -> list:

    if not missing_skills:
        return ["Great match! Your resume already aligns well with this job."]

    suggestions = []

    skills_str = ", ".join(missing_skills)

    suggestions.append(
        f"Add or strengthen these skills in your resume: {skills_str}. Consider including projects or experience that demonstrate these skills."
    )

    return suggestions

if __name__ == "__main__":
    missing = ["sql", "docker"]
    feedback = generate_resume_feedback(missing)
    print(feedback)