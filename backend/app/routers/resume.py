from fastapi import APIRouter
from pydantic import BaseModel

from app.services.resume_store import ingest_resume, resume_count, search_resume

router = APIRouter(prefix="/resume", tags=["resume"])


class ResumeIn(BaseModel):
    text: str


@router.post("")
def upload_resume(body: ResumeIn):
    return {"chunks": ingest_resume(body.text)}


@router.get("/status")
def status():
    return {"chunks": resume_count()}


@router.get("/search")
def search(q: str, k: int = 3):
    return search_resume(q, k)