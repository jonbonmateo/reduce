import os
import openai
import requests

# Set up OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Fetch PR details
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("GITHUB_REF").split("/")[-2]

url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files"
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
response = requests.get(url, headers=headers)
files = response.json()

# Collect changes from the PR
changes = []
for file in files:
    changes.append(f"File: {file['filename']}\nChanges:\n{file['patch']}")

# Prepare the prompt for OpenAI
prompt = (
    "You are a helpful code reviewer. Review the following code changes in a GitHub pull request. "
    "Provide feedback on code quality, potential bugs, and improvements. Be concise and actionable.\n\n"
    + "\n\n".join(changes)
)

# Call OpenAI API
response = openai.ChatCompletion.create(
    model="gpt-4",  # or "gpt-3.5-turbo"
    messages=[
        {"role": "system", "content": "You are a helpful code reviewer."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=500
)

# Post the review as a comment on the PR
review_comment = response["choices"][0]["message"]["content"]
comment_url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/reviews"
data = {
    "body": f"**AI Code Review:**\n\n{review_comment}",
    "event": "COMMENT"
}
requests.post(comment_url, headers=headers, json=data)
