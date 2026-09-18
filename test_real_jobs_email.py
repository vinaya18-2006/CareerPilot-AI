from services.job_discovery import discover_jobs
from services.email_service import send_job_email


# ------------------------------------------------------------
# JOB SEARCH SETTINGS
# ------------------------------------------------------------

locations = [
    "Bangalore"
]

roles = [
    "Python Developer",
    "Software Engineer",
    "Backend Developer"
]


print("🔍 Searching for real jobs...")


# ------------------------------------------------------------
# GET REAL JOBS
# ------------------------------------------------------------

jobs = discover_jobs(
    preferred_locations=locations,
    target_roles=roles
)


print(
    f"✅ Found {len(jobs)} real jobs"
)


# ------------------------------------------------------------
# DISPLAY JOBS
# ------------------------------------------------------------

if jobs.empty:

    print("❌ No jobs found.")

else:

    print("\n========== REAL JOBS ==========\n")

    columns = [
        "title",
        "company",
        "location",
        "url"
    ]

    available_columns = [
        column
        for column in columns
        if column in jobs.columns
    ]

    print(
        jobs[available_columns]
        .head(10)
        .to_string(index=False)
    )


    # --------------------------------------------------------
    # SEND TOP JOBS TO EMAIL
    # --------------------------------------------------------

    print("\n📧 Sending jobs to Gmail...")

    top_jobs = jobs.head(10)

    result = send_job_email(
        top_jobs
    )


    if result:

        print(
            "\n🎉 REAL JOB EMAIL SENT SUCCESSFULLY!"
        )

    else:

        print(
            "\n❌ Email was not sent."
        )