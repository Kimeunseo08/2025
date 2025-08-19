import streamlit as st
import pandas as pd

# ==============================
# 데이터 준비
# ==============================
def load_data():
    """증상, 약, 질병, 주의사항, 판매 여부, 처방전 여부 데이터"""
    data = [
        {
            "symptom": "두통",
            "disease": "긴장성 두통, 편두통",
            "medicine": "타이레놀",
            "caution": "간 질환이 있는 경우 과다 복용 주의",
            "availability": "일반 약국에서 구입 가능",
            "prescription": "불필요"
        },
        {
            "symptom": "소화불량",
            "disease": "소화불량, 과민성 대장 증후군",
            "medicine": "훼스탈",
            "caution": "췌장 질환 환자 주의",
            "availability": "일반 약국에서 구입 가능",
            "prescription": "불필요"
        },
        {
            "symptom": "알레르기",
            "disease": "알레르기 비염, 피부 발진",
            "medicine": "지르텍",
            "caution": "졸음 유발, 운전 전 복용 주의",
            "availability": "일반 약국에서 구입 가능",
            "prescription": "불필요"
        },
        {
            "symptom": "기침",
            "disease": "감기, 기관지염",
            "medicine": "코푸시럽",
            "caution": "고혈압 환자 주의",
            "availability": "일반 약국에서 구입 가능",
            "prescription": "불필요"
        },
        {
            "symptom": "고열",
            "disease": "인플루엔자, 세균 감염",
            "medicine": "아세트아미노펜",
            "caution": "간 질환 환자 주의",
            "availability": "일반 약국에서 구입 가능",
            "prescription": "불필요"
        },
    ]
    return pd.DataFrame(data)

# ==============================
# 추천 함수
# ==============================
def recommend(symptom, df):
    """증상에 맞는 약 정보 추천"""
    result = df[df["symptom"] == symptom]
    if result.empty:
        return None
    return result.iloc[0]

# ==============================
# UI 구성
# ==============================
def main():
    st.set_page_config(page_title="약 추천 도우미", page_icon="💊", layout="wide")

    st.title("💊 증상 기반 약 추천 도우미")
    st.write("👉 증상을 선택하면 적합한 약, 관련 질병, 주의사항 등을 확인할 수 있습니다.")

    # 데이터 로드
    df = load_data()

    # 증상 선택
    symptom = st.selectbox("증상을 선택하세요", df["symptom"].unique())

    # 추천 결과 가져오기
    result = recommend(symptom, df)

    if result is not None:
        st.subheader(f"🔎 '{symptom}' 관련 정보")
        st.markdown(f"**🦠 관련 질병:** {result['disease']}")
        st.markdown(f"**💊 추천 약:** {result['medicine']}")
        st.markdown(f"**⚠️ 주의사항:** {result['caution']}")
        st.markdown(f"**🏪 구입 여부:** {result['availability']}")
        st.markdown(f"**📜 처방전 필요 여부:** {result['prescription']}")

        # 데이터 시각화 (예시: 약국 구입 가능 여부)
        st.bar_chart(df["availability"].value_counts())

    else:
        st.warning("해당 증상에 대한 데이터가 없습니다.")

if __name__ == "__main__":
    main()
