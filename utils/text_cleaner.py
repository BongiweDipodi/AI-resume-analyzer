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

