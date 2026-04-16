import os
import requests

GITHUB_API = "https://api.github.com"
def get_pr_diff(pr_number):
    repo = os.getenv("GITHUB_REPO")
    token = os.getenv("GITHUB_TOKEN")

    url = f"{GITHUB_API}/repos/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3.diff"
    }

    res = requests.get(url, headers=headers)
    return res.text

def post_review(pr_number, commit_id, body, event, comments):
    repo = os.getenv("GITHUB_REPO")
    token = os.getenv("GITHUB_TOKEN")

    url = f"{GITHUB_API}/repos/{repo}/pulls/{pr_number}/reviews"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    payload = {
        "commit_id": commit_id,
        "body": body,
        "event": event,  # COMMENT | REQUEST_CHANGES | APPROVE
        "comments": comments
    }

    res = requests.post(url, json=payload, headers=headers)

    if res.status_code >= 300:
        raise Exception(res.text)

    return res.json()

def get_pr_info(pr_number):
    repo = os.getenv("GITHUB_REPO")
    token = os.getenv("GITHUB_TOKEN")

    url = f"{GITHUB_API}/repos/{repo}/pulls/{pr_number}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    res = requests.get(url, headers=headers)
    res.raise_for_status()

    data = res.json()

    return {
        "commit_id": data["head"]["sha"]
    }


def build_comments(result, file_map):
    comments = []

    for issue in result.get("issues", []):
        file = issue["file"]
        line = issue["line"]

        comments.append({
            "path": file,
            "line": line,
            "side": "RIGHT",
            "body": f"""
**[{issue['severity'].upper()}] {issue['comment']}**

💡 Suggestion:
{issue['suggestion']}
"""
        })

    return comments


from github import post_review, get_pr_info, build_comments

def handle_confirm(pr_number, result):
    pr_info = get_pr_info(pr_number)

    comments = build_comments(result, None)

    print("\nPosting review to GitHub...")

    response = post_review(
        pr_number=pr_number,
        commit_id=pr_info["commit_id"],
        body=result.get("summary", "AI Review"),
        event="REQUEST_CHANGES",
        comments=comments
    )

    print("Review posted successfully!")
    return response