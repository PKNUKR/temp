import streamlit as st
import base64
from openai import OpenAI

st.title("GPT-5-mini Chat + Image Generator")

# 1) API Key 입력
api_key = st.text_input("OpenAI API Key 입력", type="password")

if api_key:
    client = OpenAI(api_key=api_key)

    st.subheader("💬 GPT-5-mini 답변 기능")

    # 2) 사용자 질문 입력
    user_question = st.text_input("질문을 입력하세요")

    if st.button("GPT 응답 생성"):
        if user_question.strip():
            response = client.chat.completions.create(
                model="gpt-5-mini",
                messages=[{"role": "user", "content": user_question}]
            )
            st.write("### 답변:")
            st.write(response.choices[0].message.content)
        else:
            st.warning("질문을 입력해주세요!")

    st.subheader("🖼️ 이미지 생성 (gpt-image-1-mini)")

    # 3) 이미지 생성용 프롬프트 입력
    prompt = st.text_input("이미지 생성 프롬프트 입력")

    if st.button("이미지 생성"):
        if prompt.strip():
            img = client.images.generate(
                model="gpt-image-1-mini",
                prompt=prompt
            )

            # base64 → bytes 디코딩
            image_bytes = base64.b64decode(img.data[0].b64_json)

            # 이미지 출력
            st.image(image_bytes)
        else:
            st.warning("이미지 프롬프트를 입력해주세요!")
else:
    st.info("먼저 API Key를 입력하세요.")
