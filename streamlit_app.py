import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="Fashion Chatbot", page_icon="👗")

# 제목 및 설명
st.title("👗 패션 챗봇")
st.write(
    "오늘의 코디, 스타일 추천, 패션 아이템 매칭 등을 도와주는 AI 패션 챗봇입니다. "
    "원하는 스타일이나 상황을 자유롭게 입력해보세요!"
)

# OpenAI API Key 입력
openai_api_key = st.text_input("OpenAI API 키 입력", type="password")

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요. 🗝️")
else:

    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 채팅 기록 저장
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "너는 전문 패션 스타일리스트 AI이다. "
                    "사용자의 분위기, 계절, 상황, 스타일 취향에 맞춰 "
                    "옷, 신발, 액세서리, 컬러 조합 등을 추천해준다. "
                    "답변은 친근하고 트렌디한 말투로 한국어로 답변한다."
                )
            }
        ]

    # 이전 메시지 출력
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 채팅 입력창
    if prompt := st.chat_input("예: 봄 데이트룩 추천해줘 🌸"):

        # 사용자 메시지 저장
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        # 사용자 메시지 출력
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI 응답 생성
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True,
        )

        # 응답 출력
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        # 응답 저장
        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
