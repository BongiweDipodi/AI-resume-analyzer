import re

def clean_job_description(text: str) -> str:
    """
    Cleans raw job description text.
    - Lowercases all text
    - Removes punctuation
    - Removes extra spaces
    """
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)  
    text = re.sub(r"\s+", " ", text)     
    text = text.strip()
    return text

def clean_resume_text(text: str) -> str:
    """
    Clean and normalize resume text

    Args: text (str): Raw resume text

    Returns: Cleaned text (str)
    """

    text = text.lower()
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)
    # Remove speacial characters
    text = re.sub(r"[^a-zA-Z0-9\s\.\,\-\:]", "", text)
    text = text.strip()

    return text