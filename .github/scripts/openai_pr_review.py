from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Fetch PR changes using git diff
pr_diff = os.popen("git diff HEAD^ HEAD").read()

# Generate review using OpenAI
response = client.chat.completions.create(
    model="gpt-3.5-turbo", 
    messages=[
        {"role": "system", "content": "You are a helpful code reviewer. Provide concise and actionable feedback on the following code changes."},
        {"role": "user", "content": f"Review the following code changes:\n\n{pr_diff}"}
    ]
)

# Extract the review from the response
review = response.choices[0].message.content

# Print the review (for GitHub Actions to capture as output)
print(f"::set-output name=review::{review}")
