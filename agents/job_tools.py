from crewai.tools import tool
from services.job_discovery import discover_jobs


@tool("Job Discovery Tool")
def job_discovery_tool(query: str) -> str:
    """
    Search real job opportunities using the existing Adzuna job discovery system.
    """

    try:
        jobs = discover_jobs(
            preferred_locations=[query],
            target_roles=[
                "Software Developer",
                "Python Developer",
                "Data Analyst",
                "Data Engineer",
                "Cloud Engineer",
                "AI Engineer"
            ]
        )

        if not jobs:
            return "No real jobs found."

        return str(jobs)

    except Exception as e:
        return f"Job discovery error: {str(e)}"