import os
from dotenv import load_dotenv
from crewai import Crew, Process, LLM

from agents.job_search_agent import job_search_agent
from agents.job_tasks import job_search_task

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError("GOOGLE_API_KEY is missing from .env")

gemini_llm = LLM(
    model="gemini/gemini-3.6-flash",
    api_key=google_api_key
)

job_search_agent.llm = gemini_llm

careerpilot_crew = Crew(
    agents=[job_search_agent],
    tasks=[job_search_task],
    process=Process.sequential,
    verbose=True
)