import streamlit as st
import pandas as pd

# ==============================
# 앱 기본 설정
# ==============================
st.set_page_config(
    page_title="스마트 약 추천 앱",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# 스타일 (다크 테마 적용)
# ==============================
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: #e0e0e0;
    }
    .stTextInput>div>div>input {
        background-color: #1e1e1e;
        color: #fff;
    }
    .stSelectbox>div>div>select {
        background-color: #1e1e1e;
        color: #fff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================
# 데이터베이스 (증상-약 추천 매핑)
# ==============================
drug_db = {
    "두통": {
        "추천약": "타이레놀",
        "질병 가능성": "편두통, 긴장성 두통",
        "주의 체질": "간 질환자",
        "주의사항": "과다 복용 시 간 손상 가능",
        "구매 여부": "일반의약품 (처방전 불필요)"
    },
    "발열": {
        "추천약": "부루펜",
        "질병 가능성": "감기, 독감",
        "주의 체질": "위장 장애 환자",
        "주의사항": "속쓰림, 위출혈 주의",
        "구매 여부": "일반의약품 (처방전 불필요)"
    },
    "기침": {
        "추천약": "코푸시럽",
        "질병 가능성": "감기, 기관지염",
        "주의 체질": "천식 환자",
        "주의사항": "졸음 유발 가능성",
        "구매 여부": "일반의약품 (처방전 불필요)"
    },
    "복통": {
        "추천약": "겔포스",
        "질병 가능성": "소화불량, 위염",
        "주의 체질": "만성 신부전 환자",
        "주의사항": "장기간 복용 시 전해질 불균형",
        "구매 여부": "일반의약품 (처방전 불필요)"
    },
    "알레르기": {
        "추천약": "지르텍",
        "질병 가능성": "알레르기 비염, 두드러기",
        "주의 체질": "신장 질환자",
        "주의사항": "졸음 유발 가능",
        "구매 여부": "일반의약품 (처방전 불필요)"
    }
}

# ==============================
# 함수: 증상 검색
# ==============================
def get_recommendation(symptom):
    if symptom in drug_db:
        return drug_db[symptom]
    else:
        return None

# ==============================
# UI 구성
# ==============================
st.title("💊 스마트 약 추천 앱")
st.write("증상을 입력하면 알맞은 약, 질병 가능성, 주의사항을 알려드립니다.")

# 증상 입력
symptom = st.text_input("증상을 입력하세요 (예: 두통, 발열, 기침, 복통, 알레르기)")

if st.button("추천받기"):
    result = get_recommendation(symptom)
    if result:
        st.subheader("🔎 추천 결과")
        st.markdown(f"**추천 약**: {result['추천약']}")
        st.markdown(f"**관련 질병 가능성**: {result['질병 가능성']}")
        st.markdown(f"**주의 체질**: {result['주의 체질']}")
        st.markdown(f"**주의사항**: {result['주의사항']}")
        st.markdown(f"**구매 여부**: {result['구매 여부']}")
    else:
        st.error("❌ 해당 증상에 대한 데이터가 없습니다. 다른 증상을 입력해주세요.")

# ==============================
# 추가: 데이터 테이블 시각화
# ==============================
st.subheader("📋 전체 약 정보 데이터베이스")
df = pd.DataFrame(drug_db).T
st.dataframe(df, use_container_width=True)
