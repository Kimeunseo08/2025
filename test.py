# app.py

import streamlit as st

# -------------------------------
# 데이터베이스 (증상-질병-약품 매핑)
# -------------------------------
medicine_db = {
    "두통": {
        "disease": "긴장성 두통, 편두통",
        "medicine": "타이레놀, 아스피린",
        "caution": "간 질환 환자 주의, 아스피린은 위장 장애 유발 가능",
        "otc": True,
    },
    "발열": {
        "disease": "감기, 독감",
        "medicine": "타이레놀, 이부프로펜",
        "caution": "간, 신장 질환 환자 주의",
        "otc": True,
    },
    "기침": {
        "disease": "기관지염, 감기",
        "medicine": "덱스트로메토르판, 메틸에페드린",
        "caution": "고혈압 환자 주의",
        "otc": True,
    },
    "콧물": {
        "disease": "알레르기성 비염, 감기",
        "medicine": "클로르페니라민, 로라타딘",
        "caution": "졸음 유발 가능",
        "otc": True,
    },
    "복통": {
        "disease": "소화불량, 과민성 대장증후군",
        "medicine": "부스코판, 위장약",
        "caution": "만성 질환자는 의사 상담 필요",
        "otc": True,
    },
    "피로": {
        "disease": "과로, 스트레스",
        "medicine": "비타민B 복합제, 영양제",
        "caution": "지속될 경우 진료 필요",
        "otc": True,
    },
    "불면": {
        "disease": "스트레스, 불안장애",
        "medicine": "멜라토닌 (건강기능식품), 수면유도제",
        "caution": "의존성 주의, 장기 복용 금지",
        "otc": False,
    },
}


# -------------------------------
# Streamlit 앱 UI
# -------------------------------
def main():
    st.set_page_config(
        page_title="스마트 약 추천 앱",
        page_icon="💊",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    # 앱 제목
    st.title("💊 스마트 약 추천 앱")
    st.write("👉 증상과 나이를 입력하면 적절한 **질병·약·주의사항**을 알려드려요.")

    # 나이 입력
    age = st.number_input("나이를 입력하세요", min_value=1, max_value=120, value=20)

    # 증상 다중 선택
    symptoms = st.multiselect("증상을 선택하세요", list(medicine_db.keys()))

    # 결과 버튼
    if st.button("🔍 추천 결과 보기"):
        if not symptoms:
            st.warning("증상을 최소 1개 이상 선택해주세요.")
        else:
            st.subheader("📋 진단 결과")
            for symptom in symptoms:
                data = medicine_db[symptom]
                st.markdown(f"### 🩺 증상: **{symptom}**")
                st.write(f"• 관련 질환: {data['disease']}")
                st.write(f"• 추천 약품: {data['medicine']}")
                st.write(f"• 주의 사항: ⚠️ {data['caution']}")
                if data["otc"]:
                    st.success("구입 가능: 일반 의약품 (약국에서 구매 가능)")
                else:
                    st.error("⚕️ 처방전 필요")

            st.info(f"👤 입력하신 나이: {age}세")


if __name__ == "__main__":
    main()
