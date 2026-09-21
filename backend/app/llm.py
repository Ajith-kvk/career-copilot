from langchain_groq import ChatGroq

from app.config import settings


def get_llm(temperature: float = 0.0) -> ChatGroq:
    return ChatGroq(
        model=settings.groq_model,
        temperature=temperature,
        api_key=settings.groq_api_key,
    )