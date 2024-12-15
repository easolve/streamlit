import streamlit as st
from db import load_history


def set_selected_session(session_id: int):
    st.session_state["selected_session_id"] = session_id
    st.session_state["messages"] = load_history(session_id)


def get_selected_session():
    return st.session_state.get("selected_session_id", None)


def init_session_state():
    if "selected_session_id" not in st.session_state:
        st.session_state["selected_session_id"] = None
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
