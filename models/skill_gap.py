def identify_skill_gap(candidate_skills: list, job_skills: list) -> dict:
    """
    Identify matched and missing skills between a candidate and a job.

    Args:
        candidate_skills (list): Skills the candidate has.
        job_skills       (list): Skills the job requires.

    Returns:
        dict: {"matched": [...], "missing": [...]}
    """
    
    candidate_set = set(s.lower() for s in candidate_skills)
    job_set = set(s.lower() for s in job_skills)
    
    return {
        "matched": sorted(candidate_set & job_set),
        "missing": sorted(job_set - candidate_set)
    }
    
    # ── Quick test ──
_candidate_skills = ["python", "sql", "machine learning", "git"]
_job_skills       = ["python", "sql", "docker", "aws", "machine learning"]
_gap = identify_skill_gap(_candidate_skills, _job_skills)
print("\n[Task 9 - skill_gap]")
print("Matched:", _gap["matched"])
print("Missing:", _gap["missing"])
# Expected → matched: ['machine learning', 'python', 'sql']
#            missing: ['aws', 'docker']
