import streamlit as st
import pandas as pd

# CSV 데이터 불러오기
df = pd.read_csv("drug_data.csv")

st.title("💊 증상 기반 약 추천 & 구입 경로 안내")
st.markdown("⚠️ 참고용 정보이며, 정확한 진단은 반드시 의료 전문가 상담 후 진행하세요.")

# 증상 입력
symptom = st.text_input("증상을 입력하세요 (예: 두통, 기침, 열)")

if st.button("분석하기"):
    results = df[df["증상"].str.contains(symptom)]
    
    if len(results) > 0:
        for _, row in results.iterrows():
            st.subheader(f"예상 질병: {row['질병']}")
            st.write(f"**추천 약물:** {row['약물']}")
            st.write(f"**구입 경로:** {row['구입경로']}")
            st.write(f"**체질/건강 상태 주의:** {row['체질주의']}")
            st.write(f"**복용법:** {row['복용법']}")
            st.markdown("---")
    else:
        st.warning("데이터에 없는 증상입니다. 의료 전문가 상담을 권장합니다.")
