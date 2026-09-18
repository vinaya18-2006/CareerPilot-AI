from services.matcher import (
    extract_skills,
    calculate_match,
    get_matched_skills,
    get_missing_skills,
    get_recommendation
)


resume = """
Python developer with experience in Python,
SQL, AWS, Azure, Docker, Git, Pandas,
NumPy and Power BI.
"""


job = """
We are looking for a Python Developer.

Requirements:

Python
SQL
AWS
Docker
Kubernetes
FastAPI
Git
Machine Learning
"""


candidate_skills = extract_skills(
    resume
)

job_skills = extract_skills(
    job
)


matched = get_matched_skills(
    candidate_skills,
    job_skills
)


missing = get_missing_skills(
    candidate_skills,
    job_skills
)


score = calculate_match(
    candidate_skills,
    job_skills
)


recommendation = get_recommendation(
    score
)


print("\n==============================")
print("CAREERPILOT MATCH TEST")
print("==============================")

print(
    "\nCandidate skills:"
)

print(
    candidate_skills
)


print(
    "\nJob skills:"
)

print(
    job_skills
)


print(
    "\nMatched skills:"
)

print(
    matched
)


print(
    "\nMissing skills:"
)

print(
    missing
)


print(
    "\nMatch score:"
)

print(
    f"{score}%"
)


print(
    "\nRecommendation:"
)

print(
    recommendation
)