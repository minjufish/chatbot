import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(
    page_title="Sanrio Encyclopedia Chatbot",
    page_icon="🎀"
)

# 제목
st.title("🎀 산리오 도감 챗봇")

# 설명 + 공식 사이트 링크
st.write(
    "산리오코리아 공식 사이트 기반으로 캐릭터 정보를 설명해주는 AI 도감 챗봇입니다 💖"
)

st.link_button(
    "🌐 산리오코리아 공식 사이트 바로가기",
    "https://sanriokorea.co.kr/"
)

# API KEY 입력
openai_api_key = st.text_input(
    "OpenAI API 키 입력",
    type="password"
)

if not openai_api_key:
    st.info(
        "계속하려면 OpenAI API 키를 입력해주세요 🗝️"
    )

else:

    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 시스템 프롬프트
    SYSTEM_PROMPT = """
    너는 산리오 공식 캐릭터 도감 AI이다.

    반드시 산리오코리아 공식 사이트의 캐릭터 설정과 분위기를 기준으로 설명해야 한다.
    추측하거나 존재하지 않는 설정을 만들지 않는다.

    답변 스타일:
    - 귀엽고 친근한 한국어 말투
    - 이모지 사용
    - 짧고 읽기 쉽게 설명
    - 캐릭터 소개 + 특징 + 성격 + 좋아하는 것 설명

    사용자가 캐릭터를 물어보면
    공식 캐릭터 도감처럼 소개해줘.
    """

    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

    # 이전 메시지 출력
    for message in st.session_state.messages:

        if message["role"] != "system":

            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 인기 캐릭터 버튼
    st.subheader("💖 인기 캐릭터")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("☁️ 시나모롤"):
            st.session_state.quick_prompt = "시나모롤 소개해줘"

    with col2:
        if st.button("🖤 쿠로미"):
            st.session_state.quick_prompt = "쿠로미 소개해줘"

    with col3:
        if st.button("🎀 마이멜로디"):
            st.session_state.quick_prompt = "마이멜로디 소개해줘"

    with col4:
        if st.button("🐱 헬로키티"):
            st.session_state.quick_prompt = "헬로키티 소개해줘"

    # 채팅 입력
    user_input = st.chat_input(
        "예: 포차코 설명해줘 🐶"
    )

    # 버튼 클릭 처리
    if "quick_prompt" in st.session_state:

        prompt = st.session_state.quick_prompt
        del st.session_state.quick_prompt

    else:
        prompt = user_input

    # 메시지 처리
    if prompt:

        # 사용자 메시지 저장
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        # 사용자 메시지 출력
        with st.chat_message("user"):
            st.markdown(prompt)

        # GPT 응답 생성
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            stream=True,
        )

        # 응답 출력
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        # 응답 저장
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )
