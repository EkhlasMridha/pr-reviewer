from crewai import Crew
from agents import create_agents
from tasks import create_tasks
import json
import re

def safe_parse(result):
    # 1. Extract text from CrewOutput
    text = getattr(result, "raw", None) or str(result)

    # 2. Try direct JSON parse
    try:
        return json.loads(text)
    except:
        pass

    # 3. Extract JSON block from messy output
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass

    # 4. Fallback
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

    # 👇 IMPORTANT FIX
    raw_text = getattr(result, "raw", str(result))

    return safe_parse(raw_text)