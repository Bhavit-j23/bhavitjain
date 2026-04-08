import pandas as pd
import os
import re

from pyswarm import pso
import PyPDF2
import docx


# ---------------- READ FILES ----------------

def read_txt(path):
    with open(path, "r", errors="ignore") as f:
        return f.read().lower()


def read_pdf(path):
    text = ""

    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text.lower()

    return text


def read_docx(path):
    doc = docx.Document(path)

    text = ""

    for para in doc.paragraphs:
        text += para.text.lower() + " "

    return text


def read_file(path):

    if path.endswith(".txt"):
        return read_txt(path)

    elif path.endswith(".pdf"):
        return read_pdf(path)

    elif path.endswith(".docx"):
        return read_docx(path)

    return ""


# ---------------- FEATURE EXTRACTION ----------------

def extract_features(jd_text, resume_text):

    jd_words = set(jd_text.split())
    resume_words = set(resume_text.split())

    # skill matching score
    common_words = jd_words.intersection(resume_words)

    if len(jd_words) == 0:
        skill_score = 0
    else:
        skill_score = len(common_words) / len(jd_words)

    # experience score
    experience_score = 0

    years = re.findall(r"(\d+)\s+year", resume_text)

    if years:
        max_year = max([int(y) for y in years])
        experience_score = min(max_year / 10, 1)

    # education score
    education_keywords = [
        "btech",
        "mtech",
        "bca",
        "mca",
        "bachelor",
        "master",
        "phd"
    ]

    education_score = 0

    for word in education_keywords:
        if word in resume_text:
            education_score = 1
            break

    return skill_score, experience_score, education_score


# ---------------- PSO FITNESS FUNCTION ----------------

def fitness(weights, features):

    skill_w = weights[0]
    exp_w = weights[1]
    edu_w = weights[2]

    total = 0

    for skill, exp, edu in features:

        score = (
            skill_w * skill +
            exp_w * exp +
            edu_w * edu
        )

        total += score

    # PSO minimizes value
    return -total


# ---------------- MAIN RANK FUNCTION ----------------

def rank_resumes(jd_path, resume_paths):

    jd_text = read_file(jd_path)

    features = []
    names = []

    for path in resume_paths:

        resume_text = read_file(path)

        skill_score, experience_score, education_score = extract_features(
            jd_text,
            resume_text
        )

        features.append(
            (
                skill_score,
                experience_score,
                education_score
            )
        )

        names.append(os.path.basename(path))

    # PSO optimize weights
    lower_bounds = [0, 0, 0]
    upper_bounds = [1, 1, 1]

    best_weights, _ = pso(
        lambda w: fitness(w, features),
        lower_bounds,
        upper_bounds,
        swarmsize=30,
        maxiter=50
    )

    skill_w = best_weights[0]
    exp_w = best_weights[1]
    edu_w = best_weights[2]

    scores = []

    for skill, exp, edu in features:

        final_score = (
            skill_w * skill +
            exp_w * exp +
            edu_w * edu
        ) * 100

        scores.append(round(final_score, 2))

    df = pd.DataFrame({
        "Resume": names,
        "Score (%)": scores
    })

    df = df.sort_values(
        by="Score (%)",
        ascending=False
    )

    df["Rank"] = range(1, len(df) + 1)

    df = df[
        ["Rank", "Resume", "Score (%)"]
    ]

    return df