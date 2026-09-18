import json
import streamlit as st
import pandas as pd

from services.resume_parser import analyze_resume
from services.job_discovery import discover_jobs
from services.matcher import (
    calculate_match,
    get_matched_skills,
    get_missing_skills,
)

from services.job_emailer import send_matching_job_alert


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# LOAD CANDIDATE PROFILE
# ============================================================

try:
    with open(
        "data/candidate.json",
        "r",
        encoding="utf-8"
    ) as file:

        candidate = json.load(file)

except FileNotFoundError:
    st.error("❌ data/candidate.json was not found.")
    st.stop()

except json.JSONDecodeError:
    st.error("❌ candidate.json contains invalid JSON.")
    st.stop()


# ============================================================
# INITIAL VALUES
# ============================================================

candidate_skills = candidate.get("skills", [])
target_roles = candidate.get("target_roles", [])
preferred_locations = candidate.get("preferred_locations", [])


# ============================================================
# HEADER
# ============================================================

st.title("🚀 CareerPilot AI")

st.subheader(
    "AI-Powered Job Discovery & Application Assistant"
)

st.write(
    """
    CareerPilot analyzes your resume, searches real job opportunities,
    calculates job-fit scores, identifies skill gaps and sends matching
    job alerts to your email.
    """
)


# ============================================================
# SIDEBAR - RESUME
# ============================================================

st.sidebar.header("📄 Resume Analyzer")

uploaded_resume = st.sidebar.file_uploader(
    "Upload your resume",
    type=["pdf"]
)


# ============================================================
# RESUME ANALYSIS
# ============================================================

if uploaded_resume:

    with st.spinner("🔍 Analyzing your resume..."):

        try:

            resume_profile = analyze_resume(
                uploaded_resume
            )

            st.sidebar.success(
                "✅ Resume analyzed successfully!"
            )

            # ----------------------------
            # Skills
            # ----------------------------

            detected_skills = resume_profile.get(
                "skills",
                []
            )

            if detected_skills:

                candidate["skills"] = detected_skills
                candidate_skills = detected_skills

            # ----------------------------
            # Education
            # ----------------------------

            education = resume_profile.get(
                "education",
                []
            )

            if education:

                if isinstance(
                    education,
                    list
                ):

                    candidate["education"] = ", ".join(
                        education
                    )

                else:

                    candidate["education"] = str(
                        education
                    )

            # ----------------------------
            # Email
            # ----------------------------

            email = resume_profile.get(
                "email"
            )

            if email:

                st.sidebar.write(
                    f"📧 {email}"
                )

            # ----------------------------
            # Phone
            # ----------------------------

            phone = resume_profile.get(
                "phone"
            )

            if phone:

                st.sidebar.write(
                    f"📱 {phone}"
                )

        except Exception as error:

            st.sidebar.error(
                f"❌ Resume analysis failed: {error}"
            )


# ============================================================
# SIDEBAR - CANDIDATE PROFILE
# ============================================================

st.sidebar.divider()

st.sidebar.header(
    "👤 Candidate Profile"
)

st.sidebar.write(
    f"**Name:** {candidate.get('name', 'Unknown')}"
)

st.sidebar.write(
    f"**Education:** "
    f"{candidate.get('education', 'Not detected')}"
)

st.sidebar.write(
    f"**Experience:** "
    f"{candidate.get('experience', 'Not specified')}"
)


# ============================================================
# SKILLS
# ============================================================

st.sidebar.subheader(
    "💻 Skills"
)

if candidate_skills:

    for skill in candidate_skills:

        st.sidebar.write(
            f"• {skill}"
        )

else:

    st.sidebar.warning(
        "No skills detected."
    )


# ============================================================
# TARGET ROLES
# ============================================================

st.sidebar.subheader(
    "🎯 Target Roles"
)

if target_roles:

    for role in target_roles:

        st.sidebar.write(
            f"• {role}"
        )

else:

    st.sidebar.warning(
        "No target roles specified."
    )


# ============================================================
# LOCATIONS
# ============================================================

st.sidebar.subheader(
    "📍 Preferred Locations"
)

if preferred_locations:

    for location in preferred_locations:

        st.sidebar.write(
            f"• {location}"
        )

else:

    st.sidebar.warning(
        "No preferred locations specified."
    )


# ============================================================
# SEARCH REAL JOBS
# ============================================================

st.header("🌐 Real Job Search")

st.write(
    """
    Click below to search for current job opportunities
    using your target roles and preferred locations.
    """
)

search_button = st.button(
    "🔍 Search Real Jobs",
    type="primary"
)


if search_button:

    with st.spinner(
        "🌐 Searching real job opportunities..."
    ):

        try:

            jobs = discover_jobs(
                preferred_locations=preferred_locations,
                target_roles=target_roles
            )

            # ------------------------------------------------
            # Convert to DataFrame
            # ------------------------------------------------

            if jobs is None:

                jobs = pd.DataFrame()

            elif not isinstance(
                jobs,
                pd.DataFrame
            ):

                jobs = pd.DataFrame(
                    jobs
                )

            # ------------------------------------------------
            # Save in session
            # ------------------------------------------------

            st.session_state["jobs"] = jobs

            # ------------------------------------------------
            # Status
            # ------------------------------------------------

            if jobs.empty:

                st.warning(
                    "⚠️ No real jobs found for the selected "
                    "roles and locations."
                )

                st.info(
                    "Try adding more target roles or locations "
                    "in data/candidate.json."
                )

            else:

                st.success(
                    f"✅ {len(jobs)} real jobs found!"
                )

        except Exception as error:

            st.error(
                "❌ Real job search failed."
            )

            st.exception(
                error
            )


# ============================================================
# LOAD JOBS FROM SESSION
# ============================================================

if "jobs" not in st.session_state:

    st.info(
        "👆 Click **Search Real Jobs** to find current openings."
    )

    st.stop()


jobs = st.session_state["jobs"]


# ============================================================
# CHECK JOB DATA
# ============================================================

if jobs is None or jobs.empty:

    st.warning(
        "⚠️ No jobs were returned."
    )

    st.stop()


# ============================================================
# FIX DATA TYPES
# ============================================================

if "id" in jobs.columns:

    jobs["id"] = jobs["id"].astype(str)


# ============================================================
# RAW JOB DATA
# ============================================================

with st.expander(
    "🔧 Developer: Raw Job Data"
):

    st.dataframe(
        jobs,
        width="stretch"
    )


# ============================================================
# JOB MATCHING
# ============================================================

results = []


for _, job in jobs.iterrows():

    # --------------------------------------------------------
    # Job skills
    # --------------------------------------------------------

    raw_skills = job.get(
        "skills",
        ""
    )

    if pd.isna(raw_skills):

        raw_skills = ""

    job_skills = [
        skill.strip()
        for skill in str(
            raw_skills
        ).split(",")
        if skill.strip()
    ]


    # --------------------------------------------------------
    # If API does not provide skills,
    # extract keywords from description
    # --------------------------------------------------------

    if not job_skills:

        description = str(
            job.get(
                "description",
                ""
            )
        )

        job_skills = [
            skill
            for skill in candidate_skills
            if skill.lower() in description.lower()
        ]


    # --------------------------------------------------------
    # Calculate match
    # --------------------------------------------------------

    score = calculate_match(
        candidate_skills,
        job_skills
    )


    # --------------------------------------------------------
    # Matched skills
    # --------------------------------------------------------

    matched = get_matched_skills(
        candidate_skills,
        job_skills
    )


    # --------------------------------------------------------
    # Missing skills
    # --------------------------------------------------------

    missing = get_missing_skills(
        candidate_skills,
        job_skills
    )


    # --------------------------------------------------------
    # Store
    # --------------------------------------------------------

    results.append({

        "id": str(
            job.get(
                "id",
                ""
            )
        ),

        "title": str(
            job.get(
                "title",
                "Unknown Position"
            )
        ),

        "company": str(
            job.get(
                "company",
                "Unknown Company"
            )
        ),

        "location": str(
            job.get(
                "location",
                "Unknown"
            )
        ),

        "experience": str(
            job.get(
                "experience",
                "Not specified"
            )
        ),

        "score": float(
            score
        ),

        "matched": matched,

        "missing": missing,

        "description": str(
            job.get(
                "description",
                ""
            )
        ),

        "url": str(
            job.get(
                "url",
                ""
            )
        )
    })


# ============================================================
# SORT BY MATCH SCORE
# ============================================================

results.sort(
    key=lambda job: job["score"],
    reverse=True
)


# ============================================================
# DASHBOARD
# ============================================================

st.divider()

st.header(
    "📊 Career Dashboard"
)


# ============================================================
# METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


# Jobs Found

with col1:

    st.metric(
        "Jobs Found",
        len(results)
    )


# High Match

with col2:

    high_match = sum(
        job["score"] >= 80
        for job in results
    )

    st.metric(
        "🔥 High Match",
        high_match
    )


# Average Match

with col3:

    if results:

        average_score = (
            sum(
                job["score"]
                for job in results
            )
            / len(results)
        )

    else:

        average_score = 0

    st.metric(
        "📊 Average Match",
        f"{average_score:.1f}%"
    )


# Weekly Goal

with col4:

    st.metric(
        "🎯 Weekly Goal",
        "100 Jobs"
    )


# ============================================================
# EMAIL ALERT
# ============================================================

st.divider()

st.header(
    "📧 Email Job Alerts"
)

st.write(
    """
    Send the matching real job opportunities to the
    email address configured in your `.env` file.
    """
)


email_button = st.button(
    "📨 Send Matching Jobs to Email"
)


if email_button:

    with st.spinner(
        "📨 Sending real job opportunities to email..."
    ):

        try:

            # Only send actual discovered jobs
            # and not test/example jobs.

            email_jobs = []

            for job in results:

                email_jobs.append({

                    "id": job["id"],

                    "title": job["title"],

                    "company": job["company"],

                    "location": job["location"],

                    "score": job["score"],

                    "url": job["url"]

                })


            if not email_jobs:

                st.warning(
                    "⚠️ No jobs available to email."
                )

            else:
                email_result = send_matching_job_alert(
                    email_jobs,
                    threshold=60
                )

                st.success(
                    "✅ Matching real jobs were sent to email!"
                )

                st.write(
                    email_result
                )

        except Exception as error:

            st.error(
                "❌ Email sending failed."
            )

            st.exception(
                error
            )


# ============================================================
# RECOMMENDED JOBS
# ============================================================

st.divider()

st.header(
    "🔥 Recommended Real Jobs"
)


for rank, job in enumerate(
    results,
    start=1
):

    # --------------------------------------------------------
    # Priority
    # --------------------------------------------------------

    if job["score"] >= 85:

        priority = "🔥 APPLY FIRST"

    elif job["score"] >= 70:

        priority = "🟢 APPLY"

    elif job["score"] >= 55:

        priority = "🟡 REVIEW"

    else:

        priority = "🔴 LOW MATCH"


    # --------------------------------------------------------
    # Job card
    # --------------------------------------------------------

    with st.container(
        border=True
    ):

        col1, col2 = st.columns(
            [4, 1]
        )


        # ----------------------------------------------------
        # Information
        # ----------------------------------------------------

        with col1:

            st.subheader(
                f"#{rank} "
                f"{job['title']} — "
                f"{job['company']}"
            )

            st.write(
                f"📍 **Location:** "
                f"{job['location']}"
            )

            st.write(
                f"💼 **Experience:** "
                f"{job['experience']}"
            )

            st.write(
                f"🎯 **Priority:** "
                f"{priority}"
            )


        # ----------------------------------------------------
        # Score
        # ----------------------------------------------------

        with col2:

            st.metric(
                "Job Match",
                f"{job['score']:.1f}%"
            )


        # ----------------------------------------------------
        # Matched Skills
        # ----------------------------------------------------

        st.write(
            "### ✅ Matched Skills"
        )

        if job["matched"]:

            matched_text = ", ".join(
                skill.title()
                for skill in job["matched"]
            )

            st.success(
                matched_text
            )

        else:

            st.write(
                "No matching skills found."
            )


        # ----------------------------------------------------
        # Skill Gaps
        # ----------------------------------------------------

        st.write(
            "### ⚠️ Skill Gaps"
        )

        if job["missing"]:

            missing_text = ", ".join(
                skill.title()
                for skill in job["missing"]
            )

            st.warning(
                missing_text
            )

        else:

            st.success(
                "🎉 You have all required skills!"
            )


        # ----------------------------------------------------
        # Description
        # ----------------------------------------------------

        if job["description"]:

            with st.expander(
                "📋 Job Description"
            ):

                st.write(
                    job["description"]
                )


        # ----------------------------------------------------
        # Apply
        # ----------------------------------------------------

        job_url = job["url"]

        if (
            isinstance(
                job_url,
                str
            )
            and job_url.startswith(
                "http"
            )
        ):

            st.link_button(
                "🔗 View / Apply for Job",
                job_url
            )

        else:

            st.warning(
                "🔗 Application link unavailable."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🚀 CareerPilot AI | "
    "Real Job Discovery • AI Matching • "
    "Email Job Alerts"
)