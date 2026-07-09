# Smartdraft-AI — AI Email Reply Assistant

## Overview

This project is an AI-powered email assistant that connects directly with Gmail, intelligently identifies emails that actually require a response, drafts personalized replies using a Large Language Model (LLM), and evaluates the quality of generated responses using an LLM-as-a-Judge framework.

Unlike traditional email automation, the assistant first determines whether an email genuinely deserves a reply. Marketing emails, newsletters, receipts, shipping notifications, and other automated messages are skipped, while conversational emails receive context-aware draft responses.

For safety, replies are **saved as Gmail drafts instead of being sent automatically**, allowing the user to review them before sending.

---

# Features

- 📥 Connects to Gmail using OAuth 2.0
- 📧 Fetches unread emails directly from the inbox
- 🧠 Classifies whether an email actually needs a reply
- ✍️ Generates personalized AI replies
- 📝 Creates Gmail drafts (never auto-sends emails)
- 📊 Evaluates generated replies using an LLM-as-a-Judge framework
- 📁 Supports both Gmail mode and static dataset mode for reproducible evaluation

---

# Approach

The project consists of four major stages.

## 1. Dataset Generation

A synthetic dataset of realistic customer support emails is generated using the Groq API and stored locally in:

```
data/emails.json
```

The dataset contains multiple categories including:

- Refund requests
- Shipping delays
- Billing issues
- Product defects
- Order cancellations
- Customer complaints
- General questions

The dataset is generated only once to ensure reproducible evaluation.

---

## 2. Gmail Integration

The project authenticates using the Gmail API through OAuth 2.0.

Once authenticated, it:

- Fetches unread emails
- Extracts sender, subject and body
- Preserves Gmail thread IDs
- Works directly on a user's inbox

Authentication tokens are stored locally and reused for future sessions.

---

## 3. Intelligent Reply Generation

Instead of behaving like a customer support representative, the model acts as a **personal email assistant**.

Before generating a response, the assistant first determines whether an email deserves a reply.

Emails such as:

- newsletters
- advertisements
- promotions
- receipts
- shipping notifications
- OTP emails

are automatically skipped.

Only conversational emails proceed to the reply generation stage.

The reply is generated using the Groq Llama 3.3 70B Versatile model with a prompt that writes naturally in the user's voice rather than using corporate support language.

Generated replies are:

- concise
- natural
- conversational
- context-aware
- written in first person

---

## 4. Gmail Draft Creation

Instead of sending emails automatically, every generated response is saved as a Gmail Draft.

This allows human review before sending and avoids accidental responses.

Drafts are created within the original email thread, preserving Gmail conversations.

---

## 5. Evaluation

When running in dataset mode, every generated reply is evaluated using an LLM-as-a-Judge.

Each reply is scored on five dimensions:

- Relevance
- Tone
- Completeness
- Accuracy
- Conciseness

The evaluator produces:

- Per-response scores
- Criterion averages
- Overall quality score
- Lowest scoring response with justification

Results are stored in:

```
data/scores.json
```

---

# Why LLM-as-a-Judge?

Evaluating email quality is inherently subjective.

Simple rule-based methods struggle to assess qualities like empathy, conversational tone, or whether a reply genuinely resolves the sender's concern.

Instead, this project uses another LLM as an evaluator with a structured rubric.

This approach captures nuanced qualities while still producing structured, machine-readable scores.

To improve consistency:

- Temperature is fixed at 0
- A strict JSON schema is enforced
- Every reply is evaluated using the same rubric

---

# Evaluation Rubric

Each generated reply is scored from **1–5** on:

| Criterion | Description |
|------------|-------------|
| **Relevance** | Does the reply address the original email? |
| **Tone** | Is the response polite, natural and appropriate? |
| **Completeness** | Does it answer the email and provide a next step? |
| **Accuracy** | Does it avoid making unsupported claims? |
| **Conciseness** | Is the response brief while remaining useful? |

The overall score is the average across all criteria and all evaluated replies.

---

# Tech Stack

- Python 3.11+
- Groq API
- Llama 3.3 70B Versatile
- Gmail API
- Google OAuth 2.0
- OpenAI Python SDK (Groq-compatible)
- python-dotenv

---

# Key Design Decisions

### Gmail Drafts Instead of Auto-Send

Emails are saved as drafts rather than being sent automatically.

This keeps the user in control and avoids unintended responses.

---

### Reply Classification Before Generation

Many inbox messages (newsletters, receipts, promotions) do not require replies.

An LLM classifier filters these emails before generation, reducing unnecessary API calls and preventing nonsensical draft responses.

---

### Personal Assistant Persona

Instead of responding like a customer support chatbot, replies are written as if the user is personally replying to their own inbox.

This produces much more natural emails.

---

### LLM-as-a-Judge

A rubric-based LLM evaluator provides richer feedback than keyword matching while remaining structured enough for quantitative evaluation.

---

### Static Dataset for Evaluation

Synthetic emails are stored locally and reused across runs.

This ensures reproducible benchmarking.

---

# Repository Structure

```
hiver-email-ai-challenge/
│
├── common/
│   ├── __init__.py
│   └── utils.py
│
├── gmail/
│   ├── __init__.py
│   └── gmail_client.py
│
├── data/
│   ├── generate_dataset.py
│   ├── emails.json
│   ├── replies.json
│   ├── scores.json
│   └── __init__.py
│
├── generator/
│   ├── generate_replies.py
│   └── __init__.py
│
├── evaluator/
│   ├── evaluate_replies.py
│   └── __init__.py
│
├── credentials.json      # ignored by Git
├── token.pickle          # ignored by Git
├── run.py
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

---

# Installation

## Clone the repository

```bash
git clone <repository-url>
cd hiver-email-ai-challenge
```

---

## Create a virtual environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

macOS/Linux

```bash
source .venv/bin/activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
YOUR_NAME=Pratik
```

---

## Gmail API Setup

1. Create a Google Cloud project.
2. Enable the Gmail API.
3. Configure the OAuth Consent Screen.
4. Create Desktop OAuth Credentials.
5. Download `credentials.json`.
6. Place `credentials.json` in the project root.

The first run will open a browser for Gmail authentication.

---

# Running the Project

Run the complete pipeline:

```bash
python run.py
```

Depending on the selected mode:

### Gmail Mode

- Authenticate with Gmail
- Fetch unread emails
- Skip newsletters/promotions
- Generate AI replies
- Save replies as Gmail drafts

### Dataset Mode

- Load synthetic dataset
- Generate replies
- Evaluate replies
- Produce evaluation metrics

---

# Output Files

```
data/emails.json
```

Synthetic evaluation dataset.

```
data/replies.json
```

Generated AI replies.

```
data/scores.json
```

Evaluation scores generated by the LLM judge.

---

# Known Limitations

- Single-turn email conversations only
- No long-term conversation memory
- No Retrieval-Augmented Generation (RAG)
- Gmail integration currently supports draft creation only
- Evaluation depends on the judge model
- Small synthetic evaluation dataset

---

# Future Improvements

- Multi-turn email conversations
- Retrieval-Augmented Generation using previous emails
- Calendar-aware scheduling assistance
- Automatic attachment summarization
- Multi-model evaluation
- Confidence scoring
- Human-in-the-loop feedback for continual improvement
- Web interface for reviewing generated drafts

---

# Author

**Pratik Galave**

Built to demonstrate practical LLM integration, prompt engineering, Gmail API automation, and rubric-based AI evaluation.