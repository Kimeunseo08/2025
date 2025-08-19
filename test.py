# app.py
# -*- coding: utf-8 -*-
"""
⚕️ 간단 증상 → 의약품 추천 Streamlit 앱 (한국어)
- 사용자 입력(증상/연령/임신/질환/복약중 약 등)에 따라 일반의약품(OTC) 추천
- 의심 질환/주의 체질(상황) 안내, 빨간 깃발(응급/진료 필요) 표시
- "약국에서 구매 가능 / 편의점 소포장 가능 / 처방전 필요" 등 가용성 표기
- ⚠️ 법적/의학적 고지: 참고 정보일 뿐, 진단이 아님. 전문의 상담 권장.

파일 하나로 실행:  
    streamlit run app.py
"""

import streamlit as st
from datetime import datetime
from typing import List, Dict, Any

st.set_page_config(
    page_title="증상 맞춤 약 추천 (비의료 진단 아님)",
    page_icon="💊",
    layout="wide",
)

# ------------------------------
# 스타일 (모던/미니멀)
# ------------------------------
st.markdown(
    """
    <style>
      :root {
        --radius: 16px;
      }
      .app-card {
        border: 1px solid rgba(0,0,0,0.08);
        border-radius: var(--radius);
        padding: 18px 18px 14px 18px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.05);
        background: #ffffff;
      }
      .tag { display:inline-block; padding:4px 10px; border-radius:999px; border:1px solid rgba(0,0,0,0.08); margin-right:8px; font-size:12px; }
      .tag.green { background:#f0fff4; border-color:#a7f3d0; }
      .tag.yellow { background:#fffbeb; border-color:#fde68a; }
      .tag.red { background:#fef2f2; border-color:#fecaca; }
      .pill { display:inline-block; padding:4px 10px; border-radius:999px; background:#f4f4f5; margin:2px; font-size:12px; }
      .muted { color:#6b7280; }
      .small { font-size:13px; }
      .section-title { font-weight:700; font-size:18px; margin-bottom:8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------
# 간단 지식 베이스 (샘플)
# 실제 서비스에서는 약사/의사 검수 및 최신 규정 반영 필요.
# ------------------------------

# 약 가용성 enum 비슷하게
PHARMACY_ONLY = "약국 구매"
CONVENIENCE_MINIPACK = "약국 + 일부 편의점 소포장"
PRESCRIPTION = "처방전 필요"

# 약 데이터: 간단 요약용
Drug = Dict[str, Any]

drugs: List[Drug] = [
    {
        "name": "타이레놀(아세트아미노펜)",
        "class": "해열진통제",
        "actives": ["Acetaminophen"],
        "indications": ["두통", "발열", "감기", "근육통", "치통"],
        "avoid_if": [
            "중증 간질환", "과다음주/만성음주", "아세트아미노펜 과민반응"
        ],
        "cautions": [
            "다른 감기약과 중복 복용 시 성분 중복(아세트아미노펜) 주의",
            "권장 용량 초과 금지 (간 손상 위험)",
        ],
        "dose_note": "성인 500 mg 1회, 필요 시 4~6시간 간격. 1일 최대 4,000 mg 초과 금지.",
        "availability": CONVENIENCE_MINIPACK,
    },
    {
        "name": "이부프로펜(브루펜 등)",
        "class": "해열진통·소염제(NSAID)",
        "actives": ["Ibuprofen"],
        "indications": ["두통", "생리통", "근육통", "염증", "발열"],
        "avoid_if": [
            "소화성 궤양/위장 출혈", "중증 신장질환", "임신 3분기", "아스피린 천식",
        ],
        "cautions": [
            "항응고제, 스테로이드와 병용 시 위장 출혈 위험 증가",
            "천식/고혈압/신장질환 병력자 주의",
        ],
        "dose_note": "성인 200~400 mg 1회, 필요 시 6~8시간 간격.",
        "availability": PHARMACY_ONLY,
    },
    {
        "name": "나프록센(낙센 등)",
        "class": "해열진통·소염제(NSAID)",
        "actives": ["Naproxen"],
        "indications": ["두통", "생리통", "근육통", "염증"],
        "avoid_if": ["소화성 궤양/위장 출혈", "중증 신장질환", "임신 3분기"],
        "cautions": ["항응고제와 병용 주의", "위장장애 시 음식과 함께 복용"],
        "dose_note": "성인 220 mg 1~2정, 8~12시간 간격.",
        "availability": PHARMACY_ONLY,
    },
    {
        "name": "덱스트로메토르판(기침 억제)",
        "class": "진해제",
        "actives": ["Dextromethorphan"],
        "indications": ["마른기침"],
        "avoid_if": ["MAOI 복용중"],
        "cautions": [
            "과량 시 어지러움/졸림",
            "세로토닌 증후군 위험 (SSRI 등과 병용 주의)",
        ],
        "dose_note": "성인 10~30 mg 1회, 4~6시간 간격. 제품별 용량 확인.",
        "availability": PHARMACY_ONLY,
    },
    {
        "name": "구아이페네신(가래 배출)",
        "class": "거담제",
        "actives": ["Guaifenesin"],
        "indications": ["가래", "가래기침"],
        "avoid_if": [],
        "cautions": ["복용 중 수분 섭취 충분히"],
        "dose_note": "성인 200~400 mg 4시간 간격 또는 서방형 600~1200 mg 12시간 간격.",
        "availability": PHARMACY_ONLY,
    },
    {
        "name": "세티리진(지르텍 등)",
        "class": "항히스타민제(2세대)",
        "actives": ["Cetirizine"],
        "indications": ["재채기", "콧물", "가려움", "알레르기비염"],
        "avoid_if": ["중증 신장질환"],
        "cautions": ["졸림 가능, 운전 주의"],
        "dose_note": "성인 10 mg 1일 1회.",
        "availability": PHARMACY_ONLY,
    },
    {
        "name": "로라타딘(클라리틴 등)",
        "class": "항히스타민제(2세대)",
        "actives": ["Loratadine"],
        "indications": ["재채기", "콧물", "가려움", "알레르기비염"],
        "avoid_if": [],
        "cautions": ["간질환 시 용량/복용 간격 조정 고려"],
        "dose_note": "성인 10 mg 1일 1회.",
        "availability": PHARMACY_ONLY,
    },
    {
        "name": "파모티딘(가스터 등)",
        "class": "위산분비억제제(H2RA)",
        "actives": ["Famotidine"],
        "indications": ["속쓰림", "위산역류", "소화불량"],
        "avoid_if": ["중증 신장질환"],
        "cautions": ["증상 지속/체중감소/흑변 동반 시 진료"],
        "dose_note": "성인 10~20 mg 1~2회/일, 증상 시.",
        "availability": PHARMACY_ONLY,
    },
    {
        "name": "디오스멕타이트(스멕타 등)",
        "class": "지사·흡착제",
        "actives": ["Diosmectite"],
        "indications": ["설사", "묽은변"],
        "avoid_if": ["장폐색 의심"],
        "cautions": ["탈수 예방 위해 수분/전해질 보충 병행"],
        "dose_note": "성인 1포 1일 3회, 물에 타서.",
        "availability": PHARMACY_ONLY,
    },
    {
        "name": "로페라마이드(로페민 등)",
        "class": "지사제(장운동 억제)",
        "actives": ["Loperamide"],
        "indications": ["급성 설사"],
        "avoid_if": ["고열/혈변/세균성 장염 의심", "소아"],
        "cautions": ["남용 시 장폐색 위험", "감염성 설사 의심 시 사용 금기"],
        "dose_note": "성인 초회 4 mg, 이후 설사 시 2 mg, 1일 최대 8 mg(OTC).",
        "availability": PHARMACY_ONLY,
    },
]

# 증상 → 가능 질환(간단 규칙)
condition_rules = {
    "두통": [
        {"name": "긴장형 두통", "hints": ["목 뻐근", "스트레스", "양쪽"], "notes": "대부분 휴식/진통제로 호전."},
        {"name": "편두통", "hints": ["한쪽", "구역", "빛/소리 민감"], "notes": "카페인/수면패턴 교정 도움."},
    ],
    "발열": [
        {"name": "감염에 의한 열", "hints": ["오한", "몸살"], "notes": "수분섭취, 해열제 고려."}
    ],
    "기침": [
        {"name": "상기도 감염(감기)", "hints": ["콧물", "인후통"], "notes": "대개 1~2주 내 호전."},
        {"name": "후비루/알레르기", "hints": ["재채기", "맑은 콧물"], "notes": "항히스타민이 도움."}
    ],
    "가래": [
        {"name": "기관지염", "hints": ["가슴 답답", "기침"], "notes": "수분섭취와 거담제 고려."}
    ],
    "콧물": [
        {"name": "알레르기 비염", "hints": ["가려움", "재채기"], "notes": "2세대 항히스타민 우선."}
    ],
    "재채기": [
        {"name": "알레르기 비염", "hints": ["가려움", "콧물"], "notes": "원인 회피 및 항히스타민."}
    ],
    "인후통": [
        {"name": "인두염(바이러스성)", "hints": ["기침", "콧물"], "notes": "진통제/수분섭취."},
    ],
    "속쓰림": [
        {"name": "위식도역류", "hints": ["야간 악화", "신물"], "notes": "야식/과식 피하기, H2RA 고려."}
    ],
    "소화불량": [
        {"name": "기능성 소화불량", "hints": ["더부룩"], "notes": "식습관 교정 + 제산/위산억제제."}
    ],
    "설사": [
        {"name": "급성 장염", "hints": ["복통", "구토"], "notes": "ORS로 수분/전해질 보충 필수."}
    ],
    "생리통": [
        {"name": "원발성 월경통", "hints": ["허리통증"], "notes": "온찜질 + NSAID 도움."}
    ],
}

# 응급/진료 필요(빨간 깃발) 키워드
red_flags = [
    ("두통", "갑작스럽고 인생 최악의 두통", "즉시 응급실"),
    ("발열", "3일 이상 고열 지속 또는 39℃ 이상", "진료 권장"),
    ("기침", "3주 이상 지속/피 섞인 가래/호흡곤란", "진료 권장"),
    ("설사", "혈변/고열/심한 탈수", "진료 권장"),
    ("인후통", "호흡 곤란/침 삼키기 어려움", "즉시 진료"),
    ("속쓰림", "흉통/운동 시 악화/식은땀 동반", "심장질환 감별 필요"),
]

# 증상 키워드 → 추천 약 매핑(간단 규칙)
symptom_to_drugs = {
    "두통": ["타이레놀(아세트아미노펜)", "이부프로펜(브루펜 등)", "나프록센(낙센 등)"],
    "발열": ["타이레놀(아세트아미노펜)", "이부프로펜(브루펜 등)"],
    "기침": ["덱스트로메토르판(기침 억제)", "구아이페네신(가래 배출)"],
    "가래": ["구아이페네신(가래 배출)"],
    "콧물": ["세티리진(지르텍 등)", "로라타딘(클라리틴 등)"],
    "재채기": ["세티리진(지르텍 등)", "로라타딘(클라리틴 등)"],
    "인후통": ["타이레놀(아세트아미노펜)"],
    "속쓰림": ["파모티딘(가스터 등)"],
    "소화불량": ["파모티딘(가스터 등)"],
    "설사": ["디오스멕타이트(스멕타 등)", "로페라마이드(로페민 등)"],
    "생리통": ["이부프로펜(브루펜 등)", "나프록센(낙센 등)"],
}

# ------------------------------
# 유틸 함수
# ------------------------------

def find_drug(name: str) -> Drug:
    for d in drugs:
        if d["name"] == name:
            return d
    return {}


def match_conditions(selected: List[str], detail: str) -> List[Dict[str, str]]:
    results = []
    for s in selected:
        if s in condition_rules:
            for rule in condition_rules[s]:
                score = 1
                for h in rule["hints"]:
                    if h in detail:
                        score += 1
                results.append({"name": rule["name"], "score": str(score), "notes": rule["notes"], "symptom": s})
    # 점수순
    results.sort(key=lambda x: int(x["score"]), reverse=True)
    return results


def collect_red_flags(selected: List[str], detail: str) -> List[str]:
    alerts = []
    for key, rf, action in red_flags:
        if key in selected and any(tok in detail for tok in rf.split("/")):
            alerts.append(f"{key}: {rf} → {action}")
    return alerts


def filter_by_contra(drug: Drug, ctx: Dict[str, Any]) -> Dict[str, Any]:
    """금기/주의 상황 반영해 주의 메시지 생성"""
    warnings = []
    # 상황별 주의
    if ctx.get("pregnant"):
        # 임신 3분기 NSAID 금기, 임신 중엔 전문가 상담 권장
        if "소염제" in drug.get("class", "") or "NSAID" in drug.get("class", ""):
            warnings.append("임신 후기(NSAID 금기) 가능성 시 복용 금지. 전문가 상담 필요.")
    if ctx.get("liver") and "Acetaminophen" in ",".join(drug.get("actives", [])):
        warnings.append("간질환 보유: 아세트아미노펜 용량 엄격 준수 또는 회피 고려.")
    if ctx.get("kidney") and ("NSAID" in drug.get("class", "") or drug["name"].startswith("나프록센") or drug["name"].startswith("이부프로펜")):
        warnings.append("신장질환 보유: NSAID는 악화 가능. 전문가 상담.")
    if ctx.get("anticoagulant") and ("NSAID" in drug.get("class", "")):
        warnings.append("항응고제 복용 중: NSAID 병용 시 출혈 위험↑")
    if ctx.get("maoi") and ("Dextromethorphan" in ",".join(drug.get("actives", []))):
        warnings.append("MAOI 복용 중: 덱스트로메토르판 병용 금기.")
    if ctx.get("ssri") and ("Dextromethorphan" in ",".join(drug.get("actives", []))):
        warnings.append("SSRI 등과 병용 시 세로토닌 증후군 위험.")

    # 약 자체의 회피 조건
    for cond in drug.get("avoid_if", []):
        if any(key in ctx.get("raw_detail", "") for key in ["혈변", "고열", "흑변"]):
            # red flag와 겹치는 키워드가 detail에 들어있는 경우 강조
            warnings.append(f"현재 상태에서 사용 피하거나 전문가 상담: {cond}")
    return {"drug": drug, "warnings": warnings}


# ------------------------------
# 사이드바 입력
# ------------------------------
with st.sidebar:
    st.markdown("### 🧾 기본 정보")
    age = st.number_input("나이", min_value=0, max_value=120, value=20, step=1)
    sex = st.selectbox("생물학적 성별", ["여성", "남성", "기타/응답안함"], index=0)
    pregnant = st.checkbox("임신/임신 가능성") if sex == "여성" else False

    st.markdown("### 💡 건강 상태")
    liver = st.checkbox("간질환이 있다")
    kidney = st.checkbox("신장질환이 있다")
    ulcer = st.checkbox("위궤양/위장출혈 병력")

    st.markdown("### 💊 복용 중 약물")
    anticoagulant = st.checkbox("항응고제 복용 중")
    ssri = st.checkbox("SSRI/세로토닌계 항우울제 복용 중")
    maoi = st.checkbox("MAOI 복용 중")

    st.markdown("---")
    st.caption("⚠️ 이 앱은 의료진의 진단을 대체하지 않습니다. 심한 증상/빨간 깃발 시 즉시 진료.")

# ------------------------------
# 메인 입력
# ------------------------------
st.title("💊 증상 맞춤 의약품 추천 (참고용)")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("#### 1) 증상 선택")
    all_symptoms = list(symptom_to_drugs.keys())
    selected = st.multiselect("해당되는 증상을 모두 선택하세요", options=all_symptoms, default=[])

    st.markdown("#### 2) 증상 상세")
    detail = st.text_area(
        "언제부터, 어떤 양상인지 자세히 써주세요 (예: 한쪽 두통/빛에 민감, 39도 고열, 혈변 등)",
        height=120,
    )

    st.markdown("#### 3) 생활/체질 특이사항 (선택)")
    tags = st.tags = st.text_input("카페인 민감, 졸림 민감, 야간근무, 천식 등 키워드")

    ctx = {
        "age": age,
        "sex": sex,
        "pregnant": pregnant,
        "liver": liver,
        "kidney": kidney,
        "ulcer": ulcer,
        "anticoagulant": anticoagulant,
        "ssri": ssri,
        "maoi": maoi,
        "raw_detail": detail,
        "trait_tags": tags,
    }

with col2:
    st.markdown("#### 결과")

    if not selected:
        st.info("왼쪽에서 증상을 선택하면 추천이 표시됩니다.")
    else:
        # 1) 의심 질환
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🩺 의심 질환(참고)</div>', unsafe_allow_html=True)
        conditions = match_conditions(selected, detail)
        if conditions:
            for c in conditions[:6]:
                st.markdown(
                    f"**{c['name']}** · <span class='muted small'>({c['symptom']}, 단서일치 {c['score']})</span><br><span class='small'>{c['notes']}</span>",
                    unsafe_allow_html=True,
                )
        else:
            st.write("선택한 증상으로 특정하기 어렵습니다. 증상 상세를 더 적어주세요.")
        st.markdown('</div>', unsafe_allow_html=True)

        # 2) 빨간 깃발
        alerts = collect_red_flags(selected, detail)
        if alerts:
            st.markdown('<div class="app-card" style="border-color:#fecaca;background:#fff7f7">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🚩 즉시 주의/진료 권고</div>', unsafe_allow_html=True)
            for a in alerts:
                st.markdown(f"<span class='tag red'>{a}</span>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 3) 추천 약
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">💡 추천 일반의약품(OTC)</div>', unsafe_allow_html=True)

        recommended: List[Drug] = []
        for s in selected:
            for name in symptom_to_drugs.get(s, []):
                d = find_drug(name)
                if d and d not in recommended:
                    recommended.append(d)

        if not recommended:
            st.write("해당 증상에 대한 일반의약품 추천 정보가 부족합니다.")
        else:
            for d in recommended:
                filt = filter_by_contra(d, ctx)
                with st.container(border=True):
                    left, right = st.columns([2,1])
                    with left:
                        st.markdown(f"**{d['name']}** · {d['class']}")
                        st.markdown(
                            """
                            - 적응증: %s  
                            - 복용: %s
                            """ % (", ".join(d["indications"]), d["dose_note"])
                        )
                        if d.get("cautions"):
                            st.markdown("**주의사항:** ")
                            for c in d["cautions"]:
                                st.markdown(f"<span class='pill'>{c}</span>", unsafe_allow_html=True)
                        if filt["warnings"]:
                            st.markdown("**개인 상황 주의:** ")
                            for w in filt["warnings"]:
                                st.markdown(f"<span class='pill'>{w}</span>", unsafe_allow_html=True)
                    with right:
                        avail = d["availability"]
                        if avail == PRESCRIPTION:
                            tag_class = "red"
                        elif avail == CONVENIENCE_MINIPACK:
                            tag_class = "yellow"
                        else:
                            tag_class = "green"
                        st.markdown(f"<span class='tag {tag_class}'>가용성: {avail}</span>", unsafe_allow_html=True)
                        st.markdown("<span class='muted small'>*한국 기준: 일부 OTC는 편의점 소포장 판매*</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 4) 처방전 필요 가능 영역(예시 안내)
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🧠 처방전이 필요한 경우 예시</div>', unsafe_allow_html=True)
        st.markdown(
            """
            - **세균 감염 의심**(중이염/축농증/폐렴 등): 항생제는 **처방전 필요**
            - **위산 과다로 장기 복용 필요**: 고용량 PPI 등은 **처방전 필요**
            - **천식/만성기침**: 흡입제/장기치료는 **처방전 필요**
            - **심한 통증/염증**: 주사제/강력 진통제는 **처방전 필요**
            """
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # 5) 생활요법/셀프케어 팁(간단)
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🌿 셀프케어 팁</div>', unsafe_allow_html=True)
        st.markdown(
            """
            - **수분/휴식**: 감기/발열/설사 시 수분과 휴식이 가장 중요합니다.
            - **카페인/야식 조절**: 두통·역류성 식도염 악화 요인이 될 수 있어요.
            - **복약 간격/중복 성분 확인**: 종합감기약 + 해열제 동시 복용 시 성분 중복 주의.
            """
        )
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------
# 푸터
# ------------------------------
st.markdown("---")
st.caption(
    "이 정보는 교육·참고용으로 제공되며, 전문적인 의료 조언/진단/치료를 대체하지 않습니다. 심한 증상·빨간 깃발 시 즉시 의료기관을 이용하세요. (\u00a9 {year})".format(year=datetime.now().year)
)
