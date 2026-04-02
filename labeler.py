import os
import requests

title = os.getenv("ISSUE_TITLE", "").lower()
body = os.getenv("ISSUE_BODY", "").lower()
issue_number = os.getenv("ISSUE_NUMBER")
repo = os.getenv("REPO")
token = os.getenv("GITHUB_TOKEN")

text = title + " " + body

labels = ["bug"]

# ---- TYPE ----
if any(word in text for word in ["error", "crash", "crashes", "failed", "bug"]):
    labels.append("bug")
elif any(word in text for word in ["feature", "add", "improve", "enhancement"]):
    labels.append("enhancement")

# ---- DIFFICULTY ----
length = len(text)

if length < 80:
    labels.append("easy")
elif length < 200:
    labels.append("medium")
else:
    labels.append("hard")

# ---- API CALL ----
url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels"

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

response = requests.post(url, json={"labels": labels}, headers=headers)

print(response.json())