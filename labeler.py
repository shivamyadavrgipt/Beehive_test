import os
import requests

title = os.getenv("ISSUE_TITLE", "").lower()
body = os.getenv("ISSUE_BODY", "").lower()
issue_number = os.getenv("ISSUE_NUMBER")
repo = os.getenv("REPO")
token = os.getenv("GITHUB_TOKEN")

text = title + " " + body

labels = []

# ---- TYPE LABEL ----
if "error" in text or "crash" in text or "bug" in text:
    labels.append("bug")
elif "feature" in text or "add" in text:
    labels.append("enhancement")

# ---- DIFFICULTY ----
length = len(text)

if length < 100:
    labels.append("easy")
elif length < 300:
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