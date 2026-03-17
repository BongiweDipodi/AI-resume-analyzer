import spacy

nlp = spacy.load("en_core_web_sm")

def process_job_description(jd_text: str):
    """
    Task 1: Processes raw job description text into a list of 
    cleaned, meaningful keywords.
    """
    doc = nlp(jd_text) 
    
    keywords = []
    for token in doc:
        # 1. Skip stop words and punctuation
        if token.is_stop or token.is_punct:
            continue
            
        # 2. Handle Proper Nouns (like AWS, Python, SQL) - Keep exact text
        if token.pos_ == "PROPN":
            keywords.append(token.text.lower())
            
        # 3. Handle regular Nouns (like developer, experience) - Use lemma
        elif token.pos_ == "NOUN":
            keywords.append(token.lemma_.lower())
            

    return sorted(list(set(keywords)))

if __name__ == "__main__":
    sample_jd = "I am a Java developer with experience in AWS and SQL."
    result = process_job_description(sample_jd)
    print(f"Extracted Keywords: {result}")
