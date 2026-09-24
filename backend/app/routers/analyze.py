from fastapi import APIRouter, HTTPException

from app.agents.pipeline import get_graph
from app.routers.jd import resolve_jd_text
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.resume_store import resume_count

router = APIRouter(prefix="/analyze", tags=["analyze"])


@router.post("", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    if resume_count() == 0:
        raise HTTPException(400, "Upload your resume first (POST /resume).")

    state = get_graph().invoke(
        {
            "jd_text": resolve_jd_text(req),
            "jd_url": req.jd_url,
            "candidate_name": req.candidate_name,
            "force": req.force,
        }
    )
    return AnalyzeResponse(
        parsed_jd=state["parsed_jd"],
        fit=state["fit"],
        tailored=state.get("tailored"),
    )