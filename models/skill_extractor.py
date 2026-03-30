import spacy

nlp = spacy.load("en_core_web_sm")

def extract_job_skills(job_description: str) -> list:
    """
    Extracts meaningful keywords from a job description.
    Returns a list of skills/keywords.
    """
    doc = nlp(job_description)
    keywords = []

    for token in doc:
        if token.is_stop or token.is_punct:
            continue

        # Proper nouns (technologies)
        if token.pos_ == "PROPN":
            keywords.append(token.text.lower())
        # Nouns, adjectives, verbs
        elif token.pos_ in ["NOUN", "ADJ", "VERB"]:
            keywords.append(token.lemma_.lower())

    return sorted(list(set(keywords)))

# Example usage
if __name__ == "__main__":
    jd = "Python developer with AWS, SQL, and cloud computing experience."
    print(extract_job_skills(jd))


    import json, os, re
    from utils.text_cleaner import clean_resume_text

# In the real project this loads from data/skills_list.json
# For testing, we define a small inline dictionary
_SKILL_DICT = {
    "python", "sql", "machine learning", "docker", "git",
    "javascript", "react", "node js", "aws", "azure",
    "tensorflow", "pandas", "numpy", "scikit learn", "streamlit",
    "java", "c++", "kubernetes", "flask", "fastapi",
    "data analysis", "deep learning", "nlp", "computer vision",
}

def extract_resume_skills(resume_text: str, skill_dict: set = _SKILL_DICT) -> list:
    """
    Extract known skills from resume text using a predefined skill dictionary.

    Args:
        resume_text (str): Cleaned resume text.
        skill_dict  (set): Set of known skill strings (lowercase).

    Returns:
        list: Matched skills found in the text.
    """
    cleaned = clean_resume_text(resume_text)
    found = []
    for skill in skill_dict:
        # Match whole skill phrase (not as a substring of another word)
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, cleaned):
            found.append(skill)
    return sorted(found)


# ── Quick test ──
_skill_input = "Experienced in Python, SQL, Machine Learning, Docker and Git."
_skills_found = extract_resume_skills(_skill_input)
# print("\n[Task 3 - skill_extractor]")
# print("Input :", _skill_input)
# print("Skills:", _skills_found)
# Expected → ['docker', 'git', 'machine learning', 'python', 'sql']
