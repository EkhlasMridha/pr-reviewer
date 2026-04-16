from crewai import Agent, LLM
import os

def create_llm():
    return LLM(
        model=os.getenv("MODEL_NAME", "gemini-1.5-flash"),
        api_key=os.getenv("GOOGLE_API_KEY"),
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
        goal="Return strict JSON output",
        backstory="Strict output generator",
        llm=llm,
        verbose=False
    )

    return diff_analyzer, reviewer, formatter