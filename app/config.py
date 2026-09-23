"""
Central configuration for the Cloud Architecture Recommendation Framework.

Reads settings from environment variables (see .env.example). Keeping all
paths and model names in one place makes the project easy to reconfigure
without touching the pipeline logic.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# --- Paths -------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "data" / "knowledge_base"
VECTOR_STORE_DIR = PROJECT_ROOT / "data" / "vector_store"

# --- Embedding model -----------------------------------------------------
# Local, free, no API key required. Swap for an API-based embedding model
# (e.g. OpenAI's text-embedding-3-small) if you prefer and have quota.
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

# --- Text splitting --------------------------------------------------
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "600"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "80"))
RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", "6"))

# --- LLM (generation) -----------------------------------------------
# The framework is written against the Anthropic API by default.
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1500"))
