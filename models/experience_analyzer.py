import re

def estimate_experience_years(resume_text: str) -> int:
    """
    Estimate total years of experience mentioned in a resume.

    Strategy:
        1. Look for "X years" patterns (e.g. "3 years of experience").
        2. Look for year ranges (e.g. "2019 - 2024") and sum durations.
        3. Return the largest single value found.

    Args:
        resume_text (str): Raw or cleaned resume text.

    Returns:
        int: Estimated years of experience (0 if none detected).
    """
    text_lower = resume_text.lower()

    # Pattern 1: "3 years" / "three years"
    word_to_num = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    }
    explicit_years = []

    digit_matches = re.findall(r"(\d+)\s+year", text_lower)
    explicit_years += [int(y) for y in digit_matches]

    for word, num in word_to_num.items():
        if re.search(rf"\b{word}\s+year", text_lower):
            explicit_years.append(num)

    # Pattern 2: year ranges like "2019 - 2024" or "2021–Present"
    current_year = 2025
    range_total = 0
    range_matches = re.findall(
        r"(20\d{2}|19\d{2})\s*[-–—to]+\s*(20\d{2}|19\d{2}|present)", text_lower
    )
    for start, end in range_matches:
        end_year = current_year if end == "present" else int(end)
        duration = end_year - int(start)
        if 0 < duration <= 50:           # sanity check
            range_total += duration

    all_estimates = explicit_years + ([range_total] if range_total > 0 else [])
    return max(all_estimates) if all_estimates else 0


# ── Quick test ──
_exp_text = """
Worked as developer from 2021 - 2024.
Also had 3 years experience with Python.
Internship at DataCo 2019–2020.
"""
# _years = estimate_experience_years(_exp_text)
# print("\n[Task 4 - experience_analyzer]")
# print("Input :", _exp_text.strip())
# print("Output:", _years, "years")
# # Expected → 3 (largest explicit match wins)
