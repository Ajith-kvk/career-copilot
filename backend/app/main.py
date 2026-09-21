from fastapi import FastAPI

app = FastAPI(title="Career Copilot API")

@app.get("/health")
def health():
    return {"status": "working."}