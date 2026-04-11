def rank_resumes(resume_scores: dict) -> list:
    """
    Rank candidates from highest to lowest score.

    Args:
        resume_scores (dict): {candidate_name: score} mapping.

    Returns:
        list: Sorted list of (rank, name, score) tuples.
    """

    sorted_candidates = sorted(resume_scores.items(), key=lambda x: x[1], reverse=True)

    return [
        {"rank": i + 1, "candidate": name, "score": score}
        for i, (name, score) in enumerate(sorted_candidates)
    ]
    
# ── Quick test ──
_scores = {"Alice": 82, "Bob": 65, "Carol": 91, "Dave": 74}
_ranking = rank_resumes(_scores)
# print("\n[Task 7 - resume_ranker]")
# for entry in _ranking:
#     print(f"  #{entry['rank']}  {entry['candidate']:10s}  {entry['score']}%")
# Expected → Carol 91, Alice 82, Dave 74, Bob 65
