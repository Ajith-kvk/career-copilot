from langchain_core.prompts import ChatPromptTemplate

from app.llm import get_llm
from app.schemas import FitReport, ParsedJD, SkillAssessment
from app.scoring import compute_score
from app.services.resume_store import search_resume

PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a strict but fair resume reviewer. For EACH required skill, "
            "decide using ONLY the resume excerpts provided:\n"
            "- strong: clear hands-on evidence\n"
            "- partial: related or adjacent experience only\n"
            "- missing: no evidence\n"
            "Never invent experience. Return one entry per skill, in order. "
            "Then give 2-4 concrete pieces of advice to close the biggest gaps.",
        ),
        (
            "human",
            "Required skills:\n{skills}\n\nResume excerpts retrieved per skill:\n{evidence}",
        ),
    ]
)


def build_evidence(skills: list[str]) -> str:
    blocks = []
    for skill in skills:
        hits = search_resume(skill, k=2)
        excerpts = "\n".join(f"  - {h['text']}" for h in hits) or "  (nothing found)"
        blocks.append(f"[{skill}]\n{excerpts}")
    return "\n\n".join(blocks)


def score_fit(parsed: ParsedJD) -> FitReport:
    skills = parsed.required_skills[:15]
    if not skills:
        return FitReport(score=0, matches=[], gaps=[], advice=["No skills found in JD."])

    chain = PROMPT | get_llm().with_structured_output(SkillAssessment)
    assessment = chain.invoke(
        {"skills": "\n".join(f"- {s}" for s in skills), "evidence": build_evidence(skills)}
    )
    return FitReport(
        score=compute_score(assessment.matches),
        matches=assessment.matches,
        gaps=[m.skill for m in assessment.matches if m.status == "missing"],
        advice=assessment.advice,
    )