from functools import lru_cache
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.agents.fit_scorer import score_fit
from app.agents.jd_parser import parse_jd
from app.agents.tailor import tailor
from app.config import settings
from app.schemas import FitReport, ParsedJD, TailoredOutput


class PipelineState(TypedDict, total=False):
    jd_text: str
    jd_url: str | None
    candidate_name: str
    force: bool
    parsed_jd: ParsedJD
    fit: FitReport
    tailored: TailoredOutput


def parse_node(state: PipelineState) -> dict:
    return {"parsed_jd": parse_jd(state["jd_text"])}


def score_node(state: PipelineState) -> dict:
    return {"fit": score_fit(state["parsed_jd"])}


def tailor_node(state: PipelineState) -> dict:
    return {
        "tailored": tailor(
            state["parsed_jd"], state["fit"], state.get("candidate_name", "Candidate")
        )
    }


def route_after_score(state: PipelineState) -> str:
    if state["fit"].score < settings.min_fit_to_tailor and not state.get("force"):
        return "skip"
    return "tailor"


def build_graph():
    g = StateGraph(PipelineState)
    g.add_node("parse", parse_node)
    g.add_node("score", score_node)
    g.add_node("tailor", tailor_node)

    g.add_edge(START, "parse")
    g.add_edge("parse", "score")
    g.add_conditional_edges("score", route_after_score, {"tailor": "tailor", "skip": END})
    g.add_edge("tailor", END)
    return g.compile()


@lru_cache
def get_graph():
    return build_graph()