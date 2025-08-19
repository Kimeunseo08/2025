import streamlit as st
import pandas as pd

# =====================
# 약 데이터 정의 (DB 대체용)
# =====================
MEDICINE_DB = {
    "두통": {
        "약": ["타이레놀", "게보린"],
        "질병": ["편두통", "긴장성 두통"],
        "주의 체질": "간 질환 환자는 복용 전 의사 상담 필요",
        "처방전": False
    },
    "발열": {
        "약": ["타이레놀", "이부프로펜"],
        "질병": ["감기", "인플루엔자"],
        "주의 체질": "위장 장애 환자 주의",
        "처방전": False
    },
    "기침": {
        "약": ["코데인 시럽", "덱스트로메토르판"],
        "질병": ["급성 기관지염", "감기"],
        "주의 체질": "호흡기 질환자 주의",
        "처방전": True
    }
}

# =====================
# Streamlit 앱 구성
# =====================

def main():
    # ----- 페이지 설정 -----
    st.set_page_config(page_title="약 추천 도우미", page_icon="💊", layout="wide")

    # ----- 헤더 -----
    st.title("💊 증상 기반 약 추천 도우미")
    st.markdown("""
    ### 🧾 사용 방법
    1. 증상을 입력하면 관련 **약**, **가능한 질병**, **체질 주의사항**을 보여드립니다.  
    2. 약이 **처방전 필요 여부**도 함께 확인할 수 있습니다.
    """)

    # ----- 사이드바 -----
    st.sidebar.header("🔍 검색 옵션")
    symptom = st.sidebar.selectbox("증상을 선택하세요:", list(MEDICINE_DB.keys()))

    # ----- 메인 결과 -----
    if symptom:
        st.subheader(f"🩺 '{symptom}' 관련 정보")

        data = MEDICINE_DB[symptom]

        # 카드 형태 UI
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label="추천 약", value=", ".join(data["약"]))

        with col2:
            st.metric(label="관련 질병", value=", ".join(data["질병"]))

        with col3:
            st.metric(label="처방전 필요", value="✅ 필요" if data["처방전"] else "❌ 불필요")

        # 주의사항 박스
        st.warning(f"⚠️ 주의 체질: {data['주의 체질']}")

        # 데이터프레임 시각화
        df = pd.DataFrame({
            "약": data["약"],
            "관련 질병": ", ".join(data["질병"]),
            "처방전 필요 여부": ["예" if data["처방전"] else "아니오"] * len(data["약"])
        })

        st.dataframe(df, use_container_width=True)

        # 인터랙션: 유용성 피드백
        feedback = st.radio("이 정보가 도움이 되었나요?", ("네", "아니오"))
        if feedback == "네":
            st.success("😊 도움이 되었다니 다행입니다!")
        else:
            st.info("💡 더 많은 데이터를 추가하겠습니다.")

    # ----- 푸터 -----
    st.markdown("---")
    st.caption("※ 본 서비스는 참고용이며, 실제 진단 및 처방은 의사 상담이 필요합니다.")


# =====================
# 실행 시작
# =====================
if __name__ == "__main__":
    main()
