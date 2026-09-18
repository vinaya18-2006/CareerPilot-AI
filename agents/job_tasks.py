from crewai import Task

from agents.job_search_agent import job_search_agent
from agents.job_tools import job_discovery_tool


job_search_task = Task(
    description="""
    Find relevant entry-level jobs for the candidate.

    Candidate target roles:
    {target_roles}

    Preferred locations:
    {preferred_locations}

    Candidate skills:
    {skills}

    Use the Job Discovery Tool to find matching opportunities.

    For every suitable job, provide:
    - Job title
    - Company
    - Location
    - Job URL
    - Why it matches the candidate
    """,

    expected_output="""
    A structured list of relevant job opportunities.
    Each opportunity must contain:
    Job Title, Company, Location, Job URL, and Match Reason.
    """,

    agent=job_search_agent
)