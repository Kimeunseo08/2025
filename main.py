import streamlit as st

# CSS 스타일 (꽉 차고 화려하게, 이모지 잔뜩, 귀엽게)
st.markdown("""
<style>
/* 전체 배경 */
body, .block-container {
    background: linear-gradient(135deg, #c1f0f6, #ffe1f5);
    padding: 1rem 2rem 0.5rem 2rem;
}

/* 제목 */
h1 {
    font-family: 'Comic Sans MS', cursive, sans-serif;
    color: #ff4081;
    font-size: 3rem;
    text-align: center;
    margin-bottom: 0.3rem;
    user-select: none;
    text-shadow: 2px 2px 5px #ff80ab;
}

/* 경고박스 */
.warning {
    background: #ffdde1;
    border: 3px dashed #ff4081;
    border-radius: 20px;
    padding: 1rem 1.5rem;
    font-size: 1.3rem;
    font-weight: 700;
    color: #b0003a;
    text-align: center;
    margin-bottom: 1rem;
    user-select: none;
}

/* 카드 컨테이너 */
.card {
    background: #fff0f6;
    border-radius: 25px;
    box-shadow: 0 8px 25px rgba(255, 64, 129, 0.3);
    padding: 20px 25px;
    margin-bottom: 20px;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    color: #880e4f;
    user-select: none;
}

/* 카드 제목 */
.card-title {
    font-size: 2rem;
    font-weight: 800;
    margin-bottom: 12px;
    color: #ff4081;
    user-select: none;
}

/* 약 사진 */
.med-img {
    border-radius: 15px;
    box-shadow: 0 6px 15px rgba(255, 64, 129, 0.4);
    margin-bottom: 15px;
    user-select: none;
}

/* 하이라이트 박스 */
.highlight {
    background: #ffd3e0;
    border-radius: 15px;
    padding: 10px 15px;
    margin: 8px 0;
    font-weight: 700;
    font-size: 1.1rem;
    color: #a00037;
    user-select: none;
}

/* 입력창 */
[data-baseweb="input"] > div > input {
    font-size: 1.3rem !important;
    padding: 10px !important;
}

/* 버튼 */
.stButton>button {
    background: linear-gradient(90deg, #ff4081, #f50057);
    color: white;
    font-weight: 700;
    font-size: 1.3rem;
    padding: 12px 0;
    border-radius: 15px;
    width: 100%;
    transition: background 0.3s ease;
    user-select: none;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #f50057, #ff4081);
    cursor: pointer;
}

/* 경고 문구 텍스트 */
.stWarning>div {
    font-size: 1.2rem;
    font-weight: 700;
    color: #b0003a;
    user-select: none;
}
</style>
""", unsafe_allow_html=True)

# 데이터 (이모지 잔뜩 넣어서 귀엽게)
drug_data = {
    "두통": {
        "질병": "🧠 긴장성 두통",
        "약물": "💊 아세트아미노펜",
        "구입경로": "🏪 일반의약품 (약국에서 구매 가능)",
        "체질주의": "⚠️ 간 질환 환자는 주의 필요",
        "복용법": "⏰ 4~6시간 간격으로 복용",
        "이미지": "https://upload.wikimedia.org/wikipedia/commons/3/3b/Paracetamol_200mg_tablets.jpg"
    },
    "기침": {
        "질병": "🤧 감기",
        "약물": "🍬 덱스트로메토르판",
        "구입경로": "🏪 일반의약품 (약국에서 구매 가능)",
        "체질주의": "⚠️ 천식 환자 주의",
        "복용법": "⏰ 하루 3회 복용",
        "이미지": "https://upload.wikimedia.org/wikipedia/commons/0/0f/Dextromethorphan.png"
    },
    "열": {
        "질병": "🌡️ 감염성 질환",
        "약물": "💊 이부프로펜",
        "구입경로": "🏪 일반의약품 (약국에서 구매 가능)",
        "체질주의": "⚠️ 위장 장애 환자 주의",
        "복용법": "🍽️ 식후 복용",
        "이미지": "https://upload.wikimedia.org/wikipedia/commons/8/88/Ibuprofen_200mg_tablets.jpg"
    },
    "목 통증": {
        "질병": "😷 편도염",
        "약물": "💉 아목시실린",
        "구입경로": "🏥 병원 처방 필요",
        "체질주의": "⚠️ 페니실린 알레르기 환자 주의",
        "복용법": "⏰ 하루 3회 7일간 복용",
        "이미지": "https://upload.wikimedia.org/wikipedia/commons/e/e9/Amoxicillin_capsules.jpg"
    }
}

# 제목
st.markdown("<h1>💖 귀여운 증상별 약 추천 웹앱 💖</h1>", unsafe_allow_html=True)

# 경고 박스
st.markdown('<div class="warning">⚠️ 이 앱은 참고용입니다! <br>정확한 진단과 처방은 꼭 의료 전문가와 상담하세요! 🙏</div>', unsafe_allow_html=True)

# 입력
symptom = st.text_input("🔍 증상을 입력해 주세요 (예: 두통, 기침, 열, 목 통증)")

if st.button("✨ 분석하기 ✨"):
    matched = False
    for key in drug_data.keys():
        if key in symptom:
            info = drug_data[key]
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f'<div class="card-title">🏥 예상 질병: {info["질병"]}</div>', unsafe_allow_html=True)
            st.image(info["이미지"], width=180, output_format="auto", caption=info["약물"])
            st.markdown(f'<div class="highlight">💊 추천 약물: {info["약물"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="highlight">🛒 구입 경로: {info["구입경로"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="highlight">⚠️ 체질/건강 상태 주의: {info["체질주의"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="highlight">📋 복용법: {info["복용법"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            matched = True
    if not matched:
        st.warning("❗ 해당 증상에 대한 정보가 없어요! 꼭 의료 전문가와 상담해 주세요! 💕")
