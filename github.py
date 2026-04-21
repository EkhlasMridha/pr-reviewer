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

def post_review(pr_number, commit_id, body, event="REQUEST_CHANGES", comments=None):
    repo = os.getenv("GITHUB_REPO")
    token = os.getenv("GITHUB_TOKEN")

    url = f"{GITHUB_API}/repos/{repo}/pulls/{pr_number}/reviews"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    # 🧠 Base payload (ALWAYS valid)
    payload = {
        "commit_id": commit_id,
        "body": body,
        "event": event
    }

    # ✅ Only include comments if they exist and are valid
    if comments and len(comments) > 0:
        payload["comments"] = comments

    res = requests.post(url, json=payload, headers=headers)

    # 🔥 If inline comments fail → fallback to summary-only
    if res.status_code == 422:
        print("⚠️ Inline comments failed, falling back to summary-only review...")

        fallback_payload = {
            "commit_id": commit_id,
            "body": body,
            "event": event
        }

        res = requests.post(url, json=fallback_payload, headers=headers)

    # ❌ Still failing → raise error
    if res.status_code >= 300:
        raise Exception(f"GitHub API Error: {res.text}")

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

    print("\nPosting review to GitHub...")

    response = post_review(
        pr_number=pr_number,
        commit_id=pr_info["commit_id"],
        body=format_full_review(result),  # 🔥 summary instead of inline
        event="REQUEST_CHANGES",
        comments=None  # 🔥 disable inline comments
    )

    print("Review posted successfully ✅")
    return response


def format_full_review(result):
    text = f"## 🔍 AI Review\n\n{result.get('summary')}\n\n"

    for issue in result.get("issues", []):
        text += f"""
    ### {issue['file']}:{issue['line']} [{issue['severity']}]
    {issue['comment']}

    💡 {issue['suggestion']}
    \n
    """
    return text