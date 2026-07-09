import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from common.utils import retry
from gmail.gmail_client import (
    get_service,
    fetch_unread_emails,
    create_draft_reply,
)   

# Toggle this to switch between Gmail and the synthetic dataset
USE_GMAIL = True

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL_NAME = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """
You are a customer support agent for an e-commerce company.

Write a professional, empathetic, and helpful reply to the customer's email.

Guidelines:
- Thank the customer.
- Acknowledge their concern.
- Address their specific issue.
- Explain the next steps or resolution.
- Keep the response concise.
- End politely.
"""

EMAILS_FILE = "data/emails.json"
OUTPUT_FILE = "data/replies.json"


# ----------------------------------------------------
# Load emails
# ----------------------------------------------------

if USE_GMAIL:
    from gmail.gmail_client import get_service, fetch_unread_emails

    service = get_service()
    emails = fetch_unread_emails(service, max_results=5)

    print(f"Fetched {len(emails)} unread emails from Gmail.")

else:
    with open(EMAILS_FILE, "r", encoding="utf-8") as f:
        emails = json.load(f)

    print(f"Loaded {len(emails)} emails from dataset.")


# ----------------------------------------------------
# Generate replies
# ----------------------------------------------------

generated_replies = []

for email in emails:

    user_prompt = f"""
Subject:
{email['subject']}

Email:
{email['body']}
"""

    response = retry(
        lambda: client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.4,
        )
    )

    reply = response.choices[0].message.content.strip()

    if USE_GMAIL:
        create_draft_reply(
            service=service,
            to_email=email["from"],
            subject=email["subject"],
            reply_body=reply,
            thread_id=email["threadId"],
        )
        print(f"[OK] Draft created for: {email['subject']}")

    generated_replies.append(
        {
            "id": email["id"],
            "original_email": email,
            "generated_reply": reply,
        }
    )


# ----------------------------------------------------
# Save replies
# ----------------------------------------------------

os.makedirs("data", exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(
        generated_replies,
        f,
        indent=4,
        ensure_ascii=False,
    )

print(f"\nGenerated {len(generated_replies)} replies.")
print(f"Saved to {OUTPUT_FILE}")