import os
import requests

def get_pr_diff(pr_number):
    repo = os.getenv("GITHUB_REPO")
    token = os.getenv("GITHUB_TOKEN")

    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3.diff"
    }

    res = requests.get(url, headers=headers)
    return res.text