import os
import json

from openai import OpenAI


# ============================================================
# OPENAI CLIENT
# ============================================================

def get_client():

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not configured."
        )

    return OpenAI(
        api_key=api_key
    )


# ============================================================
# ANALYZE JOB
# ============================================================

def analyze_job(
    job_title,
    company,
    job_description,
    candidate_skills
):

    client = get_client()

    prompt = f"""
You are an expert technical recruiter.

Analyze this job for a candidate.

JOB TITLE:
{job_title}

COMPANY:
{company}

JOB DESCRIPTION:
{job_description}

CANDIDATE SKILLS:
{", ".join(candidate_skills)}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "required_skills": [],
    "preferred_skills": [],
    "responsibilities": [],
    "experience_required": "",
    "seniority": "",
    "job_category": "",
    "candidate_matching_skills": [],
    "candidate_missing_skills": [],
    "fit_score": 0,
    "reason": "",
    "recommendation": ""
}}

Rules:

1. fit_score must be between 0 and 100.
2. Consider semantic similarity, not only exact keywords.
3. Do not invent candidate skills.
4. Clearly distinguish required and preferred skills.
5. recommendation should be one of:
   "APPLY"
   "REVIEW"
   "SKIP"
"""


    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[

            {
                "role": "system",
                "content": (
                    "You are a professional recruitment "
                    "and job matching AI."
                )
            },

            {
                "role": "user",
                "content": prompt
            }

        ],

        temperature=0
    )


    content = response.choices[0].message.content

    # --------------------------------------------------------
    # Remove markdown JSON formatting if returned
    # --------------------------------------------------------

    content = content.strip()

    if content.startswith("```"):

        content = content.replace(
            "```json",
            ""
        )

        content = content.replace(
            "```",
            ""
        )

        content = content.strip()


    # --------------------------------------------------------
    # Convert JSON
    # --------------------------------------------------------

    try:

        result = json.loads(
            content
        )

    except json.JSONDecodeError:

        raise ValueError(
            "AI returned invalid JSON."
        )


    return result