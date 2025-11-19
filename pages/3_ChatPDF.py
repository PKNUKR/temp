from utils.pdf_loader import load_pdf_text
from utils.vector_store import VectorStore
from utils.openai_client import get_client
import streamlit as st

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

    # 텍스트를 chunk로 분할
    chunks = [text[i:i+800] for i in range(0, len(text), 800)]

    client = get_client(api_key)

    for chunk in chunks:
        emb = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        ).data[0].embedding
        st.session_state.vector.add(chunk, emb)

    st.info(f"총 {len(chunks)}개의 chunk 저장 완료!")

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
