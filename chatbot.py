import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableParallel, RunnableLambda

from prompts import (
    CATEGORY_DETECTION_PROMPT,
    PROGRAMMING_PROMPT,
    MATH_PROMPT,
    GENERAL_PROMPT,
    SUMMARY_PROMPT,
    KEYWORDS_PROMPT,
    FOLLOWUP_PROMPT,
)
from schemas import ChatResponse



load_dotenv()



# ------------------------------------------------------------------
# LLM initialisation
# ------------------------------------------------------------------
def build_llm() -> ChatGroq:
    return ChatGroq(
        model=os.getenv("GROQ_CLOUD_OPENAI_MODEL"),
        api_key=os.getenv("GROQ_CLOUD_API_KEY"),
        temperature=0.3,
    )



# ------------------------------------------------------------------
# Step 1 — detect category
# Returns "programming", "math", or "general"
# ------------------------------------------------------------------
def detect_category(question: str, llm: ChatGroq) -> str:
    category_chain = CATEGORY_DETECTION_PROMPT | llm | StrOutputParser()
    raw = category_chain.invoke({"question": question}).strip().lower()
    # Normalise — fall back to "general" if unexpected value
    if raw not in {"programming", "math", "general"}:
        return "general"
    return raw



# ------------------------------------------------------------------
# Step 2 — RunnableBranch: pick the right answer prompt
# ------------------------------------------------------------------
def build_answer_branch(llm: ChatGroq):
    string_parser = StrOutputParser()

    programming_chain = PROGRAMMING_PROMPT | llm | string_parser
    math_chain        = MATH_PROMPT        | llm | string_parser
    general_chain     = GENERAL_PROMPT     | llm | string_parser

    branch = RunnableBranch(
        (lambda x: x["category"] == "programming", programming_chain),
        (lambda x: x["category"] == "math",        math_chain),
        general_chain,   # default
    )
    return branch



# ------------------------------------------------------------------
# Step 3 — RunnableParallel: generate summary, keywords, follow-ups
# All three run simultaneously on the answer text
# ------------------------------------------------------------------
def build_parallel_enrichment(llm: ChatGroq):
    string_parser = StrOutputParser()

    parallel = RunnableParallel(
        summary   = SUMMARY_PROMPT   | llm | string_parser,
        keywords  = KEYWORDS_PROMPT  | llm | string_parser,
        follow_up = FOLLOWUP_PROMPT  | llm | string_parser,
    )
    return parallel



# ------------------------------------------------------------------
# Main public function — called by app.py
# Returns a ChatResponse Pydantic object
# ------------------------------------------------------------------
def get_response(question: str) -> ChatResponse:
    llm = build_llm()

    # Step 1 — classify
    category = detect_category(question, llm)

    # Step 2 — branch to domain-expert answer
    answer_branch = build_answer_branch(llm)
    answer_text   = answer_branch.invoke({
        "question": question,
        "category": category,
    })

    # Step 3 — parallel enrichment (summary + keywords + follow-ups)
    parallel_chain   = build_parallel_enrichment(llm)
    parallel_results = parallel_chain.invoke({"answer": answer_text})

    # Parse keywords (comma-separated string → list)
    raw_keywords = parallel_results["keywords"]
    keywords_list = [k.strip() for k in raw_keywords.split(",") if k.strip()]

    # Parse follow-up questions (one per line → list)
    raw_followup = parallel_results["follow_up"]
    followup_list = [q.strip() for q in raw_followup.splitlines() if q.strip()]

    # Step 4 — pack into Pydantic structured output
    return ChatResponse(
        answer               = answer_text,
        summary              = parallel_results["summary"],
        keywords             = keywords_list,
        follow_up_questions  = followup_list,
        category             = category,
    )
