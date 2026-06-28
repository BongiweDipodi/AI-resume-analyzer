"""Resume feedback and improvement suggestions."""

from typing import List


def generate_resume_feedback(missing_skills: List[str]) -> List[str]:
    """Generate actionable feedback based on missing skills.

    Args:
        missing_skills: Skills required by job but absent from resume.

    Returns:
        List of feedback strings.
    """
    if not missing_skills:
        return ["Great match! Your resume already aligns well with this job."]

    skills_str = ", ".join(missing_skills)
    return [
        "Add or strengthen these skills in your resume: "
        f"{skills_str}. Consider including projects or experience that "
        "demonstrate these skills."
    ]


def generate_keyword_suggestions(missing_skills: List[str]) -> List[str]:
    """Suggest exact keywords to add based on job skill gaps.

    Args:
        missing_skills: Skills missing from the resume.

    Returns:
        Keyword optimization suggestions.
    """
    if not missing_skills:
        return ["Your resume already includes the main job keywords."]
    return [
        f"Add the keyword '{skill}' in your skills or experience section."
        for skill in missing_skills[:10]
    ]


def generate_cover_letter_draft(
    missing_skills: List[str],
    job_title: str = "this role",
) -> str:
    """Generate a basic cover letter using missing skills as talking points.

    Args:
        missing_skills: Skills to address in the letter.
        job_title: Target job title phrase.

    Returns:
        Cover letter draft text.
    """
    skills_clause = (
        ", ".join(missing_skills[:5]) if missing_skills else "the required stack"
    )
    return (
        f"Dear Hiring Manager,\n\n"
        f"I am excited to apply for {job_title}. My background aligns closely "
        f"with your needs, and I am actively strengthening skills such as "
        f"{skills_clause} through hands-on projects and continuous learning.\n\n"
        "I would welcome the opportunity to discuss how I can "
        "contribute to your team.\n\n"
        f"Sincerely,\n[Your Name]"
    )
