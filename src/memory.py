import streamlit as st
from langgraph.checkpoint.memory import MemorySaver
from src.utils import is_followup_query


def get_checkpointer() -> MemorySaver:
    if "checkpointer" not in st.session_state:
        st.session_state.checkpointer = MemorySaver()
    return st.session_state.checkpointer


def save_last_city(city: str):
    st.session_state["last_city"] = city


def get_last_city() -> str | None:
    return st.session_state.get("last_city")


def resolve_query(query: str) -> str:
    """If the query looks like a follow-up, substitute the last city."""
    if is_followup_query(query):
        last = get_last_city()
        if last:
            return f"Tell me about {last}"
    return query
