import streamlit as st
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from src.graph import build_graph, generate_graph_image
from src.memory import save_last_city, get_last_city, resolve_query
from src.ui_components import (
    inject_custom_css, render_header, render_sidebar, render_source_badge,
    render_step_timeline, render_metrics, render_weather_chart,
    render_image_gallery, render_debug_panel,
)

st.set_page_config(page_title="Travel Explorer", page_icon="✈", layout="wide")

if not os.path.exists("graph.png"):
    generate_graph_image("graph.png")

inject_custom_css()
render_sidebar()
render_header()

if "graph" not in st.session_state:
    st.session_state.graph = build_graph()

graph = st.session_state.graph

# Quick-pick buttons
cols = st.columns(5)
examples = ["Paris", "Tokyo", "New York City", "London", "Barcelona"]
for col, city in zip(cols, examples):
    if col.button(city, use_container_width=True):
        st.session_state["query_input"] = f"Tell me about {city}"

st.markdown("")

query = st.text_input(
    "Search",
    key="query_input",
    placeholder="Where do you want to go?",
    label_visibility="collapsed",
)

if not query:
    st.stop()

resolved = resolve_query(query)

with st.spinner("Agent is running..."):
    try:
        result = graph.invoke({"user_query": resolved, "steps": []})
    except Exception as e:
        st.error(f"Agent error: {e}")
        st.stop()

response = result.get("final_response", {})
steps = result.get("steps", [])
city = result.get("normalized_city", "")

if city:
    save_last_city(city)

if response.get("error"):
    st.error(response["city_summary"])
    st.stop()

# ── Results ──
st.markdown("")

left, right = st.columns([3, 1])
with left:
    render_source_badge(response.get("source_used", "Unknown"))
with right:
    score = response.get("confidence_score", 0)
    st.markdown(f'<span class="confidence-pill">Confidence {score:.0%}</span>', unsafe_allow_html=True)

st.markdown("")

# Summary
st.markdown('<p class="section-label">Summary</p>', unsafe_allow_html=True)
raw_summary = response.get("city_summary", "")
clean_summary = raw_summary.replace("## ", "### ").replace("###", "<h3>").replace("\n\n", "</h3>\n<p>") + "</p>"
clean_summary = clean_summary.replace("<p></h3>", "<h3>").replace("</h3>\n<p></p>", "</h3>")
st.markdown(f'<div class="summary-block">{clean_summary}</div>', unsafe_allow_html=True)

# Recommendations
recs = response.get("recommendations", [])
if recs:
    st.markdown("")
    st.markdown('<p class="section-label">Recommendations</p>', unsafe_allow_html=True)
    html = "".join(f'<span class="rec-item">{r}</span>' for r in recs)
    st.markdown(html, unsafe_allow_html=True)

st.markdown("")
st.divider()

# Metrics
render_metrics(response.get("weather_forecast", []), response.get("image_urls", []))

st.markdown("")

# Weather
st.markdown('<p class="section-label">7-day forecast</p>', unsafe_allow_html=True)
render_weather_chart(response.get("weather_forecast", []))

st.divider()

# Images
render_image_gallery(response.get("image_urls", []))

st.markdown("")
st.divider()

# Timeline
render_step_timeline(steps)

st.markdown("")

# Debug
render_debug_panel(result)

# Sidebar last city
last = get_last_city()
if last:
    st.sidebar.divider()
    st.sidebar.caption(f"Last queried → {last.title()}")
