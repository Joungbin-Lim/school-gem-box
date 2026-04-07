import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="우리 반 보석함", page_icon="💎", layout="centered")
# --- 배경 꾸미기 (CSS) ---
st.markdown(
    """
    <style>
    /* 전체 배경색을 은은한 보석 빛깔 그라데이션으로 변경 */
    .stApp {
        background: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%);
    }

    /* 입력창(카드) 스타일 변경 */
    div[data-testid="stForm"] {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }

    /* 제목 글자 스타일 */
    h1 {
        color: #5a4a75;
        font-family: 'Nanum Gothic', sans-serif;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    /* 버튼 스타일 */
    .stButton>button {
        background-color: #d4af37; /* 금색 느낌 */
        color: white;
        border-radius: 10px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #b8860b;
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. 선생님께서 직접 정해주신 25가지 보석 리스트
GEMS = [
    "다이아몬드", "에메랄드", "사파이어", "루비", "진주",
    "아쿠아마린", "토파즈", "자수정", "터키석", "오팔",
    "로즈쿼츠", "황옥", "문스톤", "가넷", "페리도트",
    "산호", "옥", "수정", "금", "은",
    "핑크다이아몬드", "블루사파이어", "크리스탈", "핑크사파이어", "핑크진주"
]

# 3. 데이터 저장소 초기화
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["날짜", "보석명", "기분", "이유", "메시지"])

# --- 사이드바 메뉴 ---
st.sidebar.title("💎 마음함 메뉴")
mode = st.sidebar.radio("어디로 갈까요?", ["학생용 (내 마음 기록)", "교사용 (선생님 확인)"])

# --- [학생용 모드] ---
if mode == "학생용 (내 마음 기록)":
    st.title("✨ 오늘의 내 마음 기록하기")
    st.info("안녕! 오늘 너의 마음은 어떤 보석처럼 빛나고 있니? 솔직하게 너의 마음을 표현해 줘")

    with st.form("emotion_form", clear_on_submit=True):
        # 보석 선택
        selected_gem = st.selectbox("나의 보석 이름을 골라주세요", ["선택하세요"] + GEMS)

        st.markdown("### 1. 지금 내 기분은 어떤가요?")
        emotion_options = {
            "😭 정말 불쾌해요(힘들어요)": "정말 불쾌해요(힘들어요) 😭",
            "😟 조금 불쾌해요": "조금 불쾌해요 😟",
            "😐 보통이에요": "보통이에요 😐",
            "😊 기분 좋아요": "기분 좋아요 😊",
            "💖 정말 행복해요!": "정말 행복해요! 💖"
        }
        raw_emotion = st.select_slider("슬라이더를 옆으로 밀어보세요", options=list(emotion_options.keys()))
        selected_emotion = emotion_options[raw_emotion]

        st.markdown("### 2. 그런 감정이 드는 이유는 무엇인가요?")
        reason = st.text_input("짧게 적어도 괜찮아요!", placeholder="예) 친구와 사이좋게 놀아서, 선물을 받아서")

        st.markdown("### 3. 선생님께 더 전하고 싶은 말이 있나요?")
        note = st.text_area("비밀글로 전달됩니다.", placeholder="선생님께만 하고 싶은 이야기를 적어주세요.")

        submit_button = st.form_submit_button("내 마음 전송하기")

        if submit_button:
            if selected_gem == "선택하세요":
                st.error("보석 이름을 꼭 선택해야 해요!")
            else:
                new_entry = {
                    "날짜": datetime.now().strftime("%m-%d %H:%M"),
                    "보석명": selected_gem,
                    "기분": selected_emotion,
                    "이유": reason,
                    "메시지": note
                }
                st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_entry])], ignore_index=True)
                st.success(f"{selected_gem}님, 소중한 기록이 완료되었습니다! 오늘도 행복한 하루 보내요.")
                st.balloons()

# --- [교사용 모드] ---
elif mode == "교사용 (선생님 확인)":
    st.title("👩‍🏫 우리 반 보석 관리함")

    # 비밀번호는 0000으로 설정되어 있습니다 (필요시 수정 가능)
    admin_pw = st.sidebar.text_input("관리자 비밀번호를 입력하세요", type="password")

    if admin_pw == "0000":
        if st.session_state.db.empty:
            st.info("아직 도착한 보석들의 마음이 없습니다.")
        else:
            st.subheader("📊 오늘 우리 반 기분 그래프")
            st.bar_chart(st.session_state.db["기분"].value_counts())

            st.subheader("📝 학생별 상세 기록")
            st.dataframe(st.session_state.db, use_container_width=True)

            # 엑셀 저장을 위한 CSV 다운로드
            csv = st.session_state.db.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📁 엑셀 파일로 저장하기",
                data=csv,
                file_name=f"보석함_기록_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

            if st.button("🚨 모든 기록 초기화"):
                st.session_state.db = pd.DataFrame(columns=["날짜", "보석명", "기분", "이유", "메시지"])
                st.rerun()
    else:
        st.warning("비밀번호를 입력하면 기록을 볼 수 있습니다.")