from crewai import Task

def create_tasks(diff, instructions, agents):
    diff_analyzer, reviewer, formatter = agents

    analyze = Task(
        description=f"""
Analyze PR diff:

{diff}

User instructions:
{instructions}

Find risky changes and important logic.
""",
        agent=diff_analyzer,
    )

    review = Task(
        description=f"""
Review code strictly following:
{instructions}

Return issues with:
- file
- line
- severity (low, medium, high)
- comment
- suggestion
""",
        agent=review,
    )

    format_task = Task(
        description="""
Return ONLY JSON:

{
  "summary": "text",
  "issues": [
    {
      "file": "",
      "line": 0,
      "severity": "",
      "comment": "",
      "suggestion": ""
    }
  ]
}
""",
        agent=formatter,
    )

    review.context = [analyze]
    format_task.context = [review]

    return [analyze, review, format_task]