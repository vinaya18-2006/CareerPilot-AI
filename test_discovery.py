from dotenv import load_dotenv

from services.job_discovery import discover_jobs


# Load .env
load_dotenv()


print()
print("========================================")
print("      CAREERPILOT JOB DISCOVERY TEST")
print("========================================")


# Test with only ONE role and ONE location
jobs = discover_jobs(

    preferred_locations=[
        "Bangalore"
    ],

    target_roles=[
        "Python Developer"
    ]
)


print()
print("========================================")
print("RESULT")
print("========================================")

print(
    "TOTAL JOBS:",
    len(jobs)
)


if jobs.empty:

    print()
    print("❌ NO JOBS FOUND")

else:

    print()
    print("✅ JOBS FOUND!")

    print()

    for _, job in jobs.head(10).iterrows():

        print("----------------------------------------")

        print(
            "Title:",
            job.get(
                "title",
                "Unknown"
            )
        )

        print(
            "Company:",
            job.get(
                "company",
                "Unknown"
            )
        )

        print(
            "Location:",
            job.get(
                "location",
                "Unknown"
            )
        )

        print(
            "URL:",
            job.get(
                "url",
                "No URL"
            )
        )

print()
print("========================================")