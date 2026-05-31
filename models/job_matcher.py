from utils.text_cleaner import clean_resume_text
from models.skill_extractor import extract_job_skills as extract_skills


def extract_job_skills(job_description: str) -> list:
    """
    Extract skills from a job description.
    
    Args:
        job_description (str): Raw job description text
    
    Returns:
        list: Skills extracted from the job description
    """
    cleaned_jd = clean_resume_text(job_description)
    job_skills = extract_skills(cleaned_jd)
    
    return job_skills


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


def remove_duplicate_skills(skills: list) -> list:
    """
    Ensure skills list contains unique values.
    
    Args:
        skills (list): List of skills that may contain duplicates
    
    Returns:
        list: List of unique skills
    """
    return list(set(skills))


def sort_skills(skills: list) -> list:
    """
    Sort skills alphabetically.
    
    Args:
        skills (list): List of skills to sort
    
    Returns:
        list: Sorted skills in alphabetical order
    """
    return sorted(skills)


if __name__ == "__main__":
    resume = ["Python", "Java", "AWS"]
    job = ["Python", "AWS", "SQL", "Cloud"]
    print(match_resume_to_job(resume, job))