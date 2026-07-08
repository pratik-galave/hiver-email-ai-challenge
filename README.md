# Hiver Open Challenge — AI Email Reply Generator

## Overview

This project implements an AI-powered customer support email assistant that automatically generates professional draft replies to customer emails and evaluates the quality of those replies using an LLM-as-a-Judge framework.

The project is divided into three stages:

1. **Dataset Generation** – Generate a realistic dataset of customer support emails using an LLM.
2. **Reply Generation** – Generate empathetic and professional replies for each customer email.
3. **Evaluation** – Evaluate every generated reply using a rubric-based LLM judge and produce quantitative scores.

The entire pipeline can be executed with a single command.

---

# Approach

## Dataset Generation

A dataset of **15 realistic customer support emails** was generated using the Groq API with the Llama 3.3 70B Versatile model.

The emails cover multiple customer support scenarios including:

- Refund requests
- Shipping delays
- Product defects
- Billing issues
- Order cancellations
- Angry complaints
- General questions

The generated dataset is stored in `data/emails.json`.

To ensure reproducibility, the dataset is generated **only once** and reused in subsequent runs instead of regenerating every execution.

---

## Reply Generation

Each email is processed independently.

A system prompt instructs the language model to behave as an experienced customer support representative and generate replies that are:

- Professional
- Empathetic
- Helpful
- Concise
- Action-oriented

The original email's subject and body are provided as the user prompt.

Generated replies are stored in:

```
data/replies.json
```

---

## Evaluation

Instead of manually reviewing responses or relying on keyword matching, this project uses an **LLM-as-a-Judge** approach.

Each generated reply is evaluated against the original customer email using a structured rubric.

The evaluator produces both:

- Individual criterion scores
- Overall response score

Results are saved in:

```
data/scores.json
```

At the end of execution, the evaluation script prints:

- Overall average score
- Average score for each criterion
- Lowest scoring response
- Justification for the lowest score

---

# Tech Stack

- Python 3.11+
- Groq API
- Llama 3.3 70B Versatile
- python-dotenv
- OpenAI Python SDK (Groq-compatible API)

---

# Key Design Decisions

### 1. Static Dataset

The dataset is generated once and saved locally.

This ensures that evaluations are reproducible and comparable across multiple runs.

---

### 2. LLM-generated Replies

Instead of template-based responses, replies are generated dynamically by the language model.

This allows responses to adapt naturally to different customer situations and writing styles.

---

### 3. LLM-as-a-Judge

Email quality is subjective.

A rule-based evaluator would struggle to assess qualities like empathy, professionalism, or completeness.

Using an LLM with a fixed evaluation rubric provides more nuanced assessments while remaining structured and reproducible.

---

### 4. Structured JSON Output

Every LLM response requested by the evaluation pipeline returns strict JSON.

This makes parsing reliable and allows easy aggregation of evaluation metrics.

---

# Why This Evaluation Metric?

Each generated reply is evaluated using five criteria:

| Criterion | Description |
|------------|-------------|
| **Relevance** | Does the reply directly address the customer's issue? |
| **Tone & Empathy** | Is the response professional, polite, and empathetic? |
| **Completeness** | Does the reply provide a useful resolution or next step? |
| **Accuracy** | Does it avoid unsupported promises or incorrect information? |
| **Conciseness** | Is the reply brief while remaining informative? |

Each criterion is scored from **1–5**.

The final overall score is calculated by averaging all criteria across every generated response.

### Why LLM-as-a-Judge?

Compared to rule-based scoring, an LLM can better evaluate:

- empathy
- conversational quality
- contextual relevance
- helpfulness

while still producing structured outputs.

### Limitations

LLM-based evaluation is not perfect.

Possible limitations include:

- Slight scoring inconsistency across runs
- Potential evaluator bias
- Dependence on prompt quality

These are partially mitigated by:

- Fixed evaluation rubric
- Temperature set to 0 during evaluation
- Strict JSON output format

---

# Known Limitations

- Small dataset (15 emails)
- Single-turn conversations only
- No retrieval of company policies or knowledge base
- Replies are generated without customer history
- No human evaluation for comparison
- Evaluation depends on the judge model

---

# Repository Structure

```
hiver-email-ai-challenge/
│
├── common/
│   ├── __init__.py
│   └── utils.py
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
├── run.py
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

---

# How to Run

## 1. Clone the repository

```bash
git clone <repository-url>
cd hiver-email-ai-challenge
```

---

## 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

Windows

```bash
.venv\Scripts\activate
```

macOS/Linux

```bash
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure API key

Create a `.env` file from `.env.example`

```
GROQ_API_KEY=your_api_key_here
```

---

## 5. Run the complete pipeline

```bash
python run.py
```

The pipeline will automatically:

1. Generate the email dataset (if not already present)
2. Generate AI replies
3. Evaluate every reply
4. Produce summary statistics

---

# Output Files

```
data/emails.json
```

Generated customer support dataset.

```
data/replies.json
```

AI-generated customer support replies.

```
data/scores.json
```

Evaluation scores and justifications for every reply.

---

# Future Improvements

- Larger evaluation dataset
- Human evaluation alongside LLM evaluation
- Retrieval-Augmented Generation (RAG) using company policies
- Multi-turn conversation support
- Automatic prompt optimization
- Multiple judge models for more robust evaluation
- Confidence estimation for generated replies