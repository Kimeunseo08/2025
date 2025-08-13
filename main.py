import streamlit as st

# CSS로 카드 스타일 정의
st.markdown("""
<style>
.card {
    background-color: #e6f2ff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
.title {
    color: #004d99;
    font-weight: bold;
    font-size: 24px;
}
.sub-title {
    color: #007acc;
    font-weight: 600;
    margin-bottom: 10px;
}
.highlight {
    background-color: #ccf2ff;
    padding: 10px;
    border-radius: 8px;
    font-weight: 600;
    margin-top: 10px;
}
.warning {
    color: red;
    font-weight: bold;
    font-size: 18px;
    background-color: #ffe6e6;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# 데이터
drug_data = {
    "두통": {
        "질병": "긴장성 두통",
        "약물": "아세트아미노펜",
        "구입경로": "일반의약품 (약국에서 구매 가능)",
        "체질주의": "간 질환 환자는 주의 필요",
        "복용법": "4~6시간 간격으로 복용",
        "이미지": "https://upload.wikimedia.org/wikipedia/commons/3/3b/Paracetamol_200mg_tablets.jpg"
    },
    "기침": {
        "질병": "감기",
        "약물": "덱스트로메토르판",
        "구입경로": "일반의약품 (약국에서 구매 가능)",
        "체질주의": "천식 환자 주의",
        "복용법": "하루 3회 복용",
        "이미지": "https://upload.wikimedia.org/wikipedia/commons/0/0f/Dextromethorphan.png"
    },
    "열": {
        "질병": "감염성 질환",
        "약물": "이부프로펜",
        "구입경로": "일반의약품 (약국에서 구매 가능)",
        "체질주의": "위장 장애 환자 주의",
        "복용법": "식후 복용",
        "이미지": "https://upload.wikimedia.org/wikipedia/commons/8/88/Ibuprofen_200mg_tablets.jpg"
    },
    "목 통증": {
        "질병": "편도염",
        "약물": "아목시실린",
        "구입경로": "병원 처방 필요",
        "체질주의": "페니실린 알레르기 환자 주의",
        "복용법": "하루 3회 7일간 복용",
        "이미지": "https://upload.wikimedia.org/wikipedia/commons/e/e9/Amoxicillin_capsules.jpg"
    }
}

st.title("💊 증상 기반 약 추천 & 구입 경로 안내")
st.markdown('<div class="warning">⚠️ 참고용 정보입니다. 정확한 진단과 처방은 반드시 의료 전문가 상담이 필요합니다.</div>', unsafe_allow_html=True)

symptom = st.text_input("🔎 증상을 입력하세요 (예: 두통, 기침, 열, 목 통증)")

if st.button("분석하기"):
    matched = False
    for key in drug_data.keys():
        if key in symptom:
            info = drug_data[key]
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f'<div class="title">🏥 예상 질병: {info["질병"]}</div>', unsafe_allow_html=True)
            st.image(info["이미지"], width=150)
            st.markdown(f'<div class="sub-title">💊 추천 약물: {info["약물"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="highlight">🛒 구입 경로: {info["구입경로"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="highlight">⚠️ 체질/건강 상태 주의: {info["체질주의"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="highlight">📋 복용법: {info["복용법"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            matched = True

    if not matched:
        st.warning("❗ 해당 증상에 대한 정보가 없습니다. 의료 전문가 상담을 권장합니다.")
