import os
import requests
import pandas as pd

from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# ADZUNA INDIA API
# ============================================================

ADZUNA_URL = (
    "https://api.adzuna.com/v1/api/jobs/in/search"
)


# ============================================================
# SEARCH ADZUNA
# ============================================================

def search_adzuna(
    role,
    location,
    results_per_page=20,
    page=1
):

    app_id = os.getenv(
        "ADZUNA_APP_ID"
    )

    app_key = os.getenv(
        "ADZUNA_APP_KEY"
    )


    # --------------------------------------------------------
    # Validate credentials
    # --------------------------------------------------------

    if not app_id:

        raise ValueError(
            "ADZUNA_APP_ID is missing from .env"
        )


    if not app_key:

        raise ValueError(
            "ADZUNA_APP_KEY is missing from .env"
        )


    # --------------------------------------------------------
    # API URL
    # --------------------------------------------------------

    url = f"{ADZUNA_URL}/{page}"


    # --------------------------------------------------------
    # Parameters
    # --------------------------------------------------------

    params = {

        "app_id": app_id,

        "app_key": app_key,

        "results_per_page":
            results_per_page,

        "what":
            role,

        "where":
            location,

        "content-type":
            "application/json"
    }


    print()
    print(
        f"Searching Adzuna: "
        f"{role} | {location}"
    )


    # --------------------------------------------------------
    # API REQUEST
    # --------------------------------------------------------

    response = requests.get(

        url,

        params=params,

        timeout=30
    )


    # --------------------------------------------------------
    # HTTP ERROR
    # --------------------------------------------------------

    response.raise_for_status()


    # --------------------------------------------------------
    # JSON RESPONSE
    # --------------------------------------------------------

    data = response.json()


    jobs = []


    # --------------------------------------------------------
    # PROCESS RESULTS
    # --------------------------------------------------------

    for job in data.get(
        "results",
        []
    ):

        company = job.get(
            "company",
            {}
        )


        location_data = job.get(
            "location",
            {}
        )


        jobs.append({

            "id":
                job.get(
                    "id",
                    ""
                ),

            "title":
                job.get(
                    "title",
                    ""
                ),

            "company":
                company.get(
                    "display_name",
                    ""
                ),

            "location":
                location_data.get(
                    "display_name",
                    ""
                ),

            "experience":
                "",

            "skills":
                "",

            "description":
                job.get(
                    "description",
                    ""
                ),

            "url":
                job.get(
                    "redirect_url",
                    ""
                ),

            "created":
                job.get(
                    "created",
                    ""
                ),

            "salary_min":
                job.get(
                    "salary_min"
                ),

            "salary_max":
                job.get(
                    "salary_max"
                )
        })


    print(
        f"Found {len(jobs)} jobs"
    )


    return jobs


# ============================================================
# COLLECT JOBS
# ============================================================

def collect_jobs(
    roles,
    locations,
    jobs_per_search=20
):

    all_jobs = []


    # --------------------------------------------------------
    # SEARCH EACH ROLE + LOCATION
    # --------------------------------------------------------

    for role in roles:

        for location in locations:

            print(
                f"\nSearching: "
                f"{role} | {location}"
            )


            try:

                jobs = search_adzuna(

                    role=role,

                    location=location,

                    results_per_page=
                        jobs_per_search
                )


                all_jobs.extend(
                    jobs
                )


            except Exception as error:

                print(
                    f"❌ Search failed: "
                    f"{role} / {location}"
                )

                print(
                    error
                )


    # --------------------------------------------------------
    # NO JOBS
    # --------------------------------------------------------

    if not all_jobs:

        return pd.DataFrame()


    # --------------------------------------------------------
    # CREATE DATAFRAME
    # --------------------------------------------------------

    df = pd.DataFrame(
        all_jobs
    )


    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    if not df.empty:

        df = df.drop_duplicates(

            subset=[
                "title",
                "company",
                "location"
            ]
        )


    # --------------------------------------------------------
    # RESET INDEX
    # --------------------------------------------------------

    df = df.reset_index(
        drop=True
    )


    print()
    print(
        f"TOTAL UNIQUE JOBS: {len(df)}"
    )


    return df