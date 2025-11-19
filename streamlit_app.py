import streamlit as st
from utils.openai_client import get_client

st.set_page_config(page_title="GPT-5-mini Q/A", layout="centered")

st.title("GPT-5-mini 질의응답")

api_key = st.text_input("Enter your OpenAI API Key", type="password")

if api_key:
    st.session_state["api_key"] = api_key

@st.cache_data
def ask_gpt(question, api_key):
    client = get_client(api_key)
    response = client.responses.create(
        model="gpt-5-mini",
        input=question
    )
    return response.output_text

question = st.text_input("질문을 입력하세요")

if st.button("질문하기"):
    if "api_key" not in st.session_state:
        st.error("API Key를 입력하세요.")
    else:
        answer = ask_gpt(question, st.session_state["api_key"])
        st.write(answer)
