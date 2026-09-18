import os
import json
import time
import pandas as pd
from dotenv import load_dotenv

from services.job_discovery import discover_jobs
from services.email_service import send_job_email

load_dotenv()

# =========================
# SETTINGS
# =========================

CHECK_INTERVAL = 60      # 1 hour
MIN_MATCH_SCORE = 60

ROLES = [
    "Python Developer",
    "Software Engineer",
    "Data Analyst"
]

LOCATIONS = [
    "Bangalore"
]

SENT_FILE = "data/sent_jobs.json"


# =========================
# SENT JOBS
# =========================

def load_sent_jobs():

    if not os.path.exists(SENT_FILE):
        return set()

    try:
        with open(SENT_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))

    except Exception:
        return set()


def save_sent_jobs(sent_jobs):

    os.makedirs("data", exist_ok=True)

    with open(SENT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            list(sent_jobs),
            f,
            indent=2
        )


# =========================
# MATCHING
# =========================

def calculate_match_score(job):

    text = " ".join([
        str(job.get("title", "")),
        str(job.get("description", "")),
        str(job.get("skills", ""))
    ]).lower()

    skills = [
        "python",
        "sql",
        "aws",
        "azure",
        "power bi",
        "machine learning",
        "pandas",
        "numpy",
        "django",
        "flask",
        "fastapi",
        "git",
        "github",
        "html",
        "css",
        "javascript",
        "data analysis",
        "computer vision"
    ]

    matched = []

    for skill in skills:
        if skill in text:
            matched.append(skill)

    # Give a reasonable score based on matched skills
    score = min(
        100,
        round((len(matched) / 8) * 100, 2)
    )

    return score, matched


# =========================
# SEARCH + EMAIL
# =========================

def search_and_email_jobs():

    print("\n" + "=" * 70)
    print("🚀 CAREERPILOT AI - AUTOMATIC JOB MONITOR")
    print("=" * 70)

    try:

        print("🔎 Searching real jobs from Adzuna...")

        jobs = discover_jobs(
            preferred_locations=LOCATIONS,
            target_roles=ROLES
        )

        if jobs is None or jobs.empty:

            print("❌ No jobs returned.")

            return

        print(f"\n✅ {len(jobs)} real jobs found.")

        # -------------------------
        # Calculate scores
        # -------------------------

        results = []

        for _, job in jobs.iterrows():

            score, matched = calculate_match_score(job)

            job_data = job.to_dict()

            job_data["score"] = score
            job_data["matched_skills"] = ", ".join(matched)

            results.append(job_data)

        results_df = pd.DataFrame(results)

        # -------------------------
        # Show top jobs
        # -------------------------

        results_df = results_df.sort_values(
            by="score",
            ascending=False
        )

        print("\n🎯 TOP MATCHING JOBS:")

        for _, job in results_df.head(10).iterrows():

            print(
                f"{job.get('score', 0)}% | "
                f"{job.get('title', '')} | "
                f"{job.get('company', '')}"
            )

        # -------------------------
        # Filter matching jobs
        # -------------------------

        matching_jobs = results_df[
            results_df["score"] >= MIN_MATCH_SCORE
        ].copy()

        print(
            f"\n🎯 Jobs >= {MIN_MATCH_SCORE}%: "
            f"{len(matching_jobs)}"
        )

        if matching_jobs.empty:

            print("⚠️ No jobs passed the match threshold.")

            return

        # -------------------------
        # Remove duplicates
        # -------------------------

        sent_jobs = load_sent_jobs()

        new_jobs = []

        for _, job in matching_jobs.iterrows():

            job_id = str(
                job.get("id")
                or job.get("url")
            )

            if job_id not in sent_jobs:

                new_jobs.append(job.to_dict())

        print(
            f"🆕 New jobs not previously emailed: "
            f"{len(new_jobs)}"
        )

        if not new_jobs:

            print("ℹ️ All matching jobs were already emailed.")

            return

        new_jobs_df = pd.DataFrame(new_jobs)

        # -------------------------
        # SEND EMAIL
        # -------------------------

        print("\n📧 Sending Gmail alert...")

        success = send_job_email(new_jobs_df)

        print(f"📧 Email result: {success}")

        if success:

            for _, job in new_jobs_df.iterrows():

                job_id = str(
                    job.get("id")
                    or job.get("url")
                )

                sent_jobs.add(job_id)

            save_sent_jobs(sent_jobs)

            print(
                f"✅ {len(new_jobs_df)} jobs emailed successfully!"
            )

        else:

            print("❌ Email function returned False.")

    except Exception as error:

        print("\n❌ ERROR:")
        print(error)


# =========================
# 24/7 LOOP
# =========================

def main():

    print("\n🤖 CareerPilot AI 24/7 Job Monitor")
    print("🌐 Source: Adzuna")
    print("📧 Destination: Gmail")
    print("🎯 Match threshold: 60%")
    print("⏰ Search interval: 1 hour")
    print("🛑 Press Ctrl+C to stop")

    while True:

        search_and_email_jobs()

        print("\n⏳ Waiting 1 hour for next search...")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main() 