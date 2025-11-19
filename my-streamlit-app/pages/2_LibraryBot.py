import streamlit as st
from utils.openai_client import get_client

st.title("국립부경대학교 도서관 챗봇")

api_key = st.session_state.get("api_key")
if not api_key:
    st.warning("먼저 홈에서 API Key 입력하세요.")

with open("data/library_rules.txt", "r", encoding="utf-8") as f:
    rules = f.read()

question = st.text_input("도서관 관련 질문을 입력하세요")

if st.button("질문하기") and question:
    client = get_client(api_key)
    prompt = f"""
당신은 국립부경대학교 도서관 규정 기반 챗봇입니다.
아래 규정을 참고해 정확히 답변하세요.

[규정]
{rules}

사용자 질문: {question}
"""

    answer = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    ).output_text

    st.write(answer)
