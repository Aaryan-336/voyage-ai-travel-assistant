import streamlit as st
import plotly.graph_objects as go


def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');

    /* ── Animations ── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(18px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 8px rgba(45,212,191,0.15); }
        50% { box-shadow: 0 0 20px rgba(45,212,191,0.3); }
    }
    @keyframes gradientText {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes dotBounce {
        0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
        40% { transform: scale(1.2); opacity: 1; }
    }

    /* ── Base ── */
    html, body, .stApp, .stApp * {
        font-family: 'DM Sans', -apple-system, sans-serif !important;
    }
    .stApp {
        background: #0e0e0e !important;
        color: #f5f5f4 !important;
    }
    .stApp *, div[data-testid="stSidebar"] * { color: #d6d3d1 !important; }
    .stApp strong, .stApp b { color: #f5f5f4 !important; }

    /* ── Sidebar ── */
    div[data-testid="stSidebar"],
    div[data-testid="stSidebar"] > div:first-child,
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div:first-child {
        background: #131313 !important;
        border-right: 1px solid #1c1c1c !important;
    }
    div[data-testid="stSidebar"] .stMarkdown h3 { color: #f5f5f4 !important; }
    div[data-testid="stSidebar"] .stMarkdown h5 { color: #a8a29e !important; }

    /* ── Header ── */
    .hero {
        padding: 2rem 0 0.5rem 0;
        animation: fadeInUp 0.7s ease-out;
    }
    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 0;
        background: linear-gradient(135deg, #f5f5f4, #c4956a, #2dd4bf, #f5f5f4);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientText 6s ease infinite;
    }
    .hero-sub {
        font-size: 0.9rem;
        color: #57534e !important;
        font-weight: 400;
        margin-top: 0.3rem;
        letter-spacing: 0.5px;
    }
    .hero-accent {
        width: 48px;
        height: 3px;
        background: linear-gradient(90deg, #c4956a, #2dd4bf);
        border-radius: 2px;
        margin-top: 1rem;
        margin-bottom: 1.2rem;
    }

    /* ── Buttons ── */
    .stApp button[kind="secondary"], .stApp button {
        background: #161616 !important;
        border: 1px solid #2a2a2a !important;
        color: #a8a29e !important;
        border-radius: 10px !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        padding: 0.55rem 1.2rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
    }
    .stApp button:hover {
        background: #1e1e1e !important;
        border-color: #c4956a !important;
        color: #c4956a !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(196,149,106,0.08) !important;
    }
    .stApp button:active {
        transform: translateY(0) !important;
    }

    /* ── Input ── */
    .stApp input[type="text"], .stApp textarea {
        background: #141414 !important;
        border: 1px solid #252525 !important;
        color: #f5f5f4 !important;
        border-radius: 12px !important;
        padding: 0.7rem 1rem !important;
        font-size: 0.95rem !important;
        transition: all 0.25s ease !important;
    }
    .stApp input[type="text"]:focus {
        border-color: #c4956a !important;
        box-shadow: 0 0 0 2px rgba(196,149,106,0.1) !important;
    }

    /* ── Cards ── */
    .card {
        background: #151515;
        border: 1px solid #1e1e1e;
        border-radius: 14px;
        padding: 1.4rem;
        margin-bottom: 0.6rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.5s ease-out both;
    }
    .card:hover {
        border-color: #2a2a2a;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }
    .card-label {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #57534e !important;
        margin-bottom: 0.6rem;
        font-weight: 600;
    }
    .card-value {
        font-size: 2rem;
        font-weight: 700;
        color: #f5f5f4 !important;
        line-height: 1;
    }
    .card-unit {
        font-size: 0.8rem;
        color: #78716c !important;
        font-weight: 400;
    }
    .card-1 { animation-delay: 0.05s; }
    .card-2 { animation-delay: 0.1s; }
    .card-3 { animation-delay: 0.15s; }
    .card-4 { animation-delay: 0.2s; }

    /* ── Source tag ── */
    .source-tag {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 8px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .source-internal {
        background: rgba(45, 212, 191, 0.08);
        color: #2dd4bf !important;
        border: 1px solid rgba(45,212,191,0.15);
        animation: pulseGlow 3s ease-in-out infinite;
    }
    .source-web {
        background: rgba(196, 149, 106, 0.08);
        color: #c4956a !important;
        border: 1px solid rgba(196,149,106,0.15);
    }

    /* ── Section label ── */
    .section-label {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 2.5px;
        color: #44403c !important;
        font-weight: 700;
        margin-bottom: 0.8rem;
        margin-top: 1.5rem;
        position: relative;
        display: inline-block;
    }
    .section-label::after {
        content: '';
        position: absolute;
        bottom: -4px;
        left: 0;
        width: 100%;
        height: 1px;
        background: linear-gradient(90deg, #c4956a, transparent);
    }

    /* ── Summary ── */
    .summary-block {
        background: #131313;
        border: 1px solid #1c1c1c;
        border-left: 3px solid #c4956a;
        border-radius: 0 12px 12px 0;
        padding: 1.6rem;
        animation: fadeInUp 0.6s ease-out both;
        animation-delay: 0.1s;
        line-height: 1.8;
        color: #d6d3d1 !important;
        font-size: 0.92rem;
    }
    .summary-block h3 {
        color: #f5f5f4 !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }

    /* ── Recommendations ── */
    .rec-item {
        display: inline-block;
        padding: 7px 16px;
        background: #141414;
        border: 1px solid #1e1e1e;
        border-radius: 20px;
        font-size: 0.78rem;
        color: #a8a29e !important;
        margin: 4px 3px;
        transition: all 0.2s ease;
    }
    .rec-item:hover {
        border-color: #c4956a;
        color: #c4956a !important;
        background: rgba(196,149,106,0.05);
    }

    /* ── Timeline ── */
    .timeline { margin: 0.5rem 0; animation: fadeInUp 0.6s ease-out both; animation-delay: 0.2s; }
    .timeline-step {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 9px 0;
        transition: all 0.2s ease;
    }
    .timeline-step:hover { padding-left: 6px; }
    .timeline-dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        flex-shrink: 0;
        transition: transform 0.2s ease;
    }
    .timeline-step:hover .timeline-dot { transform: scale(1.4); }
    .dot-ok { background: #2dd4bf; }
    .dot-err { background: #f87171; }
    .timeline-label {
        font-size: 0.82rem;
        color: #78716c !important;
    }
    .timeline-label b { color: #a8a29e !important; }

    /* ── Images ── */
    .stImage img {
        border-radius: 12px !important;
        border: 1px solid #1e1e1e !important;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stImage img:hover {
        transform: scale(1.02) !important;
        border-color: #2a2a2a !important;
        box-shadow: 0 12px 32px rgba(0,0,0,0.4) !important;
    }

    /* ── Dividers ── */
    hr { border-color: #1a1a1a !important; opacity: 0.6 !important; }

    /* ── Expander ── */
    [data-testid="stExpander"] {
        border: 1px solid #1c1c1c !important;
        border-radius: 12px !important;
        background: #111111 !important;
    }
    [data-testid="stExpander"] summary { color: #57534e !important; font-size: 0.85rem !important; }

    /* ── JSON / Code ── */
    pre, code, [data-testid="stJson"] {
        background: #0e0e0e !important;
        color: #c4956a !important;
        border-radius: 8px !important;
        border: 1px solid #1c1c1c !important;
    }

    /* ── Status widget ── */
    [data-testid="stStatusWidget"] {
        background: #131313 !important;
        border: 1px solid #1e1e1e !important;
        border-radius: 10px !important;
    }

    /* ── Confidence pill ── */
    .confidence-pill {
        display: inline-block;
        padding: 4px 12px;
        background: #141414;
        border: 1px solid #1e1e1e;
        border-radius: 6px;
        font-size: 0.75rem;
        color: #78716c !important;
        font-weight: 500;
    }

    /* ── Ambient background dots ── */
    .ambient {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    .ambient-dot {
        position: absolute;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(196,149,106,0.06) 0%, transparent 70%);
    }

    /* hide streamlit chrome */
    footer { visibility: hidden; }

    /* Fix: sidebar collapse/expand buttons showing icon names as text (excluding Main Menu) */
    button[data-testid="stBaseButton-headerNoPadding"]:not([aria-label="Main menu"]),
    [data-testid="stSidebarCollapseButton"]:not([aria-label="Main menu"]),
    [data-testid="collapsedSidebar"] button:not([aria-label="Main menu"]),
    button[aria-label="Collapse sidebar"],
    button[aria-label="Expand sidebar"],
    .stApp > button:first-of-type:not([aria-label="Main menu"]),
    div[data-testid="stSidebar"] button:first-of-type,
    button[class*="e7msn5c15"]:not([aria-label="Main menu"]):first-of-type {
        font-size: 0 !important;
        width: 28px !important;
        height: 28px !important;
        min-width: 28px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: #161616 !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 6px !important;
        cursor: pointer !important;
        position: relative !important;
        z-index: 99999 !important;
    }
    
    /* Default Chevron for Sidebar Open (pointing right - e.g. when collapsed) */
    button[data-testid="stBaseButton-headerNoPadding"]:not([aria-label="Main menu"])::after,
    [data-testid="stSidebarCollapseButton"]:not([aria-label="Main menu"])::after,
    [data-testid="collapsedSidebar"] button:not([aria-label="Main menu"])::after,
    button[aria-label="Expand sidebar"]::after,
    .stApp > button:first-of-type:not([aria-label="Main menu"])::after,
    button[class*="e7msn5c15"]:not([aria-label="Main menu"]):first-of-type::after {
        content: '›' !important;
        font-size: 18px !important;
        color: #78716c !important;
        line-height: 1 !important;
        display: block !important;
    }

    /* Chevron for Sidebar Close (pointing left - overridden when sidebar is actually open) */
    [data-testid="stSidebar"] button:first-of-type::after,
    [data-testid="stSidebar"] button[class*="e7msn5c15"]:not([aria-label="Main menu"]):first-of-type::after,
    [data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"]::after,
    button[aria-label="Collapse sidebar"]::after {
        content: '‹' !important;
        font-size: 18px !important;
        color: #78716c !important;
        line-height: 1 !important;
        display: block !important;
    }
    
    /* Nuclear hide for any default icons or text inside these buttons */
    button[data-testid="stBaseButton-headerNoPadding"]:not([aria-label="Main menu"]) span,
    button[data-testid="stBaseButton-headerNoPadding"]:not([aria-label="Main menu"]) svg,
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="collapsedSidebar"] button span,
    [data-testid="collapsedSidebar"] button svg,
    button[aria-label="Collapse sidebar"] span,
    button[aria-label="Collapse sidebar"] svg,
    button[aria-label="Expand sidebar"] span,
    button[aria-label="Expand sidebar"] svg,
    .stApp > button:first-of-type span,
    .stApp > button:first-of-type svg,
    [data-testid="stSidebar"] button:first-of-type span,
    [data-testid="stSidebar"] button:first-of-type svg,
    button[class*="e7msn5c15"]:not([aria-label="Main menu"]):first-of-type span,
    button[class*="e7msn5c15"]:not([aria-label="Main menu"]):first-of-type svg {
        display: none !important;
        visibility: hidden !important;
        font-size: 0 !important;
        width: 0 !important;
        height: 0 !important;
    }

    /* Fix: expander header — hide icon text leak + clean styling */
    [data-testid="stExpander"] {
        position: relative !important;
        z-index: 1 !important;
        overflow: hidden !important;
    }
    [data-testid="stExpander"] summary {
        background: #131313 !important;
        padding: 0.8rem 1.2rem !important;
        border-radius: 12px !important;
        position: relative !important;
        z-index: 2 !important;
        overflow: hidden !important;
    }
    /* Hide the Streamlit icon element that leaks 'expand_more' / 'ba' text */
    [data-testid="stExpander"] summary [data-testid="stIconMaterial"],
    [data-testid="stExpander"] summary .material-symbols-rounded,
    [data-testid="stExpander"] summary span[style*="font-variation"],
    [data-testid="stExpander"] summary > div > div:first-child > span:first-child {
        font-size: 0 !important;
        width: 0 !important;
        overflow: hidden !important;
        display: inline-block !important;
        visibility: hidden !important;
    }
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span {
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Ambient background dots
    st.markdown("""
    <div class="ambient">
        <div class="ambient-dot" style="width:400px;height:400px;top:10%;right:-100px;"></div>
        <div class="ambient-dot" style="width:300px;height:300px;bottom:20%;left:-80px;background:radial-gradient(circle, rgba(45,212,191,0.04) 0%, transparent 70%);"></div>
        <div class="ambient-dot" style="width:200px;height:200px;top:50%;left:40%;background:radial-gradient(circle, rgba(196,149,106,0.03) 0%, transparent 70%);"></div>
    </div>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div class="hero">
        <h1 class="hero-title">Travel Explorer</h1>
        <p class="hero-sub">LangGraph agent · Vector retrieval · Structured output</p>
        <div class="hero-accent"></div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("")
        st.markdown("### ✦ Architecture")
        st.markdown("""
        The agent parses your query, identifies a city, and routes
        it through a **LangGraph** state machine.

        Known cities → **ChromaDB** vector store
        Unknown cities → mock web search fallback

        Weather + images fetched in **parallel** via fan-out,
        then assembled into a structured Pydantic response.
        """)
        st.divider()
        st.markdown("##### Known Cities")
        cols = st.columns(3)
        cities = ["🗼 Paris", "🏯 Tokyo", "🗽 NYC"]
        for col, city in zip(cols, cities):
            col.caption(city)
        st.caption("_Other cities → web search fallback_")
        st.divider()
        st.markdown("##### Registered Tools")
        st.code("weather · images · web_search", language=None)
        st.divider()
        if __import__("os").path.exists("graph.png"):
            st.markdown("##### Agent Topology")
            st.image("graph.png", width="stretch")


def render_source_badge(source: str):
    cls = "source-internal" if "Vector" in source else "source-web"
    st.markdown(f'<span class="source-tag {cls}">{source}</span>', unsafe_allow_html=True)


def render_step_timeline(steps: list):
    st.markdown('<p class="section-label">Execution trace</p>', unsafe_allow_html=True)
    html = '<div class="timeline">'
    for step in steps:
        dot = "dot-ok" if step.get("status") == "done" else "dot-err"
        html += f'<div class="timeline-step"><span class="timeline-dot {dot}"></span><span class="timeline-label"><b>{step["node"]}</b> — {step.get("detail", "")}</span></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def render_metrics(weather_data: list, image_urls: list):
    if not weather_data:
        return
    temps = [w["temperature"] for w in weather_data]
    avg_temp = sum(temps) / len(temps)
    cols = st.columns(4)
    metrics = [
        ("Avg Temp", f"{avg_temp:.1f}", "°C"),
        ("Warmest", f"{max(temps):.1f}", "°C"),
        ("Coldest", f"{min(temps):.1f}", "°C"),
        ("Photos", str(len(image_urls)), "found"),
    ]
    for i, (col, (label, value, unit)) in enumerate(zip(cols, metrics)):
        with col:
            st.markdown(
                f'<div class="card card-{i+1}">'
                f'<div class="card-label">{label}</div>'
                f'<div class="card-value">{value} <span class="card-unit">{unit}</span></div>'
                f'</div>',
                unsafe_allow_html=True,
            )


def render_weather_chart(weather_data: list):
    if not weather_data:
        return
    dates = [w["date"][-5:] for w in weather_data]
    temps = [w["temperature"] for w in weather_data]
    humidity = [w["humidity"] for w in weather_data]
    conditions = [w["condition"] for w in weather_data]

    fig = go.Figure()
    # Temperature area fill
    fig.add_trace(go.Scatter(
        x=dates, y=temps, mode="lines", name="",
        line=dict(width=0), fill="tozeroy",
        fillcolor="rgba(196,149,106,0.06)", showlegend=False,
        hoverinfo="skip",
    ))
    # Temperature line
    fig.add_trace(go.Scatter(
        x=dates, y=temps, mode="lines+markers+text", name="Temperature",
        line=dict(color="#c4956a", width=2.5, shape="spline"),
        marker=dict(size=8, color="#c4956a", line=dict(width=2, color="#0e0e0e")),
        text=[f"{t}°" for t in temps], textposition="top center",
        textfont=dict(size=10, color="#c4956a"),
        hovertemplate="<b>%{x}</b><br>%{y}°C · " + "%{customdata}<extra></extra>",
        customdata=conditions,
    ))
    # Humidity bars
    fig.add_trace(go.Bar(
        x=dates, y=humidity, name="Humidity",
        marker_color="rgba(45,212,191,0.1)",
        marker_line=dict(width=0),
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>Humidity: %{y}%<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#57534e", size=11),
        yaxis=dict(title="", gridcolor="rgba(255,255,255,0.02)", zeroline=False, showticklabels=True),
        yaxis2=dict(title="", overlaying="y", side="right", showgrid=False, zeroline=False, showticklabels=False, range=[0, 200]),
        xaxis=dict(gridcolor="rgba(255,255,255,0.02)", tickfont=dict(color="#78716c")),
        legend=dict(orientation="h", y=1.08, x=0, font=dict(size=10, color="#78716c")),
        margin=dict(l=5, r=5, t=25, b=5), height=280,
        hoverlabel=dict(bgcolor="#1a1a1a", font_color="#f5f5f4", font_size=12, bordercolor="#2a2a2a"),
    )
    st.plotly_chart(fig, width="stretch")


def render_image_gallery(image_urls: list):
    if not image_urls:
        return
    st.markdown('<p class="section-label">Gallery</p>', unsafe_allow_html=True)
    cols = st.columns(3, gap="small")
    for i, url in enumerate(image_urls[:6]):
        with cols[i % 3]:
            st.image(url, width="stretch")


def render_debug_panel(state: dict):
    with st.expander("Debug · Agent state & JSON"):
        col1, col2 = st.columns(2)
        with col1:
            st.caption("DETECTED CITY")
            st.markdown(f"**{state.get('detected_city', '—')}**")
            st.caption("ROUTE")
            st.markdown(f"**{state.get('route', '—')}**")
        with col2:
            st.caption("SOURCE")
            st.markdown(f"**{state.get('source_used', '—')}**")
            st.caption("CONFIDENCE")
            st.markdown(f"**{state.get('confidence_score', '—')}**")
        st.divider()
        st.caption("STRUCTURED OUTPUT")
        st.json(state.get("final_response", {}))
