import streamlit as st

# CSS 스타일 (무채색 위주, 심플하고 세련되게, 제목 글씨 잘림 방지 포함)
st.markdown("""
<style>
/* 전체 배경 및 패딩 */
body, .block-container {
    background-color: #f9f9f9;
    padding: 1.5rem 3rem 1.5rem 3rem;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

/* 제목 스타일 - 글씨 안 잘리도록 */
h1 {
    color: #222222;
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 1.5rem;
    user-select: none;
    word-break: keep-all;
    white-space: nowrap;
    overflow-wrap: normal;
}

/* 경고박스 */
.warning {
    background: #e0e0e0;
    border-left: 6px solid #555555;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    font-size: 1.15rem;
    font-weight: 600;
    color: #444444;
    margin-bottom: 1.8rem;
    user-select: none;
}

/* 카드 컨테이너 */
.card {
    background: #ffffff;
    border-radius: 14px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.07);
    padding: 24px 28px;
    margin-bottom: 28px;
    color: #333333;
    user-select: none;
    transition: transform 0.15s ease-in-out;
}
.card:hover {
    transform: translateY(-4px);
}

/* 카드 제목 */
.card-title {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 16px;
    border-bottom: 2px solid #888888;
    padding-bottom: 8px;
    user-select: none;
}

/* 약 사진 */
.med-img {
    border-radius: 10px;
    box-shadow: 0 6px 14px rgba(0,0,0,0.05);
    margin-bottom: 18px;
    user-select: none;
}

/* 하이라이트 박스 */
.highlight {
    background: #f0f0f0;
    border-radius: 12px;
    padding: 12px 18px;
    margin: 10px 0;
    font-weight: 600;
    font-size: 1.05rem;
    color: #555555;
    user-select: none;
    box-shadow: inset 0 0 8px #d0d0d0;
}

/* 입력창 */
[data-baseweb="input"] > div > input {
    font-size: 1.3rem !important;
    padding: 14px !important;
    border-radius: 12px !important;
    border: 1.5px solid #bbbbbb !important;
    transition: border-color 0.3s ease;
    color: #222222 !important;
    background-color: #fafafa !important;
}
[data-baseweb="input"] > div > input:focus {
    border-color: #777777 !important;
    outline: none !important;
}

/* 버튼 */
.stButton>button {
    background-color: #555555;
    color: white;
    font-weight: 700;
    font-size: 1.25rem;
    padding: 14px 0;
    border-radius: 14px;
    width: 100%;
    transition: background-color 0.3s ease;
    user-select: none;
    box-shadow: 0 3px 12px rgba(85,85,85,0.4);
}
.stButton>button:hover {
    background-color: #333333;
    cursor: pointer;
}

/* 경고 문구 텍스트 */
.stWarning>div {
    font-size: 1.15rem;
    font-weight: 600;
    color: #666666;
    user-select: none;
}
</style>
""", unsafe_allow_html=True)

# 데이터 (무채색과 잘 어울리게 이모지 없이 심플하게)
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

# 제목
st.markdown("<h1>증상 기반 약 추천 & 구입 경로 안내</h1>", unsafe_allow_html=True)

# 경고 박스
st.markdown('<div class="warning">참고용 정보입니다. 정확한 진단과 처방은 반드시 의료 전문가 상담이 필요합니다.</div>', unsafe_allow_html=True)

# 입력
symptom = st.text_input("증상을 입력하세요 (예: 두통, 기침, 열, 목 통증)")

if st.button("분석하기"):
    matched = False
    for key in drug_data.keys():
        if key in symptom:
            info = drug_data[key]
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f'<div class="card-title">예상 질병: {info["질병"]}</div>', unsafe_allow_html=True)
            st.image(info["이미지"], width=180, output_format="auto", caption=info["약물"], use_column_width=False)
            st.markdown(f'<div class="highlight">추천 약물: {info["약물"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="highlight">구입 경로: {info["구입경로"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="highlight">체질/건강 상태 주의: {info["체질주의"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="highlight">복용법: {info["복용법"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            matched = True

    if not matched:
        st.warning("해당 증상에 대한 정보가 없습니다. 의료 전문가 상담을 권장합니다.")

