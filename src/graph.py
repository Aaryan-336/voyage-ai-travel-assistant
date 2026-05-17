from langgraph.graph import StateGraph, START, END
from src.state import AgentState
from src.nodes import (
    parse_user_query_node,
    route_city_node,
    route_decision,
    internal_retrieval_node,
    web_search_node,
    summary_refinement_node,
    weather_node,
    image_node,
    final_response_node,
    error_handler_node,
)


def build_graph() -> StateGraph:
    builder = StateGraph(AgentState)

    builder.add_node("parse_user_query", parse_user_query_node)
    builder.add_node("route_city", route_city_node)
    builder.add_node("internal_retrieval", internal_retrieval_node)
    builder.add_node("web_search", web_search_node)
    builder.add_node("summary_refinement", summary_refinement_node)
    builder.add_node("weather", weather_node)
    builder.add_node("images", image_node)
    builder.add_node("final_response", final_response_node)
    builder.add_node("error_handler", error_handler_node)

    builder.add_edge(START, "parse_user_query")
    builder.add_edge("parse_user_query", "route_city")

    builder.add_conditional_edges("route_city", route_decision, {
        "internal": "internal_retrieval",
        "web": "web_search",
        "error": "error_handler",
    })

    builder.add_edge("internal_retrieval", "summary_refinement")
    builder.add_edge("web_search", "summary_refinement")

    # Fan-out: summary_refinement sends to both weather and images in parallel
    builder.add_edge("summary_refinement", "weather")
    builder.add_edge("summary_refinement", "images")

    # Fan-in: both converge on final_response
    builder.add_edge("weather", "final_response")
    builder.add_edge("images", "final_response")

    builder.add_edge("final_response", END)
    builder.add_edge("error_handler", END)

    return builder.compile()


def generate_graph_image(output_path: str = "graph.png"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    bg = "#111111"
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis("off")

    nodes = {
        "START":               (7, 9.5),
        "parse_user_query":    (7, 8.5),
        "route_city":          (7, 7.2),
        "internal_retrieval":  (4, 5.9),
        "web_search":          (10, 5.9),
        "summary_refinement":  (7, 4.6),
        "weather":             (4.5, 3.3),
        "images":              (9.5, 3.3),
        "final_response":      (7, 2.0),
        "error_handler":       (12.5, 4.6),
        "END":                 (7, 0.8),
    }

    edges = [
        ("START", "parse_user_query"), ("parse_user_query", "route_city"),
        ("route_city", "internal_retrieval"), ("route_city", "web_search"),
        ("route_city", "error_handler"),
        ("internal_retrieval", "summary_refinement"), ("web_search", "summary_refinement"),
        ("summary_refinement", "weather"), ("summary_refinement", "images"),
        ("weather", "final_response"), ("images", "final_response"),
        ("final_response", "END"), ("error_handler", "END"),
    ]
    conditional_edges = {
        ("route_city", "internal_retrieval"): "internal",
        ("route_city", "web_search"): "web",
        ("route_city", "error_handler"): "error",
    }
    fan_edges = {
        ("summary_refinement", "weather"), ("summary_refinement", "images"),
        ("weather", "final_response"), ("images", "final_response"),
    }

    for name, (x, y) in nodes.items():
        if name in ("START", "END"):
            circle = plt.Circle((x, y), 0.35, color="#2a2a2a", ec="#c4956a", linewidth=1.5, zorder=3)
            ax.add_patch(circle)
            ax.text(x, y, name, ha="center", va="center", fontsize=9, fontweight="bold", color="#c4956a", zorder=4)
        elif name == "error_handler":
            box = mpatches.FancyBboxPatch((x - 1.2, y - 0.3), 2.4, 0.6, boxstyle="round,pad=0.1",
                                           facecolor="#2a1a1a", edgecolor="#f87171", linewidth=1, zorder=3)
            ax.add_patch(box)
            ax.text(x, y, name, ha="center", va="center", fontsize=8, color="#f87171", fontweight="500", zorder=4)
        else:
            ec = "#c4956a" if "route" in name else "#333333"
            box = mpatches.FancyBboxPatch((x - 1.2, y - 0.3), 2.4, 0.6, boxstyle="round,pad=0.1",
                                           facecolor="#1a1a1a", edgecolor=ec, linewidth=1, zorder=3)
            ax.add_patch(box)
            ax.text(x, y, name, ha="center", va="center", fontsize=8, color="#d6d3d1", fontweight="500", zorder=4)

    for src, dst in edges:
        x1, y1 = nodes[src]
        x2, y2 = nodes[dst]
        color = "#c4956a" if (src, dst) in conditional_edges else ("#2dd4bf" if (src, dst) in fan_edges else "#3a3a3a")
        ax.annotate("", xy=(x2, y2 + 0.35), xytext=(x1, y1 - 0.35),
                     arrowprops=dict(arrowstyle="->", color=color, lw=1.2))
        if (src, dst) in conditional_edges:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx + 0.15, my, conditional_edges[(src, dst)], fontsize=7, color="#c4956a", fontstyle="italic", zorder=5)

    ax.text(7, 0.15, "Travel Explorer — LangGraph Topology", ha="center", fontsize=10, color="#57534e", fontstyle="italic")
    legend_items = [
        mpatches.Patch(color="#3a3a3a", label="Sequential"),
        mpatches.Patch(color="#c4956a", label="Conditional"),
        mpatches.Patch(color="#2dd4bf", label="Fan-out / Fan-in"),
        mpatches.Patch(color="#f87171", label="Error"),
    ]
    ax.legend(handles=legend_items, loc="upper left", fontsize=8, facecolor="#1a1a1a",
              edgecolor="#252525", labelcolor="#a8a29e")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=bg)
    plt.close()
    return output_path

