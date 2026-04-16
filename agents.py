from crewai import Agent
from crewai import LLM
import os

def create_llm():
    return LLM(
        model=os.getenv("MODEL_NAME", "grok-2-latest"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.2,
    )

def create_agents():
    llm = create_llm()

    diff_analyzer = Agent(
        role="Diff Analyzer",
        goal="Understand PR changes and find risky areas",
        backstory="Expert in git diffs",
        llm=llm,
        verbose=False
    )

    reviewer = Agent(
        role="Senior Code Reviewer",
        goal="Find bugs, performance issues, and bad practices",
        backstory="Experienced engineer",
        llm=llm,
        verbose=False
    )

    formatter = Agent(
        role="JSON Formatter",
        goal="Return strictly valid JSON output",
        backstory="Strict formatter",
        llm=llm,
        verbose=False
    )

    return diff_analyzer, reviewer, formatter