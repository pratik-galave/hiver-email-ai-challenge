import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from common.utils import retry

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL_NAME = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """
You are an expert evaluator of customer support responses.

Evaluate the reply using ONLY these criteria.

1. relevance
Does the reply directly address the customer's issue?

2. tone
Is the reply polite, empathetic and professional?

3. completeness
Does it provide a useful resolution or clear next step?

4. accuracy
Does it avoid inventing company policies or making unsupported promises?

5. conciseness
Is it brief without omitting important information?

Each score must be an integer from 1 to 5.

Return ONLY valid JSON in exactly this format:

{
    "relevance": 5,
    "tone": 4,
    "completeness": 4,
    "accuracy": 5,
    "conciseness": 4,
    "justification": "Short explanation."
}

Do not use markdown.
Do not add explanations outside the JSON.
"""

INPUT_FILE = "data/replies.json"
OUTPUT_FILE = "data/scores.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    replies = json.load(f)

scores = []

totals = {
    "relevance": 0,
    "tone": 0,
    "completeness": 0,
    "accuracy": 0,
    "conciseness": 0
}

for item in replies:

    email = item["original_email"]
    reply = item["generated_reply"]

    user_prompt = f"""
Original Email

Subject:
{email["subject"]}

Body:
{email["body"]}

-------------------------

Generated Reply

{reply}
"""

    response = retry(
    lambda: client.chat.completions.create(
        model="llama-3.3-70b-versatile",
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
        temperature=0.4
    )
)

    result = response.choices[0].message.content.strip()

    if result.startswith("```"):
        result = (
            result.replace("```json", "")
                  .replace("```", "")
                  .strip()
        )

    evaluation = json.loads(result)

    overall = (
        evaluation["relevance"]
        + evaluation["tone"]
        + evaluation["completeness"]
        + evaluation["accuracy"]
        + evaluation["conciseness"]
    ) / 5

    scores.append({
        "id": item["id"],
        "overall": round(overall, 2),
        "scores": evaluation
    })

    for key in totals:
        totals[key] += evaluation[key]

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(scores, f, indent=4, ensure_ascii=False)

n = len(scores)

averages = {
    key: round(value / n, 2)
    for key, value in totals.items()
}

overall_score = round(sum(averages.values()) / 5, 2)

lowest = min(scores, key=lambda x: x["overall"])

print("\n========== Evaluation Summary ==========\n")

print(f"Overall Score : {overall_score}/5\n")

for criterion, value in averages.items():
    print(f"{criterion.capitalize():15}: {value}")

print("\nLowest Scoring Email")
print("--------------------")
print(f"ID: {lowest['id']}")
print(f"Score: {lowest['overall']}/5")
print(f"Reason: {lowest['scores']['justification']}")

print(f"\nSaved detailed scores to {OUTPUT_FILE}")