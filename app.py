import streamlit as st
from db import init_db
from chat import init_session_state, set_selected_session, get_selected_session
from ui import sidebar_ui, display_messages, handle_user_input, update_messages
from llm import load_llm

st.title("Ollama-Bot")

# DB 초기화
init_db()

# 세션 스테이트 초기화
init_session_state()

with st.sidebar:
    selected_session_id = sidebar_ui()
    # 세션 선택 변경 시 메시지 로드
    if selected_session_id is not None and selected_session_id != get_selected_session():
        set_selected_session(selected_session_id)

current_session_id = get_selected_session()

if current_session_id is None:
    st.write("채팅방을 선택하거나 새로 만들어 주세요.")
    st.stop()

llm = load_llm()

display_messages(st.session_state["messages"])

prompt = handle_user_input()
if prompt:
    update_messages(current_session_id, prompt, llm)
