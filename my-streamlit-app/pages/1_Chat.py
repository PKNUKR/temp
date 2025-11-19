import streamlit as st
from utils.openai_client import get_client

st.title("Chat 페이지")

if "messages" not in st.session_state:
    st.session_state.messages = []

api_key = st.session_state.get("api_key")

if not api_key:
    st.warning("먼저 메인 페이지에서 API Key를 입력하세요.")

user_msg = st.text_input("메시지 입력")

client = None
if api_key:
    client = get_client(api_key)

if st.button("전송") and user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    response = client.responses.create(
        model="gpt-5-mini",
        input=st.session_state.messages
    )
    st.session_state.messages.append({"role": "assistant", "content": response.output_text})

for msg in st.session_state.messages:
    st.write(f"**{msg['role']}:** {msg['content']}")

if st.button("Clear"):
    st.session_state.messages = []
