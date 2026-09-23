
from dataclasses import dataclass, field
from typing import List


@dataclass
class StartupProfile:
    company_stage: str          # "pre-seed", "seed", "series-a", "growth"
    team_size: int
    monthly_budget_usd: float
    app_type: str                # "web_app", "mobile_backend", "ecommerce", "ml_workload", "saas_api"
    expected_traffic: str        # "low", "unpredictable", "steady_moderate", "high_sustained"
    handles_payments: bool = False
    handles_health_data: bool = False
    handles_eu_personal_data: bool = False
    preferred_provider: str = "any"   # "aws", "azure", "gcp", "any"
    needs_global_low_latency: bool = False


@dataclass
class RuleSuggestion:
    compute: List[str] = field(default_factory=list)
    database: List[str] = field(default_factory=list)
    storage: List[str] = field(default_factory=list)
    networking: List[str] = field(default_factory=list)
    devops: List[str] = field(default_factory=list)
    compliance_notes: List[str] = field(default_factory=list)


def apply_rules(profile: StartupProfile) -> RuleSuggestion:
    suggestion = RuleSuggestion()

    # --- Compute ---------------------------------------------------
    if profile.company_stage in ("pre-seed", "seed") or profile.expected_traffic == "unpredictable":
        suggestion.compute += ["serverless functions", "managed container service (scale-to-zero)"]
    elif profile.expected_traffic == "steady_moderate":
        suggestion.compute += ["managed container service", "Kubernetes (if team has DevOps capacity)"]
    elif profile.expected_traffic == "high_sustained":
        suggestion.compute += ["Kubernetes", "reserved/committed-use VM instances"]

    if profile.app_type == "ml_workload":
        suggestion.compute.append("managed ML platform (GPU-enabled) rather than serverless")

    # --- Database ----------------------------------------------------
    if profile.app_type in ("web_app", "saas_api", "ecommerce"):
        suggestion.database.append("managed relational database with autoscaling tier")
    if profile.needs_global_low_latency or profile.expected_traffic == "high_sustained":
        suggestion.database.append("NoSQL document database for high-throughput/global access patterns")
    if profile.app_type == "mobile_backend":
        suggestion.database.append("NoSQL/document database (flexible schema, mobile SDK support)")

    # --- Storage -----------------------------------------------------
    suggestion.storage.append("object storage with lifecycle policies for static/media assets")
    if profile.expected_traffic in ("steady_moderate", "high_sustained"):
        suggestion.storage.append("CDN in front of object storage / static assets")

    # --- Networking ----------------------------------------------------
    suggestion.networking.append("managed API gateway for authentication, rate limiting, routing")
    if profile.expected_traffic in ("steady_moderate", "high_sustained"):
        suggestion.networking.append("managed load balancer across compute instances")

    # --- DevOps -------------------------------------------------------
    suggestion.devops.append("managed CI/CD pipeline from first production deployment")
    if profile.team_size > 2:
        suggestion.devops.append("Infrastructure as Code (Terraform/CDK/Bicep)")
    suggestion.devops.append("centralized logging and basic uptime/error alerting")

    # --- Compliance ----------------------------------------------------
    if profile.handles_payments:
        suggestion.compliance_notes.append(
            "Offload card handling to a PCI-DSS compliant payment processor rather than storing card data directly."
        )
    if profile.handles_health_data:
        suggestion.compliance_notes.append(
            "Select HIPAA-eligible services and enforce encryption at rest and in transit as a baseline."
        )
    if profile.handles_eu_personal_data:
        suggestion.compliance_notes.append(
            "Select EU-region deployments and GDPR-compliant data processing agreements with providers."
        )

    return suggestion


def build_retrieval_query(profile: StartupProfile, suggestion: RuleSuggestion) -> str:
    """Turn the profile + rule suggestions into a natural-language query for the retriever."""
    parts = [
        f"Cloud architecture recommendation for a {profile.company_stage}-stage startup",
        f"with a team of {profile.team_size}, building a {profile.app_type.replace('_', ' ')}",
        f"expecting {profile.expected_traffic.replace('_', ' ')} traffic",
        f"on a monthly budget of about ${profile.monthly_budget_usd:.0f}.",
    ]
    if profile.preferred_provider != "any":
        parts.append(f"Preferred cloud provider: {profile.preferred_provider.upper()}.")
    if profile.handles_payments:
        parts.append("Handles payment data.")
    if profile.handles_health_data:
        parts.append("Handles health data.")
    if profile.handles_eu_personal_data:
        parts.append("Handles EU personal data.")
    parts.append("Candidate compute options: " + ", ".join(suggestion.compute) + ".")
    parts.append("Candidate database options: " + ", ".join(suggestion.database) + ".")
    return " ".join(parts)
