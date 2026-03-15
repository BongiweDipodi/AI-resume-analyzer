# README.md

# AI Resume Analyzer

## Project Overview

AI Resume Analyzer is an open-source tool designed to help job seekers evaluate how well their resumes match a specific job description. The system uses Natural Language Processing to extract skills from both the resume and job posting and produces a match score along with actionable suggestions.

## Features

* Resume parsing for **PDF and DOCX**
* NLP-based skill extraction using **spaCy**
* Job description analysis
* Resume-job **match scoring**
* Skill gap analysis
* Resume improvement suggestions

## Technology Stack

Frontend / Backend

* Streamlit

NLP

* spaCy

File Parsing

* pdfplumber
* python-docx

Utilities

* scikit-learn (optional similarity analysis)

## Installation

Clone repository

```
git clone https://github.com/BongiweDipodi/AI-resume-analyzer.git
cd ai-resume-analyzer
```

Install dependencies

```
pip install -r requirements.txt
```

Install spaCy model

```
python -m spacy download en_core_web_sm
```

Run the app

```
streamlit run app.py
```

## Usage

1. Upload resume (PDF or DOCX)
2. Paste job description
3. Click **Analyze Match**
4. View match score and improvement suggestions

## Contributors

- Mosa Dondolo — Resume Processing Pipeline
- Bongiwe Dipodi — Matching Engine & UI
