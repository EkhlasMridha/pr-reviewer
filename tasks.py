from crewai import Task

def create_tasks(diff, instructions, agents):
    diff_analyzer, reviewer, formatter = agents

    analyze = Task(
        description=f"""
Analyze this PR diff:

{diff}

User instructions:
{instructions}

Identify:
- risky changes
- important logic
- potential bugs
""",
        expected_output="Clear explanation of risky and important code changes",
        agent=diff_analyzer,
    )

    review = Task(
        description=f"""
Review the code.

STRICT RULES:
- Follow user instructions: {instructions}
- Ignore style unless explicitly asked
- Focus on bugs, performance, and correctness

Return structured issues.
""",
        expected_output="List of issues with file, line, severity, comment, suggestion",
        agent=reviewer,
    )

    format_task = Task(
        description="""
    You are a STRICT JSON generator.

    Return ONLY valid JSON.
    NO markdown.
    NO explanation.
    NO extra text.

    If you fail, output empty JSON:

    {
      "summary": "",
      "issues": []
    }

    FORMAT:

    {
      "summary": "string",
      "issues": [
        {
          "file": "string",
          "line": number,
          "severity": "low|medium|high",
          "comment": "string",
          "suggestion": "string"
        }
      ]
    }
    """,
        expected_output="Valid JSON only",
        agent=formatter,
    )

    review.context = [analyze]
    format_task.context = [review]

    return [analyze, review, format_task]