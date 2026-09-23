"""
Calls Groq's free, OpenAI-compatible API to turn (startup profile + rule
suggestions + retrieved knowledge-base context) into a final, structured
architecture recommendation.

Groq (https://console.groq.com) offers a genuinely free tier with no
credit card required, serving fast open-weight models like Llama 3.3 70B.
"""

import json
import re

from openai import OpenAI

from app import config
from app.rules_engine import RuleSuggestion, StartupProfile

SYSTEM_PROMPT = """You are a cloud solutions architect advising early-stage startups.
You will be given a startup's profile, a set of candidate services already narrowed
down by a rules engine, and supporting context retrieved from cloud architecture
documentation.

Respond with ONLY a valid JSON object (no markdown fences, no preamble) with this
exact shape:

{
  "summary": "2-3 sentence high-level summary of the recommended architecture",
  "compute": {"choice": "...", "justification": "..."},
  "database": {"choice": "...", "justification": "..."},
  "storage": {"choice": "...", "justification": "..."},
  "networking": {"choice": "...", "justification": "..."},
  "devops": {"choice": "...", "justification": "..."},
  "estimated_monthly_cost_tier": "low | moderate | high",
  "compliance_notes": ["..."],
  "risks_or_tradeoffs": ["..."]
}

Ground every justification in the provided context where possible. Do not invent
services or pricing figures that are not supported by the context or standard
knowledge of major cloud providers. Keep each justification to 1-2 sentences.
"""


def _build_user_prompt(profile: StartupProfile, suggestion: RuleSuggestion, context: str) -> str:
    return f"""STARTUP PROFILE:
- Stage: {profile.company_stage}
- Team size: {profile.team_size}
- Monthly budget: ${profile.monthly_budget_usd:.0f}
- App type: {profile.app_type}
- Expected traffic: {profile.expected_traffic}
- Preferred provider: {profile.preferred_provider}
- Handles payments: {profile.handles_payments}
- Handles health data: {profile.handles_health_data}
- Handles EU personal data: {profile.handles_eu_personal_data}
- Needs global low latency: {profile.needs_global_low_latency}

RULE-ENGINE CANDIDATE SERVICES:
- Compute: {suggestion.compute}
- Database: {suggestion.database}
- Storage: {suggestion.storage}
- Networking: {suggestion.networking}
- DevOps: {suggestion.devops}
- Compliance notes: {suggestion.compliance_notes}

RETRIEVED CONTEXT FROM KNOWLEDGE BASE:
{context}

Produce the final recommendation as the JSON object described in your instructions.
"""


def generate_recommendation(profile: StartupProfile, suggestion: RuleSuggestion, context: str) -> dict:
    if not config.GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to your .env file before calling the LLM. "
            "Get a free key at https://console.groq.com"
        )

    client = OpenAI(api_key=config.GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
    user_prompt = _build_user_prompt(profile, suggestion, context)

    response = client.chat.completions.create(
        model=config.GROQ_MODEL,
        max_tokens=config.MAX_TOKENS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    raw_text = response.choices[0].message.content
    return _parse_json_response(raw_text)


def _parse_json_response(raw_text: str) -> dict:
    """Strip any accidental markdown fences and parse the model's JSON output."""
    cleaned = re.sub(r"^```(json)?|```$", "", raw_text.strip(), flags=re.MULTILINE).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model did not return valid JSON:\n{raw_text}") from exc