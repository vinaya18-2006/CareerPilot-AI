from crewai import Agent

from agents.job_tools import job_discovery_tool


job_search_agent = Agent(
    role="Job Search Specialist",

    goal=(
        "Find relevant entry-level jobs based on the candidate's "
        "skills, target roles, and preferred locations."
    ),

    backstory=(
        "You are an expert recruitment research specialist. "
        "You search for relevant technology jobs and identify "
        "opportunities that strongly match a candidate's profile."
    ),

    tools=[job_discovery_tool],

    verbose=True
)