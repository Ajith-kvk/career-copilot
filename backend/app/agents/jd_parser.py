from langchain_core.prompts import ChatPromptTemplate

from app.llm import get_llm
from app.schemas import ParsedJD

PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
                        "You are an expert technical recruiter. Extract structured data from "
            "the job description. Use ONLY information present in the text. "
            "If something is not mentioned, leave it empty. Normalize skill "
            "names (e.g. 'Postgres' -> 'PostgreSQL') and keep each skill short, "
            "but do not lose meaning (keep 'REST API design', not 'REST'). "
            "When the text offers alternatives such as 'FastAPI or Flask', "
            "keep them together as ONE entry. "
            "'keywords' must only contain domain words that are NOT already "
            "listed as skills.",
        ),
        ("human", "Job description:\n\n{jd_text}"),
    ]
)


def parse_jd(jd_text: str) -> ParsedJD:
    chain = PROMPT | get_llm().with_structured_output(ParsedJD)
    return chain.invoke({"jd_text": jd_text})