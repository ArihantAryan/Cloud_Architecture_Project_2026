<<<<<<< HEAD
# Generative AI-Based Cloud Architecture Recommendation Framework
### (RAG for Startup Enterprises)

A working reference implementation of a RAG pipeline that recommends cloud
architectures (compute, database, storage, networking, DevOps) to a startup
based on its profile, grounded in a retrievable knowledge base of cloud
architecture guidance.

## How it works

1. **Rules engine** (`app/rules_engine.py`) takes a structured startup
   profile (stage, team size, budget, app type, traffic pattern, compliance
   needs) and narrows candidate services using deterministic heuristics.
2. **Retrieval** (`app/rag_pipeline.py`) embeds the knowledge base
   (`data/knowledge_base/*.md`) with a local sentence-transformers model,
   stores vectors in Chroma, and retrieves the most relevant passages for
   the profile.
3. **Generation** (`app/generation.py`) sends the profile + rule
   suggestions + retrieved context to Claude, which returns a structured
   JSON recommendation grounded in that context.
4. **Diagram** (`app/diagram.py`) renders the recommendation as a Graphviz
   architecture diagram.
5. Exposed via a **FastAPI** backend (`app/main.py`) and a **Streamlit**
   demo UI (`streamlit_app.py`).

## Project structure

```
cloud_rag_project/
├── app/
│   ├── config.py          # paths, model names, env-driven settings
│   ├── rules_engine.py    # StartupProfile + heuristic rules
│   ├── rag_pipeline.py    # chunking, embeddings, vector store, retrieval
│   ├── build_index.py     # script to (re)build the vector store
│   ├── generation.py      # Claude API call -> structured recommendation
│   ├── diagram.py         # Graphviz architecture diagram builder
│   └── main.py            # FastAPI app
├── data/
│   └── knowledge_base/    # source markdown docs (compute, database, etc.)
├── streamlit_app.py        # demo frontend
├── requirements.txt
└── .env.example
```

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure your API key
cp .env.example .env
# edit .env and set ANTHROPIC_API_KEY

# 4. Build the vector index from the knowledge base (run once, and again
#    whenever you edit/add files under data/knowledge_base/)
python -m app.build_index
```

## Running the demo (Streamlit — easiest for a project demo)

```bash
streamlit run streamlit_app.py
```

Fill in the startup profile in the sidebar and click **Get Recommendation**.

## Running the API (FastAPI)

```bash
uvicorn app.main:app --reload
```

Then test it:

```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{
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
```

Interactive API docs are auto-generated at `http://localhost:8000/docs`.

## Extending this for your project report

- **Grow the knowledge base**: add more `.md` files under
  `data/knowledge_base/` (real AWS/Azure/GCP whitepapers, case studies,
  pricing docs). Re-run `python -m app.build_index` after any change.
- **Swap the embedding model**: change `EMBEDDING_MODEL_NAME` in `.env` to
  an API-based model (e.g. OpenAI's `text-embedding-3-small`) if you want
  to compare retrieval quality.
- **Evaluation**: for your report, test a handful of representative startup
  profiles, manually score whether the retrieved sources are relevant and
  whether the final recommendation is faithful to them (no hallucinated
  services/pricing). Frameworks like RAGAS can automate faithfulness and
  relevance scoring if you want a quantitative section.
- **Swap the LLM provider**: `app/generation.py` isolates the API call, so
  swapping to another provider only requires editing that one file.

## Notes

- The embedding model runs locally (no API key needed) — only the final
  generation step calls the Anthropic API, keeping running costs low for a
  student project.
- The rules engine is intentionally simple and meant to be extended; it
  exists so the LLM has a consistent starting point rather than free-form
  reasoning over the full candidate space every time.
=======
# Cloud_Architecture_Project_2026
GitHub repository for Cloud Architecture Project
>>>>>>> origin/main
