from crewai import Crew
from agents import create_agents
from tasks import create_tasks
import json

def safe_parse(text):
    try:
        return json.loads(text)
    except:
        return {
            "summary": "Failed to parse model output",
            "issues": []
        }

def run_review(diff, instructions):
    agents = create_agents()
    tasks = create_tasks(diff, instructions, agents)

    crew = Crew(
        agents=list(agents),
        tasks=tasks,
        verbose=False
    )

    result = crew.kickoff()
    return safe_parse(result)