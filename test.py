import streamlit as st
import pandas as pd

# ============================================================
# 약 추천 시스템 Streamlit App
# - 증상 입력 시 약품, 관련 질병, 주의사항, 구입 가능 여부를 안내
# - 직관적/모던 디자인, 모듈화 주석, 사용자 친화적 인터페이스
# ============================================================

# ---------------------- 데이터 정의 ---------------------- #
medications = {
    "두통": {
        "약": "타이레놀",
        "질병": "긴장성 두통, 편두통",
        "주의": "간 질환 환자는 사용 주의",
        "구입": "처방전 없이 약국에서 구입 가능"
    },
    "기침": {
        "약": "코데인 시럽",
        "질병": "감기, 기관지염",
        "주의": "호흡 억제 환자 주의",
        "구입": "처방전 필요"
    },
    "소화불량": {
        "약": "훼스탈",
        "질병": "소화불량, 과식",
        "주의": "췌장 질환 환자 주의",
        "구입": "처방전 없이 약국에서 구입 가능"
    },
    "알레르기": {
        "약": "지르텍",
        "질병": "알레르기 비염, 피부 알레르기",
        "주의": "신장 질환 환자 주의",
        "구입": "처방전 없이 약국에서 구입 가능"
    }
}

# ---------------------- 함수 정의 ---------------------- #
def recommend_medication(symptom):
    """사용자가 입력한 증상에 맞는 약품 정보를 반환"""
    return medications.get(symptom, None)

# ---------------------- 앱 UI ---------------------- #
st.set_page_config(page_title="약 추천 시스템", page_icon="💊", layout="wide")
st.title("💊 증상 기반 약 추천 시스템")
st.write("원하는 증상을 입력하면 관련 약품, 질병 정보, 주의사항, 구입 가능 여부를 알려드립니다.")

# 사용자 입력
symptom = st.text_input("증상을 입력하세요 (예: 두통, 기침, 소화불량, 알레르기)")

# 버튼 클릭 시 추천 실행
if st.button("🔍 약 추천 받기"):
    if symptom:
        result = recommend_medication(symptom)
        if result:
            st.success(f"**추천 약품: {result['약']}**")
            st.info(f"관련 질병: {result['질병']}")
            st.warning(f"주의사항: {result['주의']}")
            st.write(f"💡 구입 가능 여부: {result['구입']}")
        else:
            st.error("해당 증상에 대한 정보가 없습니다. 다시 입력해 주세요.")
    else:
        st.error("증상을 입력해 주세요.")

# ---------------------- 데이터 시각화 ---------------------- #
st.subheader("📊 지원되는 증상 및 약품 데이터")
data = pd.DataFrame(medications).T  # 보기 좋게 전치
st.dataframe(data, use_container_width=True)

# ---------------------- 사용자 저장 기능 ---------------------- #
with st.expander("💾 내가 조회한 기록 저장"):
    filename = st.text_input("저장할 파일명 (예: my_data.csv)")
    if st.button("저장하기"):
        if filename:
            data.to_csv(filename, index=True)
            st.success(f"데이터가 '{filename}' 파일로 저장되었습니다.")
        else:
            st.error("파일명을 입력해 주세요.")

