from dotenv import load_dotenv

from services.job_api import search_adzuna


load_dotenv()

print("=" * 60)
print("CAREERPILOT REAL JOB SEARCH")
print("=" * 60)

jobs = search_adzuna(
    role="Python Developer",
    location="Bangalore",
    results_per_page=10
)

print(f"\nREAL JOBS FOUND: {len(jobs)}\n")

for number, job in enumerate(jobs, start=1):

    print("-" * 60)

    print(f"{number}. {job['title']}")
    print(f"Company: {job['company']}")
    print(f"Location: {job['location']}")
    print(f"URL: {job['url']}")