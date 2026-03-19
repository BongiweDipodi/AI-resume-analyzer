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