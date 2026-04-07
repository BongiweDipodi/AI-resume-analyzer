from sklearn.feature_extraction.text import CountVectorizer

def vectorize_skills(skill_list: list, vocabulary: list = None) -> list:
    """
    Convert a list of skills into a binary vector.

    If a vocabulary is provided, the vector matches that fixed skill set.
    Otherwise, the vocabulary is built from the input itself.

    Args:
        skill_list (list): Skills to vectorize (e.g. ["python", "sql"]).
        vocabulary (list): Optional fixed vocabulary for consistent vectors.

    Returns:
        list: Binary vector (1 = skill present, 0 = absent).
    """

    if not skill_list:
        return []
    
    text = " ".join(skill_list)

    if vocabulary:
        vectorizer = CountVectorizer(vocabulary=vocabulary)
    else:
        vocabulary = CountVectorizer()

    matrix = vectorizer.fit_transform([text])
    return matrix.toarray()[0].tolist()

# ── Quick test ──
_vocab     = ["python", "sql", "ml", "docker", "git"]
_candidate = ["python", "ml", "git"]
_vector    = vectorize_skills(_candidate, vocabulary=_vocab)
# print("\n[Task 6 - vectorizer]")
# print("Vocabulary:", _vocab)
# print("Candidate :", _candidate)
# print("Vector    :", _vector)
# Expected → [1, 0, 1, 0, 1]
