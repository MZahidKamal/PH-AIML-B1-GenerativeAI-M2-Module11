from pydantic import BaseModel, Field
from typing import List



class ChatResponse(BaseModel):
    """Structured response schema for the chatbot."""

    answer: str = Field(description="The main answer to the user's question")
    summary: str = Field(description="A one-sentence summary of the answer")
    keywords: List[str] = Field(description="3 to 5 key terms from the answer")
    follow_up_questions: List[str] = Field(description="2 to 3 follow-up questions the user might ask next")
    category: str = Field(description="The detected category: programming, math, or general")
