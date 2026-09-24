# Learning log

## Day 1
- Built: repo, GitHub login, FastAPI /health endpoint
- Confused me:
- Tell a friend: (explain working directory vs staging vs repository in one sentence)

## Day 2
- Built: Groq config, JD parser agent, /jd/parse endpoint
- Confused me:
- Tell a friend: why a schema beats "reply in JSON", and why code must enforce what prompts only request

## Day 3
- Built: ChromaDB resume store, /resume API, fit scorer agent, deterministic scoring with tests
- Confused me: git add -p can't split adjacent added lines into separate hunks
- Tell a friend: RAG always returns the closest match even if nothing is truly relevant, so the LLM has to judge whether retrieved evidence actually proves a skill, not just trust that a result came back

## Day 4
- Built: tailoring agent, LangGraph pipeline with conditional routing, /analyze endpoint
- Confused me: HEAD@{1} needs quotes in PowerShell; squash merge vs regular merge look different in the log
- Tell a friend: a guardrail against "never invent facts" doesn't stop the model from spinning true facts into a stretched, more persuasive argument, that's a different problem