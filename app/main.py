"""
FastAPI backend for the Cloud Architecture Recommendation Framework.

Run with:
    uvicorn app.main:app --reload

Then POST a startup profile to /recommend, e.g.:

curl -X POST http://localhost:8000/recommend -H "Content-Type: application/json" -d '{
  "company_stage": "seed",
  "team_size": 4,
  "monthly_budget_usd": 800,
  "app_type": "web_app",
  "expected_traffic": "unpredictable",
  "handles_payments": true,
  "handles_health_data": false,
  "handles_eu_personal_data": false,
  "preferred_provider": "aws",
  "needs_global_low_latency": false
}'
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.rules_engine import StartupProfile, apply_rules, build_retrieval_query
from app.rag_pipeline import load_vector_store, retrieve, format_context
from app.generation import generate_recommendation

app = FastAPI(
    title="Cloud Architecture Recommendation Framework",
    description="RAG-based cloud architecture recommender for startup enterprises.",
    version="1.0.0",
)

_vector_store = None  # lazy-loaded singleton


class ProfileRequest(BaseModel):
    company_stage: str = Field(..., examples=["pre-seed", "seed", "series-a", "growth"])
    team_size: int
    monthly_budget_usd: float
    app_type: str = Field(..., examples=["web_app", "mobile_backend", "ecommerce", "ml_workload", "saas_api"])
    expected_traffic: str = Field(..., examples=["low", "unpredictable", "steady_moderate", "high_sustained"])
    handles_payments: bool = False
    handles_health_data: bool = False
    handles_eu_personal_data: bool = False
    preferred_provider: str = "any"
    needs_global_low_latency: bool = False


def _get_vector_store():
    global _vector_store
    if _vector_store is None:
        _vector_store = load_vector_store()
    return _vector_store


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recommend")
def recommend(req: ProfileRequest):
    profile = StartupProfile(**req.model_dump())

    # 1. Rules layer narrows candidate services
    suggestion = apply_rules(profile)
    query = build_retrieval_query(profile, suggestion)

    # 2. Retrieval layer pulls grounding context
    try:
        vector_store = _get_vector_store()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    chunks = retrieve(query, vector_store)
    context = format_context(chunks)

    # 3. Generation layer produces the final structured recommendation
    try:
        recommendation = generate_recommendation(profile, suggestion, context)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return {
        "profile": req.model_dump(),
        "rule_suggestions": suggestion.__dict__,
        "retrieval_query": query,
        "sources_used": [c.metadata.get("source", "unknown") for c in chunks],
        "recommendation": recommendation,
    }
