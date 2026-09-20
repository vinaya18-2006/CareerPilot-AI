import os
import json
import time

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from services.job_discovery import discover_jobs
from services.email_service import send_job_email


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

SENT_FILE = "data/sent_jobs.json"

DEFAULT_ROLES = [
    "Python Developer",
    "Software Engineer",
    "Data Analyst",
    "Data Engineer",
    "Cloud Engineer",
    "AI Engineer"
]

DEFAULT_LOCATIONS = [
    "Bangalore",
    "Chennai",
    "Hyderabad",
    "Remote"
]

SKILLS = [
    "python",
    "sql",
    "aws",
    "azure",
    "power bi",
    "pandas",
    "numpy",
    "machine learning",
    "django",
    "flask",
    "fastapi",
    "git",
    "github",
    "linux",
    "html",
    "css",
    "javascript",
    "data analysis",
    "computer vision"
]


# ============================================================
# DARK DASHBOARD STYLE
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #080b12;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    [data-testid="stSidebar"] {
        background-color: #0d111c;
    }

    [data-testid="stMetric"] {
        background-color: #111827;
        border: 1px solid #263044;
        border-radius: 18px;
        padding: 20px;
    }

    [data-testid="stMetricValue"] {
        color: white;
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8;
    }

    .stButton > button {
        border-radius: 12px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "jobs" not in st.session_state:
    st.session_state.jobs = pd.DataFrame()

if "last_search" not in st.session_state:
    st.session_state.last_search = None

if "email_status" not in st.session_state:
    st.session_state.email_status = "Waiting for job search"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_candidate():

    if os.path.exists("candidate.json"):

        try:

            with open(
                "candidate.json",
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except Exception:
            pass

    return {
        "name": "Vinaya",
        "education": "B.E. Computer Science and Engineering",
        "experience": "Fresher",
        "skills": [
            "Python",
            "SQL",
            "AWS",
            "Azure",
            "Power BI",
            "Pandas",
            "NumPy",
            "Git",
            "Linux"
        ],
        "target_roles": DEFAULT_ROLES,
        "preferred_locations": DEFAULT_LOCATIONS
    }


def load_sent_jobs():

    if not os.path.exists(SENT_FILE):
        return set()

    try:

        with open(
            SENT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return set(json.load(file))

    except Exception:

        return set()


def save_sent_jobs(sent_jobs):

    os.makedirs(
        "data",
        exist_ok=True
    )

    with open(
        SENT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            list(sent_jobs),
            file,
            indent=2
        )


def calculate_match_score(
    job,
    candidate_skills
):

    text = " ".join(
        [
            str(job.get("title", "")),
            str(job.get("description", "")),
            str(job.get("skills", "")),
            str(job.get("company", ""))
        ]
    ).lower()

    candidate_skills = [
        str(skill).lower()
        for skill in candidate_skills
    ]

    matched = []

    for skill in SKILLS:

        if skill in text:

            if (
                skill in candidate_skills
                or skill in [
                    "machine learning",
                    "data analysis",
                    "computer vision"
                ]
            ):

                matched.append(skill)

    score = min(
        100,
        round(
            (len(matched) / 7) * 100,
            2
        )
    )

    return score, matched


def process_jobs(
    jobs,
    candidate
):

    if jobs is None:
        return pd.DataFrame()

    if jobs.empty:
        return pd.DataFrame()

    results = []

    for _, job in jobs.iterrows():

        score, matched = calculate_match_score(
            job,
            candidate.get("skills", [])
        )

        job_data = job.to_dict()

        job_data["score"] = score

        job_data["matched_skills"] = (
            ", ".join(matched)
        )

        results.append(job_data)

    result_df = pd.DataFrame(results)

    if not result_df.empty:

        result_df = result_df.sort_values(
            by="score",
            ascending=False
        ).reset_index(drop=True)

    return result_df


def get_job_id(job):

    return str(
        job.get("id")
        or job.get("url")
        or (
            str(job.get("title", ""))
            +
            str(job.get("company", ""))
        )
    )


def send_new_jobs(jobs):

    if jobs.empty:
        return 0

    sent_jobs = load_sent_jobs()

    new_jobs = []

    for _, job in jobs.iterrows():

        job_id = get_job_id(job)

        if job_id not in sent_jobs:

            new_jobs.append(
                job.to_dict()
            )

    if not new_jobs:
        return 0

    success = send_job_email(
        pd.DataFrame(new_jobs)
    )

    if not success:
        return 0

    for job in new_jobs:

        sent_jobs.add(
            get_job_id(job)
        )

    save_sent_jobs(sent_jobs)

    return len(new_jobs)


# ============================================================
# LOAD CANDIDATE
# ============================================================

candidate = load_candidate()

candidate_name = candidate.get(
    "name",
    "Candidate"
)

candidate_skills = candidate.get(
    "skills",
    []
)

target_roles = candidate.get(
    "target_roles",
    DEFAULT_ROLES
)

preferred_locations = candidate.get(
    "preferred_locations",
    DEFAULT_LOCATIONS
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🚀 CareerPilot AI")

    st.caption(
        "Intelligent Career Assistant"
    )

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Overview",
            "🔎 Job Search",
            "🎯 Matching Jobs",
            "📊 Analytics",
            "📄 Resume Analyzer",
            "👤 Candidate Profile",
            "📧 Email Alerts"
        ]
    )

    st.divider()

    st.subheader("👤 Candidate")

    st.write(
        f"**Name:** {candidate_name}"
    )

    st.write(
        "**Education:** B.E. Computer Science"
    )

    st.write(
        "**Experience:** Fresher"
    )

    st.divider()

    st.subheader("🛠️ Core Skills")

    for skill in candidate_skills[:8]:

        st.write(
            f"• {skill}"
        )


# ============================================================
# TOP HEADER
# ============================================================

st.title("🚀 CareerPilot AI")

st.subheader(
    "AI-Powered Job Discovery & Application Assistant"
)

st.caption(
    "Discover real jobs • Analyze career fit • Track opportunities • "
    "Receive automated job alerts"
)

st.success(
    "● REAL-TIME CAREER INTELLIGENCE ACTIVE"
)

st.divider()


# ============================================================
# OVERVIEW
# ============================================================

if page == "🏠 Overview":

    st.header(
        "📊 Career Intelligence Overview"
    )

    jobs = st.session_state.jobs

    total_jobs = len(jobs)

    if total_jobs > 0:

        high_matches = int(
            (jobs["score"] >= 60).sum()
        )

        average_score = round(
            jobs["score"].mean()
        )

        excellent_matches = int(
            (jobs["score"] >= 80).sum()
        )

    else:

        high_matches = 0
        average_score = 0
        excellent_matches = 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "💼 Jobs Found",
            total_jobs
        )

    with col2:

        st.metric(
            "🎯 High Matches",
            high_matches
        )

    with col3:

        st.metric(
            "📈 Average Match",
            f"{average_score}%"
        )

    with col4:

        st.metric(
            "🔥 80%+ Matches",
            excellent_matches
        )

    st.write("")

    left, right = st.columns(
        [1.7, 1]
    )

    with left:

        st.subheader(
            "🎯 Career Match Performance"
        )

        if jobs.empty:

            st.info(
                "No job data yet. Go to **Job Search** and "
                "search for real opportunities."
            )

        else:

            chart_data = jobs[
                ["title", "score"]
            ].head(10).copy()

            chart_data["title"] = (
                chart_data["title"]
                .astype(str)
                .str[:35]
            )

            chart_data = chart_data.set_index(
                "title"
            )

            st.bar_chart(
                chart_data,
                height=350
            )

    with right:

        st.subheader(
            "🤖 System Status"
        )

        st.success(
            "Job Discovery: ACTIVE"
        )

        st.success(
            "AI Matching: ACTIVE"
        )

        st.success(
            "Gmail Alerts: ACTIVE"
        )

        st.success(
            "GitHub Scheduler: ACTIVE"
        )

        st.write("")

        st.info(
            "Jobs are discovered from Adzuna "
            "and matching opportunities can be "
            "sent automatically to your Gmail."
        )


# ============================================================
# JOB SEARCH
# ============================================================

elif page == "🔎 Job Search":

    st.header(
        "🔎 Real-Time Job Discovery"
    )

    st.write(
        "Search current job opportunities using "
        "your preferred roles and locations."
    )

    col1, col2 = st.columns(2)

    with col1:

        selected_roles = st.multiselect(
            "🎯 Target Roles",
            target_roles,
            default=target_roles[:3]
        )

    with col2:

        selected_locations = st.multiselect(
            "📍 Preferred Locations",
            preferred_locations,
            default=preferred_locations[:2]
        )

    st.write("")

    search_clicked = st.button(
        "🚀 SEARCH REAL JOBS",
        use_container_width=True
    )

    if search_clicked:

        if not selected_roles:

            st.warning(
                "Please select at least one target role."
            )

        elif not selected_locations:

            st.warning(
                "Please select at least one location."
            )

        else:

            progress = st.progress(
                0
            )

            status = st.empty()

            steps = [
                "🌐 Connecting to Adzuna...",
                "🔎 Searching current job opportunities...",
                "🧠 Calculating career-fit scores...",
                "🎯 Ranking opportunities...",
                "📧 Checking new job alerts..."
            ]

            for index, message in enumerate(steps):

                status.info(message)

                progress.progress(
                    int(
                        ((index + 1) / len(steps))
                        * 100
                    )
                )

                time.sleep(0.25)

            try:

                jobs = discover_jobs(
                    preferred_locations=selected_locations,
                    target_roles=selected_roles
                )

                processed_jobs = process_jobs(
                    jobs,
                    candidate
                )

                st.session_state.jobs = processed_jobs

                st.session_state.last_search = (
                    pd.Timestamp.now()
                )

                matching_jobs = processed_jobs[
                    processed_jobs["score"] >= 60
                ]

                emailed_count = send_new_jobs(
                    matching_jobs
                )

                if emailed_count > 0:

                    st.session_state.email_status = (
                        f"{emailed_count} new matching jobs emailed"
                    )

                else:

                    st.session_state.email_status = (
                        "No new matching jobs required an email"
                    )

                status.empty()
                progress.empty()

                st.success(
                    f"✅ Search completed — "
                    f"{len(processed_jobs)} real jobs found."
                )

            except Exception as error:

                status.empty()
                progress.empty()

                st.error(
                    f"❌ Job search failed: {error}"
                )

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    if not st.session_state.jobs.empty:

        st.divider()

        st.subheader(
            "📋 Search Results"
        )

        jobs = st.session_state.jobs

        search_columns = []

        for column in [
            "title",
            "company",
            "location",
            "score"
        ]:

            if column in jobs.columns:
                search_columns.append(column)

        st.dataframe(
            jobs[search_columns].head(30),
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# MATCHING JOBS
# ============================================================

elif page == "🎯 Matching Jobs":

    st.header(
        "🎯 AI-Matched Opportunities"
    )

    jobs = st.session_state.jobs

    if jobs.empty:

        st.info(
            "No job data available. "
            "Run a search first."
        )

    else:

        minimum_score = st.slider(
            "🎯 Minimum Match Score",
            min_value=0,
            max_value=100,
            value=50,
            step=5
        )

        matches = jobs[
            jobs["score"] >= minimum_score
        ].copy()

        st.metric(
            "Matching Opportunities",
            len(matches)
        )

        st.divider()

        if matches.empty:

            st.warning(
                "No jobs match the selected score."
            )

        else:

            for _, job in matches.head(20).iterrows():

                title = str(
                    job.get(
                        "title",
                        "Job Opportunity"
                    )
                )

                company = str(
                    job.get(
                        "company",
                        "Company not specified"
                    )
                )

                location = str(
                    job.get(
                        "location",
                        "Location not specified"
                    )
                )

                score = float(
                    job.get(
                        "score",
                        0
                    )
                )

                matched_skills = str(
                    job.get(
                        "matched_skills",
                        ""
                    )
                )

                with st.container(
                    border=True
                ):

                    left, middle, right = st.columns(
                        [5, 2, 1.4]
                    )

                    with left:

                        st.subheader(
                            f"💼 {title}"
                        )

                        st.write(
                            f"🏢 **{company}**"
                        )

                        st.write(
                            f"📍 {location}"
                        )

                        if matched_skills:

                            st.caption(
                                "🧠 Matched Skills: "
                                + matched_skills
                            )

                    with middle:

                        st.write(
                            "Match Score"
                        )

                        st.progress(
                            min(
                                score / 100,
                                1.0
                            )
                        )

                        st.write(
                            f"**{score:.0f}% Match**"
                        )

                    with right:

                        url = str(
                            job.get(
                                "url",
                                ""
                            )
                        )

                        if url.startswith("http"):

                            st.link_button(
                                "Apply ↗",
                                url,
                                use_container_width=True
                            )


# ============================================================
# ANALYTICS
# ============================================================

elif page == "📊 Analytics":

    st.header(
        "📊 Career Analytics"
    )

    jobs = st.session_state.jobs

    if jobs.empty:

        st.info(
            "Search jobs first to generate analytics."
        )

    else:

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "🎯 Match Score Distribution"
            )

            distribution = pd.cut(
                jobs["score"],
                bins=[
                    -1,
                    39,
                    59,
                    79,
                    100
                ],
                labels=[
                    "0–39%",
                    "40–59%",
                    "60–79%",
                    "80–100%"
                ]
            )

            distribution_counts = (
                distribution
                .value_counts()
                .sort_index()
            )

            st.bar_chart(
                distribution_counts,
                height=320
            )

        with col2:

            st.subheader(
                "🏢 Top Companies"
            )

            companies = (
                jobs["company"]
                .fillna("Unknown")
                .value_counts()
                .head(10)
            )

            st.bar_chart(
                companies,
                height=320
            )

        st.divider()

        st.subheader(
            "🧠 Most Relevant Skills"
        )

        skill_list = []

        if "matched_skills" in jobs.columns:

            for value in jobs[
                "matched_skills"
            ]:

                for skill in str(
                    value
                ).split(","):

                    skill = skill.strip()

                    if skill:

                        skill_list.append(
                            skill
                        )

        if skill_list:

            skill_counts = (
                pd.Series(
                    skill_list
                )
                .value_counts()
                .head(15)
            )

            st.bar_chart(
                skill_counts,
                height=350
            )

        else:

            st.info(
                "No matched skill data available."
            )


# ============================================================
# RESUME ANALYZER
# ============================================================

elif page == "📄 Resume Analyzer":

    st.header(
        "📄 Resume Analyzer"
    )

    st.write(
        "Upload your PDF resume and CareerPilot will "
        "extract text and identify configured technical skills."
    )

    uploaded_file = st.file_uploader(
        "📤 Upload Resume",
        type=["pdf"]
    )

    if uploaded_file:

        try:

            from pypdf import PdfReader

            reader = PdfReader(
                uploaded_file
            )

            resume_text = ""

            for page_data in reader.pages:

                resume_text += (
                    page_data.extract_text()
                    or ""
                )

            word_count = len(
                resume_text.split()
            )

            st.success(
                "✅ Resume processed successfully."
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "📄 Resume Words",
                    word_count
                )

            with col2:

                detected_skills = []

                lower_text = resume_text.lower()

                for skill in SKILLS:

                    if skill in lower_text:

                        detected_skills.append(
                            skill
                        )

                st.metric(
                    "🧠 Skills Detected",
                    len(detected_skills)
                )

            st.divider()

            st.subheader(
                "🛠️ Detected Technical Skills"
            )

            if detected_skills:

                skill_columns = st.columns(4)

                for index, skill in enumerate(
                    detected_skills
                ):

                    with skill_columns[
                        index % 4
                    ]:

                        st.success(
                            skill.title()
                        )

            else:

                st.info(
                    "No configured skills were detected."
                )

            with st.expander(
                "📄 View Extracted Resume Text"
            ):

                st.text(
                    resume_text[:15000]
                )

        except Exception as error:

            st.error(
                f"❌ Resume processing failed: {error}"
            )


# ============================================================
# CANDIDATE PROFILE
# ============================================================

elif page == "👤 Candidate Profile":

    st.header(
        "👤 Candidate Profile"
    )

    col1, col2 = st.columns(
        [1, 2]
    )

    with col1:

        st.subheader(
            f"👩‍💻 {candidate_name}"
        )

        st.info(
            "B.E. Computer Science and Engineering"
        )

        st.info(
            "Experience: Fresher"
        )

    with col2:

        st.subheader(
            "🛠️ Technical Skills"
        )

        skill_text = " • ".join(
            candidate_skills
        )

        st.write(
            skill_text
        )

        st.subheader(
            "🎯 Target Roles"
        )

        st.write(
            " • ".join(target_roles)
        )

        st.subheader(
            "📍 Preferred Locations"
        )

        st.write(
            " • ".join(preferred_locations)
        )


# ============================================================
# EMAIL ALERTS
# ============================================================

elif page == "📧 Email Alerts":

    st.header(
        "📧 Automated Job Alerts"
    )

    st.success(
        "● EMAIL AUTOMATION ACTIVE"
    )

    st.write(
        f"Current status: "
        f"**{st.session_state.email_status}**"
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.info(
            "🌐 **Adzuna**\n\n"
            "Real Job Discovery"
        )

    with col2:

        st.info(
            "🧠 **AI Matching**\n\n"
            "Career Fit Analysis"
        )

    with col3:

        st.info(
            "🎯 **Smart Filtering**\n\n"
            "High Match Jobs"
        )

    with col4:

        st.info(
            "📧 **Gmail**\n\n"
            "Automated Alerts"
        )

    st.divider()

    if st.session_state.last_search:

        st.write(
            "🕒 Last manual search:"
        )

        st.write(
            st.session_state.last_search.strftime(
                "%d %B %Y, %I:%M %p"
            )
        )

    else:

        st.write(
            "🕒 Last manual search: Not yet performed"
        )

    st.write(
        "⏱️ Automated monitoring is handled separately "
        "by GitHub Actions."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🚀 CareerPilot AI  |  "
    "Real Job Discovery  |  "
    "AI Matching  |  "
    "Automated Gmail Alerts"
)