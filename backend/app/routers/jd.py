import httpx
from fastapi import APIRouter, HTTPException

from app.agents.jd_parser import parse_jd
from app.schemas import JDInput, ParsedJD
from app.services.jd_fetcher import fetch_jd_text

router = APIRouter(prefix="/jd", tags=["jd"])


def resolve_jd_text(payload: JDInput) -> str:
    if payload.jd_text:
        return payload.jd_text
    try:
        text = fetch_jd_text(payload.jd_url)
    except httpx.HTTPError as exc:
        raise HTTPException(502, f"Could not fetch that URL: {exc}")
    if len(text) < 200:
        raise HTTPException(
            422, "Could not extract enough text from that page. Paste the JD instead."
        )
    return text


@router.post("/parse", response_model=ParsedJD)
def parse(payload: JDInput):
    return parse_jd(resolve_jd_text(payload))