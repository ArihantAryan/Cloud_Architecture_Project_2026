

import streamlit as st

from app.rules_engine import StartupProfile, apply_rules, build_retrieval_query
from app.rag_pipeline import load_vector_store, retrieve, format_context
from app.generation import generate_recommendation
from app.diagram import build_architecture_diagram

st.set_page_config(page_title="Cloud Architecture Recommender", layout="wide")
st.title("☁️ Generative AI Cloud Architecture Recommender")
st.caption("RAG-based cloud architecture recommendation framework for startup enterprises")

with st.sidebar:
    st.header("Startup Profile")
    company_stage = st.selectbox("Company stage", ["pre-seed", "seed", "series-a", "growth"])
    team_size = st.number_input("Team size", min_value=1, max_value=500, value=4)
    monthly_budget_usd = st.number_input("Monthly cloud budget (USD)", min_value=0, value=800)
    app_type = st.selectbox(
        "App type", ["web_app", "mobile_backend", "ecommerce", "ml_workload", "saas_api"]
    )
    expected_traffic = st.selectbox(
        "Expected traffic", ["low", "unpredictable", "steady_moderate", "high_sustained"]
    )
    preferred_provider = st.selectbox("Preferred provider", ["any", "aws", "azure", "gcp"])
    needs_global_low_latency = st.checkbox("Needs global low latency")
    handles_payments = st.checkbox("Handles payments")
    handles_health_data = st.checkbox("Handles health data")
    handles_eu_personal_data = st.checkbox("Handles EU personal data")
    submitted = st.button("Get Recommendation", type="primary")

if submitted:
    profile = StartupProfile(
        company_stage=company_stage,
        team_size=team_size,
        monthly_budget_usd=monthly_budget_usd,
        app_type=app_type,
        expected_traffic=expected_traffic,
        handles_payments=handles_payments,
        handles_health_data=handles_health_data,
        handles_eu_personal_data=handles_eu_personal_data,
        preferred_provider=preferred_provider,
        needs_global_low_latency=needs_global_low_latency,
    )

    with st.spinner("Applying rules engine..."):
        suggestion = apply_rules(profile)
        query = build_retrieval_query(profile, suggestion)

    with st.spinner("Retrieving relevant architecture guidance..."):
        try:
            vector_store = load_vector_store()
        except FileNotFoundError as exc:
            st.error(str(exc))
            st.stop()
        chunks = retrieve(query, vector_store)
        context = format_context(chunks)

    with st.spinner("Generating recommendation with Claude..."):
        try:
            recommendation = generate_recommendation(profile, suggestion, context)
        except Exception as exc:
            st.error(f"Generation failed: {exc}")
            st.stop()

    st.success("Recommendation ready")

    st.subheader("Summary")
    st.write(recommendation.get("summary", ""))

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Recommended Architecture")
        for key in ["compute", "database", "storage", "networking", "devops"]:
            block = recommendation.get(key, {})
            st.markdown(f"**{key.title()}**: {block.get('choice', '-')}")
            st.caption(block.get("justification", ""))

        st.markdown(f"**Estimated monthly cost tier**: {recommendation.get('estimated_monthly_cost_tier', '-')}")

        if recommendation.get("compliance_notes"):
            st.subheader("Compliance Notes")
            for note in recommendation["compliance_notes"]:
                st.write(f"- {note}")

        if recommendation.get("risks_or_tradeoffs"):
            st.subheader("Risks / Trade-offs")
            for risk in recommendation["risks_or_tradeoffs"]:
                st.write(f"- {risk}")

    with col2:
        st.subheader("Architecture Diagram")
        dot = build_architecture_diagram(recommendation)
        st.graphviz_chart(dot)

        st.subheader("Retrieved Sources")
        for source in set(c.metadata.get("source", "unknown") for c in chunks):
            st.write(f"- {source.split('/')[-1]}")

    with st.expander("Debug: retrieval query + raw retrieved context"):
        st.code(query)
        st.text(context)
else:
    st.info("Fill in the startup profile in the sidebar and click **Get Recommendation**.")
