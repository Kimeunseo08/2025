import streamlit as st
import pandas as pd
import os

# ==============================
# 📌 기본 설정
# ==============================
st.set_page_config(page_title="증상 기록 앱", layout="wide", page_icon="💊")

# ==============================
# 📌 데이터 파일 설정
# ==============================
DATA_FILE = "symptom_data.csv"

# ==============================
# 📌 데이터 로드 함수
# ==============================
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["이름", "나이", "증상"])

# ==============================
# 📌 데이터 저장 함수
# ==============================
def save_data(new_entry):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# ==============================
# 📌 UI 레이아웃
# ==============================
st.title("💊 개인 증상 기록 및 분석")
st.markdown("#### 여러 증상을 선택하고 저장할 수 있습니다.")

# 입력 폼
with st.form("symptom_form", clear_on_submit=True):
    st.subheader("📝 증상 입력")

    name = st.text_input("이름을 입력하세요")
    age = st.number_input("나이", min_value=0, max_value=120, step=1)

    symptoms = st.multiselect(
        "현재 겪고 있는 증상을 선택하세요",
        ["두통", "발열", "기침", "피로감", "복통", "어지럼증", "근육통", "기타"],
    )

    submitted = st.form_submit_button("저장하기")

    if submitted:
        if name and symptoms:
            save_data({"이름": name, "나이": age, "증상": ", ".join(symptoms)})
            st.success("✅ 증상이 저장되었습니다!")
        else:
            st.warning("⚠️ 이름과 증상을 입력해야 합니다.")

# ==============================
# 📌 저장된 데이터 보기
# ==============================
st.subheader("📂 저장된 증상 기록")
data = load_data()

if not data.empty:
    st.dataframe(data, use_container_width=True)

    # ==============================
    # 📊 데이터 시각화
    # ==============================
    st.subheader("📊 증상 분포 시각화")
    symptom_counts = data["증상"].str.split(", ").explode().value_counts()
    st.bar_chart(symptom_counts)

    st.subheader("👥 나이 분포")
    st.line_chart(data["나이"].value_counts().sort_index())

else:
    st.info("아직 저장된 데이터가 없습니다.")

# ==============================
# 📌 사용자 친화적 기능
# ==============================
with st.expander("⚙️ 데이터 관리"):
    if st.button("📁 데이터 파일 다운로드"):
        st.download_button(
            label="데이터 다운로드 (CSV)",
            data=open(DATA_FILE, "rb").read(),
            file_name="symptom_data.csv",
            mime="text/csv"
        )

    if st.button("🗑 데이터 전체 삭제"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
            st.warning("모든 데이터가 삭제되었습니다.")
