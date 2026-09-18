from services.job_discovery import discover_jobs


locations = [
    "Bangalore",
    "Chennai",
    "Hyderabad",
    "Remote"
]


roles = [
    "Software Developer",
    "Python Developer",
    "Data Analyst",
    "Data Engineer",
    "Cloud Engineer",
    "AI Engineer"
]


jobs = discover_jobs(
    preferred_locations=locations,
    target_roles=roles
)


print("\n================================")
print("CAREERPILOT JOB DISCOVERY")
print("================================")

print(
    f"Jobs discovered: {len(jobs)}"
)

print("\nJobs:")

print(
    jobs[
        [
            "title",
            "company",
            "location"
        ]
    ].to_string(
        index=False
    )
)