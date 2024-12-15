from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
import streamlit as st

st.title("Ollama-Bot")

with st.sidebar:
    add_radio = st.radio("Choose a shipping method", ("Standard (5-15 days)", "Express (2-5 days)"))


@st.cache_resource
def load_llm():
    llm = ChatOllama(model="llama3.2-vision", temperature=0.3, streaming=True)
    print("model loaded...")
    return llm


llm = load_llm()

st.session_state.setdefault("messages", [])

# 기존 대화 내용 표시
for msg in st.session_state["messages"]:
    role = "user" if isinstance(msg, HumanMessage) else "ai"
    with st.chat_message(role):
        st.markdown(msg.content)

# 사용자 입력 처리
if prompt := st.chat_input("메시지를 입력하세요."):
    # 사용자 메시지 세션에 기록하고 UI에 출력
    st.session_state["messages"].append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답을 실시간(스트리밍)으로 표시하기 위한 UI 컨테이너
    response_container = st.chat_message("ai")
    text_placeholder = response_container.empty()

    # async 함수를 정의하여 astream 호출
    def generate_response():
        full_text = ""
        # llm의 stream을 통해 토큰 단위로 응답 수신
        for chunk in llm.stream(st.session_state["messages"]):
            full_text += chunk.content
            text_placeholder.markdown(full_text)
        # 완성된 응답을 세션 메시지에 추가
        st.session_state["messages"].append(AIMessage(content=full_text))

    generate_response()
