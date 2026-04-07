from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_resume_similarity(resume1: str, resume2: str) -> float:
    """
    Calculate cosine similarity between two resume texts using TF-IDF.

    Args:
        resume1 (str): First resume text.
        resume2 (str): Second resume text.

    Returns:
        float: Similarity score between 0.0 and 1.0.
    """
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume1, resume2])
    score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
    
    return round(float(score[0][0]), 4)

# ── Quick test ──
_r1 = "Python SQL Machine Learning Data Analysis"
_r2 = "Python SQL Deep Learning Data Science"
_sim = calculate_resume_similarity(_r1, _r2)
# print("\n[Task 8 - similarity_engine]")
# print(f"Resume 1: {_r1}")
# print(f"Resume 2: {_r2}")
# print(f"Similarity: {_sim}")
# Expected → something around 0.4–0.7 (high overlap, some differences)
