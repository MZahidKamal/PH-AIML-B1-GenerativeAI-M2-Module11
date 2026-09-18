# LangChain Chatbot

An AI chatbot built with LangChain that demonstrates **RunnableBranch**, **RunnableParallel**, and **Pydantic Structured Output** through a Streamlit chat interface.

---

## Project Overview

This chatbot automatically detects the category of a user's question and routes it to the appropriate domain-expert pipeline. Each response includes a main answer, a one-sentence summary, keywords, and follow-up questions — all generated simultaneously and validated against a typed schema before being displayed.

---

## Features

- **Automatic category detection** — classifies each question as Programming, Math, or General
- **RunnableBranch** — routes the question to the matching domain-expert prompt
- **RunnableParallel** — generates Summary, Keywords, and Follow-up Questions simultaneously
- **Pydantic Structured Output** — every response is validated against a typed schema before display
- **Chat history** — full conversation preserved across interactions

---

## Project Structure

```
project/
├── app.py            # Streamlit UI and chat loop
├── chatbot.py        # RunnableBranch + RunnableParallel logic
├── prompts.py        # All ChatPromptTemplate definitions
├── schemas.py        # Pydantic ChatResponse schema
├── requirements.txt
├── .env.example
└── README.md
```

---

## RunnableBranch Implementation

Each user question is first classified into one of three categories by an LLM call. `RunnableBranch` then evaluates the conditions in order and routes the question to the first matching domain-expert chain. Only one branch executes — the others are skipped entirely.

```
User Question
      │
      ▼
Category Detection (LLM)
      │
      ▼
RunnableBranch
  ├── programming? ──► Programming Expert Chain
  ├── math?        ──► Math Tutor Chain
  └── (default)    ──► General Assistant Chain
      │
      ▼
  Main Answer
```

---

## RunnableParallel Implementation

Once the main answer is generated, three enrichment chains run simultaneously using `RunnableParallel`. All three LLM calls happen at the same time — reducing total response time compared to running them one after another.

```
Main Answer
      │
      ▼
RunnableParallel
  ├── Summary Chain     ──► one-sentence summary
  ├── Keywords Chain    ──► 3–5 key terms
  └── Follow-up Chain   ──► 2–3 follow-up questions
      │
      ▼
  Combined Results
```

---

## Pydantic Structured Output

All chatbot responses are packed into a `ChatResponse` Pydantic model before being sent to the UI. This ensures every field is present and correctly typed — the Streamlit interface can reliably access `response.answer`, `response.keywords`, and so on without defensive checks.

```
Raw LLM Outputs
      │
      ▼
ChatResponse (Pydantic BaseModel)
  ├── answer               → str
  ├── summary              → str
  ├── keywords             → List[str]
  ├── follow_up_questions  → List[str]
  └── category             → str
      │
      ▼
  Streamlit UI Display
```

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
# Copy .env.example to .env and fill in your credentials
cp .env.example .env

# Open .env and set the following values:
# GROQ_CLOUD_API_KEY       → your Groq Cloud API key
# GROQ_CLOUD_OPENAI_MODEL  → your Groq model name

# 5. Run the app
streamlit run .\app.py
```

---

## Author

**Mohammad Zahid Kamal**
