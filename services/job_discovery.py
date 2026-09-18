import pandas as pd

from services.job_api import collect_jobs


# ============================================================
# CLEAN JOB DATA
# ============================================================

def clean_jobs(jobs):

    if jobs is None:
        return pd.DataFrame()

    if not isinstance(jobs, pd.DataFrame):
        jobs = pd.DataFrame(jobs)

    if jobs.empty:
        return jobs

    # --------------------------------------------------------
    # Make sure required columns exist
    # --------------------------------------------------------

    required_columns = [
        "id",
        "title",
        "company",
        "location",
        "experience",
        "skills",
        "description",
        "url",
        "created",
        "salary_min",
        "salary_max"
    ]

    for column in required_columns:

        if column not in jobs.columns:

            jobs[column] = ""


    # --------------------------------------------------------
    # Remove duplicate jobs
    # --------------------------------------------------------

    jobs = jobs.drop_duplicates(
        subset=[
            "title",
            "company",
            "location"
        ]
    )


    # --------------------------------------------------------
    # Remove jobs without title
    # --------------------------------------------------------

    jobs = jobs[
        jobs["title"]
        .fillna("")
        .astype(str)
        .str.strip()
        != ""
    ]


    # --------------------------------------------------------
    # Clean text fields
    # --------------------------------------------------------

    for column in [
        "title",
        "company",
        "location",
        "experience",
        "skills",
        "description",
        "url"
    ]:

        jobs[column] = (
            jobs[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )


    return jobs.reset_index(
        drop=True
    )


# ============================================================
# LIVE JOB DISCOVERY
# ============================================================

def discover_jobs(
    preferred_locations=None,
    target_roles=None,
    jobs_per_search=20
):

    # --------------------------------------------------------
    # Default locations
    # --------------------------------------------------------

    if not preferred_locations:

        preferred_locations = [
            "Bangalore"
        ]


    # --------------------------------------------------------
    # Default roles
    # --------------------------------------------------------

    if not target_roles:

        target_roles = [
            "Python Developer"
        ]


    print()
    print("=" * 60)
    print("CAREERPILOT AI - LIVE JOB DISCOVERY")
    print("=" * 60)

    print(
        "Target Roles:",
        target_roles
    )

    print(
        "Locations:",
        preferred_locations
    )


    # --------------------------------------------------------
    # Fetch REAL jobs from Adzuna
    # --------------------------------------------------------

    try:

        jobs = collect_jobs(

            roles=target_roles,

            locations=preferred_locations,

            jobs_per_search=jobs_per_search
        )

    except Exception as error:

        print()
        print(
            "❌ Live job discovery failed:"
        )

        print(error)

        raise


    # --------------------------------------------------------
    # No jobs
    # --------------------------------------------------------

    if jobs is None:

        print(
            "❌ Adzuna returned None."
        )

        return pd.DataFrame()


    if jobs.empty:

        print(
            "⚠️ Adzuna returned zero jobs."
        )

        return pd.DataFrame()


    # --------------------------------------------------------
    # Clean jobs
    # --------------------------------------------------------

    jobs = clean_jobs(
        jobs
    )


    print()
    print(
        f"✅ LIVE JOBS FOUND: {len(jobs)}"
    )


    # --------------------------------------------------------
    # Display sample
    # --------------------------------------------------------

    print()

    for _, job in jobs.head(5).iterrows():

        print(
            f"• {job['title']} | "
            f"{job['company']} | "
            f"{job['location']}"
        )


    print(
        "=" * 60
    )


    return jobs