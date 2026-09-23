

import graphviz


def build_architecture_diagram(recommendation: dict) -> graphviz.Digraph:
    dot = graphviz.Digraph("architecture", format="png")
    dot.attr(rankdir="LR", bgcolor="white")
    dot.attr("node", shape="box", style="rounded,filled", fontname="Helvetica", fontsize="11")

    def node(key: str, color: str):
        choice = recommendation.get(key, {}).get("choice", key.title())
        dot.node(key, f"{key.title()}\n{choice}", fillcolor=color)

    dot.node("client", "Client\n(Web / Mobile)", fillcolor="#E8F0FE")
    node("networking", "#FFF3CD")
    node("compute", "#D4EDDA")
    node("database", "#D1ECF1")
    node("storage", "#F8D7DA")
    node("devops", "#E2E3E5")

    dot.edge("client", "networking")
    dot.edge("networking", "compute")
    dot.edge("compute", "database")
    dot.edge("compute", "storage")
    dot.edge("devops", "compute", style="dashed", label="deploys")

    return dot
