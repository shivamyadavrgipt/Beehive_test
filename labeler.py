import os
import requests
from openai import OpenAI
import json
import re

# ---- CONFIG ----
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

title = os.getenv("ISSUE_TITLE", "")
body = os.getenv("ISSUE_BODY", "")
issue_number = os.getenv("ISSUE_NUMBER")
repo = os.getenv("REPO")
token = os.getenv("GITHUB_TOKEN")

text = f"{title}\n{body}"

# ---- PROMPT ----
prompt = f"""
You are a GitHub issue triage bot.

Classify strictly into:
- type: bug, enhancement, question
- difficulty: easy, medium, hard

Return ONLY valid JSON:
{{
  "type": "bug | enhancement | question",
  "difficulty": "easy | medium | hard"
}}

Issue:
{text}
"""

# ---- GROQ CALL ----
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}],
)

content = response.choices[0].message.content.strip()
print("RAW:", content)

# ---- SAFE JSON PARSE ----
try:
    content = re.search(r'\{.*\}', content, re.DOTALL).group()
    data = json.loads(content)
    labels = [data["type"], data["difficulty"]]
except Exception as e:
    print("PARSE ERROR:", e)
    labels = ["needs-review"]

print("FINAL LABELS:", labels)

# ---- GITHUB API ----
url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels"

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

res = requests.post(url, json={"labels": labels}, headers=headers)

print("STATUS:", res.status_code)
print("RESPONSE:", res.text)