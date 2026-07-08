import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

PROMPT = """
Generate exactly 15 realistic customer support emails for an e-commerce company.

Return ONLY a valid JSON array.

Each object must contain:
- id
- category
- subject
- body

Use these categories:
- refund request
- shipping delay
- product defect
- cancellation
- billing issue
- angry complaint
- simple question

Requirements:
- Vary the tone (frustrated, polite, confused, urgent).
- Vary the email length.
- Use realistic names and products.
- Make every email unique.
- Do NOT wrap the JSON in markdown.
- Do NOT include explanations.
- Return only the JSON array.
"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": PROMPT
        }
    ],
    temperature=0.9,
)

text = response.choices[0].message.content.strip()

emails = json.loads(text)

os.makedirs("data", exist_ok=True)

with open("data/emails.json", "w", encoding="utf-8") as f:
    json.dump(emails, f, indent=4, ensure_ascii=False)

print(f"Saved {len(emails)} emails to data/emails.json")