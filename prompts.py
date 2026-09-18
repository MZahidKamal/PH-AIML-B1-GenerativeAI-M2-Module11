from langchain_core.prompts import ChatPromptTemplate


# ------------------------------------------------------------------
# Category detection prompt
# Used once at the start to classify the user's question
# ------------------------------------------------------------------
CATEGORY_DETECTION_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a question classifier. "
        "Classify the user's question into exactly one of these categories: "
        "programming, math, general. "
        "Reply with only the single lowercase word — nothing else."
    ),
    ("human", "{question}"),
])


# ------------------------------------------------------------------
# Branch-specific answer prompts
# Each branch gets a domain-expert persona
# ------------------------------------------------------------------
PROGRAMMING_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert software engineer and programming tutor. "
        "Answer the user's programming question clearly and concisely. "
        "Include a short code example when it helps."
    ),
    ("human", "{question}"),
])

MATH_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert mathematics tutor. "
        "Answer the user's math question step by step. "
        "Use plain text for equations — no LaTeX."
    ),
    ("human", "{question}"),
])

GENERAL_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a knowledgeable and friendly general-purpose assistant. "
        "Answer the user's question clearly and helpfully."
    ),
    ("human", "{question}"),
])


# ------------------------------------------------------------------
# Parallel output prompts
# These run simultaneously after the branch answer is generated
# ------------------------------------------------------------------
SUMMARY_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "Summarize the following answer in exactly one sentence. "
        "Reply with only the summary — nothing else."
    ),
    ("human", "{answer}"),
])

KEYWORDS_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "Extract 3 to 5 key terms from the following answer. "
        "Reply with only a comma-separated list of terms — nothing else."
    ),
    ("human", "{answer}"),
])

FOLLOWUP_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "Based on the following answer, generate 2 to 3 natural follow-up questions "
        "that a curious learner might ask next. "
        "Reply with only the questions, one per line — no numbering, no extra text."
    ),
    ("human", "{answer}"),
])
