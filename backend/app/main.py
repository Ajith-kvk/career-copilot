from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import jd

from app.routers import jd, resume, analyze

app = FastAPI(title="Career Copilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jd.router)
app.include_router(resume.router)
app.include_router(analyze.router)


@app.get("/health")
def health():
    return {"status": "ok"}