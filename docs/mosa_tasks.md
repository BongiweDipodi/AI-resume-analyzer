# Developer Task Guide – Mosa

**Goal:** Build the Core Resume Intelligence Engine

**Duration:** 2 weeks

This module will be responsible for **processing resumes, extracting information, scoring candidates, and powering the AI logic of the platform.**

---

# WEEK 1 – Resume Intelligence Pipeline

## Task 1: Resume Text Cleaner

File: `utils/text_cleaner.py`

Create function:

```
clean_resume_text(text)
```

Responsibilities:

• Remove extra whitespace
• Remove special characters
• Convert to lowercase
• Normalize punctuation

Example Output:

```
Input:
"Python, SQL,  Data Analysis!!!"

Output:
"python sql data analysis"
```

---

## Task 2: Resume Section Extractor

File: `models/resume_parser.py`

Create function:

```
extract_resume_sections(resume_text)
```

Goal:

Split resume into structured sections.

Expected Output:

```
{
 "education": "...",
 "experience": "...",
 "skills": "...",
 "projects": "..."
}
```

Hint:

Use regex or keyword detection.

---

## Task 3: Skill Extraction Engine

File: `models/skill_extractor.py`

Create function:

```
extract_skills(resume_text)
```

Use:

• spaCy NLP pipeline
• Predefined skill dictionary

Return:

```
["python", "sql", "machine learning"]
```

---

## Task 4: Experience Years Estimator

File: `models/experience_analyzer.py`

Create function:

```
estimate_experience_years(resume_text)
```

Goal:

Detect years of experience mentioned in resume.

Example:

```
"3 years experience with Python"
"Worked as developer from 2021 - 2024"
```

Output:

```
3
```

---

## Task 5: Education Level Detector

File: `models/education_parser.py`

Create function:

```
detect_education_level(resume_text)
```

Possible Outputs:

```
"High School"
"Bachelor"
"Master"
"PhD"
```

Use keyword detection.

---

# WEEK 2 – Resume Scoring & Intelligence

## Task 6: Resume Skill Vectorization

File: `models/vectorizer.py`

Create function:

```
vectorize_skills(skill_list)
```

Goal:

Convert skills into a vector representation.

Example:

```
["python", "sql", "ml"]
```

Output:

```
[1,0,1,0,1]
```

Use:

• `sklearn CountVectorizer`
or
• `TF-IDF`

---

## Task 7: Resume Ranking System

File: `models/resume_ranker.py`

Create function:

```
rank_resumes(resume_scores)
```

Example:

```
{
 "candidate1": 82,
 "candidate2": 65,
 "candidate3": 91
}
```

Output sorted ranking.

---

## Task 8: Resume Similarity Engine

File: `models/similarity_engine.py`

Create function:

```
calculate_resume_similarity(resume1, resume2)
```

Use:

• Cosine similarity
• TF-IDF vectors

Output:

```
0.83 similarity score
```

---

## Task 9: Skill Gap Analysis

File: `models/skill_gap.py`

Create function:

```
identify_skill_gap(candidate_skills, job_skills)
```

Output:

```
{
 "matched": [...],
 "missing": [...]
}
```

---

## Task 10: Resume Strength Analyzer

File: `models/resume_strength.py`

Create function:

```
analyze_resume_strength(resume_text)
```

Score based on:

• Skill diversity
• Experience mentions
• Education level
• Project mentions

Output:

```
{
 "strength_score": 78,
 "feedback": [...]
}
```

---

# WEEK 3 – Advanced Intelligence

## Task 11: Keyword Optimization Detector

File: `models/keyword_optimizer.py`

Create function:

```
detect_missing_keywords(resume_text, job_description)
```

Goal:

Check if resume includes **important job keywords**.

Output:

```
["docker", "kubernetes"]
```

---

## Task 12: Resume ATS Compatibility Checker

File: `models/ats_checker.py`

Create function:

```
check_ats_compatibility(resume_text)
```

Detect:

• tables
• images
• unusual formatting

Return:

```
ATS score (0–100)
```

---

## Task 13: Resume Improvement Suggestions

File: `models/resume_improver.py`

Create function:

```
generate_resume_improvements(resume_analysis)
```

Output:

```
[
 "Add more measurable achievements",
 "Include project section",
 "Mention frameworks used"
]
```

---

# WEEK 4 – Visualization Layer

## Task 14: Candidate Score Dashboard

Inside `app.py`

Display:

```
Resume Score
Experience Years
Education Level
Skill Coverage
```

Use:

```
st.metric()
st.progress()
st.bar_chart()
```

---

## Task 15: Resume Skill Visualization

Create:

```
plot_skill_distribution(skill_list)
```

Display chart:

```
Python          ███████
SQL             █████
MachineLearning ████
```

Use:

• matplotlib
• seaborn

---

# Final Deliverable

The system should allow:

1. Upload resume
2. Extract skills
3. Analyze experience
4. Compare with job
5. Calculate score
6. Show improvement suggestions
7. Display results in dashboard

