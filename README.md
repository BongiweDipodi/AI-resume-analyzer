# AI Resume Analyzer

## Project Overview

AI Resume Analyzer is a Python application that analyzes a candidate's resume and compares it to a job description to determine how well the resume matches the job requirements.

The system extracts skills from the resume using Natural Language Processing (NLP) and compares them to the required skills in the job description.

It then generates:

- Resume Match Score
- Matched Skills
- Missing Skills
- Resume Improvement Suggestions

The application is built using Streamlit to create an interactive web interface.

---

## Tech Stack

Python

Streamlit – User interface

spaCy – Natural language processing

pdfplumber – PDF text extraction

python-docx – Word document parsing

scikit-learn – similarity calculations

---

## Features

Resume Upload (PDF or DOCX)

Automatic Resume Text Extraction

Skill Extraction using NLP

Job Description Analysis

Resume-Job Skill Matching

Match Score Calculation

Resume Feedback Generator

Interactive Results Dashboard

---

## Project Structure

app.py → Streamlit application

utils/ → File parsing and text cleaning

models/ → AI processing logic

data/ → Skills dataset

docs/ → task guides for developers

tests/ → test scripts

---

## Installation

Clone the repository

Install dependencies

pip install -r requirements.txt

Run the application

streamlit run app.py

---

## Example Workflow

1 Upload resume

2 Paste job description

3 Click analyze

4 System extracts skills

5 Resume compared to job requirements

6 Match score and suggestions displayed

---

## Contributors

Bongiwe Dipodi

Mosa Dondolo