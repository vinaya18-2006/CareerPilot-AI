from agents.crew import careerpilot_crew
from agents.candidate_context import load_candidate


candidate = load_candidate()

roles = ", ".join(candidate["target_roles"])
locations = ", ".join(candidate["preferred_locations"])
skills = ", ".join(candidate["skills"])

result = careerpilot_crew.kickoff(
    inputs={
        "target_roles": roles,
        "preferred_locations": locations,
        "skills": skills
    }
)

print("\n========== CAREERPILOT RESULTS ==========\n")
print(result)