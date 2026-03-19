def match_resume_to_job(resume_skills: list, job_skills: list) -> dict:
    """
    Compares resume skills with job skills.
    Returns matched and missing skills.
    """
    resume_set = set([skill.lower() for skill in resume_skills])
    job_set = set([skill.lower() for skill in job_skills])

    matched_skills = list(resume_set & job_set)
    missing_skills = list(job_set - resume_set)

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }


if __name__ == "__main__":
    resume = ["Python", "Java", "AWS"]
    job = ["Python", "AWS", "SQL", "Cloud"]
    print(match_resume_to_job(resume, job))