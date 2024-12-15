from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
import streamlit as st


@st.cache_resource
def load_llm(model_name="llama3.2-vision", temperature=0.3, streaming=True):
    llm = ChatOllama(model=model_name, temperature=temperature, streaming=streaming)
    print("model loaded...")
    return llm


def generate_ai_response(llm, messages):
    response_container = st.chat_message("ai")
    text_placeholder = response_container.empty()
    full_text = ""
    for chunk in llm.stream(messages):
        full_text += chunk.content
        text_placeholder.markdown(full_text)
    return full_text


def generate_title(messages, llm):
    # 대화 내용을 문자열로 변환
    conversation = "\n".join(
        [f"User: {msg.content}" if isinstance(msg, HumanMessage) else f"Assistant: {msg.content}" for msg in messages]
    )

    # 제목 생성을 위한 프롬프트
    prompt = f"""아래 대화 내용을 바탕으로 15자 이내의 간단한 제목을 생성해주세요.
    대화 내용을 잘 요약할 수 있는 제목이어야 합니다.
    제목만 출력하세요.

    대화 내용:
    {conversation}
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()
