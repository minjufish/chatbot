import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="Sanrio Encyclopedia Chatbot", page_icon="🎀")

# 제목 및 설명
st.title("🎀 산리오 도감 챗봇")
st.write(
    "산리오 캐릭터들의 정보, 성격, 특징, 세계관 등을 알려주는 AI 도감 챗봇입니다! "
    "좋아하는 캐릭터를 입력해보세요 💖"
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
                    "너는 산리오 캐릭터 전문 도감 AI이다. "
                    "사용자가 캐릭터 이름을 입력하면 "
                    "캐릭터의 성격, 특징, 좋아하는 것, 세계관, 친구 관계 등을 "
                    "귀엽고 친근한 말투로 설명해준다. "
                    "답변은 항상 한국어로 하며 이모지를 적절히 사용한다."
                )
            }
        ]

    # 이전 메시지 출력
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 추천 캐릭터 버튼
    st.subheader("💖 인기 캐릭터")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("헬로키티"):
            st.session_state.quick_prompt = "헬로키티 소개해줘"

    with col2:
        if st.button("마이멜로디"):
            st.session_state.quick_prompt = "마이멜로디 소개해줘"

    with col3:
        if st.button("쿠로미"):
            st.session_state.quick_prompt = "쿠로미 소개해줘"

    # 입력 처리
    user_input = st.chat_input("예: 시나모롤 소개해줘 ☁️")

    # 버튼 클릭 시 자동 입력
    if "quick_prompt" in st.session_state:
        prompt = st.session_state.quick_prompt
        del st.session_state.quick_prompt
    else:
        prompt = user_input

    # 사용자가 입력했을 때
    if prompt:

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
