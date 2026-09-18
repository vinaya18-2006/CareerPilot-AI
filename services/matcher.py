import re


# ============================================================
# SKILL DATABASE
# ============================================================

SKILL_DATABASE = [

    "python",
    "java",
    "c++",
    "javascript",
    "typescript",

    "sql",
    "mysql",
    "postgresql",
    "mongodb",

    "html",
    "css",
    "react",
    "node.js",
    "fastapi",
    "django",
    "flask",

    "aws",
    "azure",
    "gcp",

    "docker",
    "kubernetes",
    "linux",

    "git",
    "github",

    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",

    "machine learning",
    "deep learning",
    "artificial intelligence",

    "power bi",
    "tableau",
    "excel",

    "data analysis",
    "data engineering",
    "etl",

    "rest api",
    "api",

    "spark",
    "hadoop",

    "terraform",

    "salesforce",
    "sap"
]


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    if not text:

        return ""

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9+#.\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


# ============================================================
# EXTRACT SKILLS
# ============================================================

def extract_skills(text):

    text = normalize_text(
        text
    )

    found = []

    for skill in SKILL_DATABASE:

        skill_normalized = normalize_text(
            skill
        )

        if skill_normalized in text:

            found.append(
                skill
            )

    return sorted(
        list(
            set(found)
        )
    )


# ============================================================
# MATCH SKILLS
# ============================================================

def get_matched_skills(
    candidate_skills,
    job_skills
):

    candidate = set(
        normalize_text(skill)
        for skill in candidate_skills
    )

    job = set(
        normalize_text(skill)
        for skill in job_skills
    )

    return sorted(
        candidate.intersection(
            job
        )
    )


# ============================================================
# MISSING SKILLS
# ============================================================

def get_missing_skills(
    candidate_skills,
    job_skills
):

    candidate = set(
        normalize_text(skill)
        for skill in candidate_skills
    )

    job = set(
        normalize_text(skill)
        for skill in job_skills
    )

    return sorted(
        job.difference(
            candidate
        )
    )


# ============================================================
# MATCH SCORE
# ============================================================

def calculate_match(
    candidate_skills,
    job_skills
):

    candidate = set(
        normalize_text(skill)
        for skill in candidate_skills
    )

    job = set(
        normalize_text(skill)
        for skill in job_skills
    )

    if not job:

        return 0


    matched = candidate.intersection(
        job
    )


    score = (
        len(matched)
        /
        len(job)
    ) * 100


    return round(
        score,
        2
    )


# ============================================================
# DECISION
# ============================================================

def get_recommendation(
    score
):

    if score >= 75:

        return "APPLY"

    elif score >= 50:

        return "REVIEW"

    else:

        return "SKIP"