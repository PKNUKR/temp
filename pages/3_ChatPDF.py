import streamlit as st
from utils.pdf_loader import load_pdf_text
from utils.vector_store import VectorStore
from utils.openai_client import get_client

st.title("ChatPDF 페이지")

api_key = st.session_state.get("api_key")
if not api_key:
    st.warning("먼저 홈에서 API Key 입력하세요.")

if "vector" not in st.session_state:
    st.session_state.vector = VectorStore()

uploaded = st.file_uploader("PDF 업로드", type=["pdf"])

if st.button("Clear"):
    st.session_state.vector = VectorStore()
    st.success("벡터 스토어 초기화 완료!")

if uploaded:
    text = load_pdf_text(uploaded)
    client = get_client(api_key)

    embedding = client.embeddings.create(
        model="text-embedding-3-large",
        input=text
    ).data[0].embedding

    st.session_state.vector.add(text, embedding)
    st.info("PDF 내용이 저장되었습니다.")

query = st.text_input("질문 입력")

if st.button("질문하기") and query:
    client = get_client(api_key)
    docs = st.session_state.vector.search(query)

    prompt = f"""
다음 문서 내용을 기반으로 질문에 답하세요.

[문서 내용]
{docs}

사용자 질문: {query}
"""

    answer = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    ).output_text

    st.write(answer)
