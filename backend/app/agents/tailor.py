from langchain_core.prompts import ChatPromptTemplate

from app.llm import get_llm
from app.schemas import FitReport, ParsedJD, TailoredOutput
from app.services.resume_store import search_resume

PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a career coach writing application materials for {name}.\n"
            "STRICT RULES:\n"
            "1. Use ONLY facts found in the RESUME EXCERPTS. Never invent employers, "
            "tools, metrics, or years.\n"
            "2. NEVER claim or imply any skill listed under MISSING SKILLS.\n"
            "3. Mirror the job's vocabulary only where it is truthful.\n"
            "4. bullet_rewrites: choose 3-5 existing bullets from the excerpts and "
            "rewrite them to highlight relevance; keep every fact intact.\n"
            "5. cover_letter: at most 250 words, 3 short paragraphs, no cliche "
            "openers, sign off with the name.",
        ),
        (
            "human",
            "ROLE: {title} at {company}\n"
            "RESPONSIBILITIES:\n{responsibilities}\n"
            "KEYWORDS: {keywords}\n"
            "MISSING SKILLS (do not claim): {missing}\n\n"
            "RESUME EXCERPTS:\n{evidence}",
        ),
    ]
)


def gather_evidence(parsed: ParsedJD, fit: FitReport) -> str:
    supported = [m.skill for m in fit.matches if m.status != "missing"]
    queries = supported + parsed.responsibilities[:3] + parsed.nice_to_have_skills[:3]

    seen: set[str] = set()
    chunks: list[str] = []
    for query in queries:
        for hit in search_resume(query, k=2):
            if hit["text"] not in seen:
                seen.add(hit["text"])
                chunks.append(hit["text"])
    return "\n\n".join(chunks[:8])


def tailor(parsed: ParsedJD, fit: FitReport, candidate_name: str) -> TailoredOutput:
    chain = PROMPT | get_llm(temperature=0.4).with_structured_output(TailoredOutput)
    return chain.invoke(
        {
            "name": candidate_name,
            "title": parsed.job_title,
            "company": parsed.company or "the company",
            "responsibilities": "\n".join(f"- {r}" for r in parsed.responsibilities),
            "keywords": ", ".join(parsed.required_skills + parsed.keywords),
            "missing": ", ".join(fit.gaps) or "none",
            "evidence": gather_evidence(parsed, fit),
        }
    )