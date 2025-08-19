# app.py — 증상 기반 의약품 추천 (참고용)
# -----------------------------------------------------------------------------
# 목적:
#   - 사용자가 증상을 입력하면 관련 일반의약품(OTC)을 추천하고,
#     의심 질환, 주의 체질/상황(금기/상호작용), 가용성(약국/편의점/처방전) 정보를 제공.
#   - 직관적·모던 UI, 모듈화된 구조, 풍부한 주석과 빠른 실행.
# 면책:
#   - 이 앱은 의료진의 진단·치료를 대체하지 않으며, 참고용 정보를 제공합니다.
#   - 빨간 깃발(위험 신호) 시 즉시 의료기관을 방문하세요.
# -----------------------------------------------------------------------------

from __future__ import annotations
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Tuple

import pandas as pd
import streamlit as st

# =============================
# 0) 페이지/테마/스타일 설정
# =============================

def configure_page() -> None:
    st.set_page_config(
        page_title="증상 맞춤 의약품 추천 (참고용)",
        page_icon="💊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    # 미니멀하지만 또렷한 모던 스타일
    st.markdown(
        """
        <style>
          :root { --radius: 16px; }
          .app-card { border:1px solid rgba(0,0,0,.08); border-radius:var(--radius); padding:18px; background:#fff; box-shadow:0 6px 18px rgba(0,0,0,.04); }
          .soft { background:#fafafa; border:1px dashed #e5e7eb; }
          .tag { display:inline-block; padding:4px 10px; border-radius:999px; border:1px solid rgba(0,0,0,.08); margin:3px 8px 3px 0; font-size:12px; }
          .tag.green { background:#f0fff4; border-color:#a7f3d0; }
          .tag.yellow { background:#fffbeb; border-color:#fde68a; }
          .tag.red { background:#fef2f2; border-color:#fecaca; }
          .pill { display:inline-block; padding:4px 10px; border-radius:999px; background:#f4f4f5; margin:2px; font-size:12px; }
          .muted { color:#6b7280; }
          .small { font-size:12px; }
          .section-title { font-weight:700; font-size:18px; margin-bottom:8px; }
          .kbd { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; background:#f3f4f6; padding:2px 6px; border-radius:6px; border:1px solid #e5e7eb; }
          .grid-2 { display:grid; grid-template-columns: 1fr 1fr; gap:12px; }
          .grid-3 { display:grid; grid-template-columns: 1fr 1fr 1fr; gap:12px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# =============================
# 1) 데이터 모델/지식 베이스
# =============================

@dataclass
class Drug:
    name: str
    dclass: str
    actives: List[str]
    indications: List[str]
    avoid_if: List[str] = field(default_factory=list)
    cautions: List[str] = field(default_factory=list)
    dose_note: str = ""
    availability: str = "약국 구매"  # "약국 구매" | "약국 + 일부 편의점 소포장" | "처방전 필요"


@st.cache_data(show_spinner=False)
def load_kb() -> Dict[str, Any]:
    """지식 베이스 로드(로컬 상수) — 실제 서비스에서는 DB/시트 연동.
    cache_data로 빠르게 재사용."""
    PHARMACY_ONLY = "약국 구매"
    CONVENIENCE_MINIPACK = "약국 + 일부 편의점 소포장"
    PRESCRIPTION = "처방전 필요"

    drugs: List[Drug] = [
        Drug(
            name="타이레놀(아세트아미노펜)",
            dclass="해열진통제",
            actives=["Acetaminophen"],
            indications=["두통", "발열", "감기", "근육통", "치통"],
            avoid_if=["중증 간질환", "과다음주/만성음주", "아세트아미노펜 과민반응"],
            cautions=[
                "다른 감기약과 성분 중복(아세트아미노펜) 주의",
                "권장 용량 초과 금지 (간 손상 위험)",
            ],
            dose_note="성인 500 mg 1회, 필요 시 4~6시간 간격. 1일 최대 4,000 mg 초과 금지.",
            availability=CONVENIENCE_MINIPACK,
        ),
        Drug(
            name="이부프로펜(브루펜 등)",
            dclass="해열진통·소염제(NSAID)",
            actives=["Ibuprofen"],
            indications=["두통", "생리통", "근육통", "염증", "발열"],
            avoid_if=["소화성 궤양/위장 출혈", "중증 신장질환", "임신 3분기", "아스피린 천식"],
            cautions=[
                "항응고제/스테로이드 병용 시 위장 출혈 위험 증가",
                "천식/고혈압/신장질환 병력자 주의",
            ],
            dose_note="성인 200~400 mg 1회, 필요 시 6~8시간 간격.",
            availability=PHARMACY_ONLY,
        ),
        Drug(
            name="나프록센(낙센 등)",
            dclass="해열진통·소염제(NSAID)",
            actives=["Naproxen"],
            indications=["두통", "생리통", "근육통", "염증"],
            avoid_if=["소화성 궤양/위장 출혈", "중증 신장질환", "임신 3분기"],
            cautions=["항응고제 병용 주의", "위장장애 시 음식과 함께 복용"],
            dose_note="성인 220 mg 1~2정, 8~12시간 간격.",
            availability=PHARMACY_ONLY,
        ),
        Drug(
            name="덱스트로메토르판(기침 억제)",
            dclass="진해제",
            actives=["Dextromethorphan"],
            indications=["마른기침"],
            avoid_if=["MAOI 복용중"],
            cautions=["과량 시 어지러움/졸림", "SSRI 등과 병용 시 세로토닌 증후군 위험"],
            dose_note="성인 10~30 mg 1회, 4~6시간 간격. 제품별 용량 확인.",
            availability=PHARMACY_ONLY,
        ),
        Drug(
            name="구아이페네신(가래 배출)",
            dclass="거담제",
            actives=["Guaifenesin"],
            indications=["가래", "가래기침"],
            cautions=["복용 중 수분 섭취 충분히"],
            dose_note="성인 200~400 mg 4시간 간격 또는 서방형 600~1200 mg 12시간 간격.",
            availability=PHARMACY_ONLY,
        ),
        Drug(
            name="세티리진(지르텍 등)",
            dclass="항히스타민제(2세대)",
            actives=["Cetirizine"],
            indications=["재채기", "콧물", "가려움", "알레르기비염"],
            avoid_if=["중증 신장질환"],
            cautions=["졸림 가능, 운전 주의"],
            dose_note="성인 10 mg 1일 1회.",
            availability=PHARMACY_ONLY,
        ),
        Drug(
            name="로라타딘(클라리틴 등)",
            dclass="항히스타민제(2세대)",
            actives=["Loratadine"],
            indications=["재채기", "콧물", "가려움", "알레르기비염"],
            cautions=["간질환 시 용량/복용 간격 조정 고려"],
            dose_note="성인 10 mg 1일 1회.",
            availability=PHARMACY_ONLY,
        ),
        Drug(
            name="파모티딘(가스터 등)",
            dclass="위산분비억제제(H2RA)",
            actives=["Famotidine"],
            indications=["속쓰림", "위산역류", "소화불량"],
            avoid_if=["중증 신장질환"],
            cautions=["증상 지속/체중감소/흑변 동반 시 진료"],
            dose_note="성인 10~20 mg 1~2회/일, 증상 시.",
            availability=PHARMACY_ONLY,
        ),
        Drug(
            name="디오스멕타이트(스멕타 등)",
            dclass="지사·흡착제",
            actives=["Diosmectite"],
            indications=["설사", "묽은변"],
            avoid_if=["장폐색 의심"],
            cautions=["탈수 예방 위해 수분/전해질 보충 병행"],
            dose_note="성인 1포 1일 3회, 물에 타서.",
            availability=PHARMACY_ONLY,
        ),
        Drug(
            name="로페라마이드(로페민 등)",
            dclass="지사제(장운동 억제)",
            actives=["Loperamide"],
            indications=["급성 설사"],
            avoid_if=["고열/혈변/세균성 장염 의심", "소아"],
            cautions=["감염성 설사 의심 시 사용 금기", "남용 시 장폐색 위험"],
            dose_note="성인 초회 4 mg, 이후 설사 시 2 mg, 1일 최대 8 mg(OTC).",
            availability=PHARMACY_ONLY,
        ),
    ]

    # 증상 → 추천 약(이름) 매핑
    symptom_to_drugs: Dict[str, List[str]] = {
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

    # 증상 → 의심 질환/설명
    condition_rules: Dict[str, List[Dict[str, str]]] = {
        "두통": [
            {"name": "긴장형 두통", "hints": "목 뻐근/스트레스/양쪽", "notes": "대부분 휴식/진통제로 호전"},
            {"name": "편두통", "hints": "한쪽/구역/빛·소리 민감", "notes": "카페인/수면패턴 교정 도움"},
        ],
        "발열": [
            {"name": "감염성 발열", "hints": "오한/몸살", "notes": "수분섭취/해열제 고려"}
        ],
        "기침": [
            {"name": "상기도감염", "hints": "콧물/인후통", "notes": "대개 1~2주 내 호전"},
            {"name": "후비루/알레르기", "hints": "재채기/맑은 콧물", "notes": "항히스타민 도움"},
        ],
        "가래": [
            {"name": "기관지염", "hints": "흉부 답답/기침", "notes": "수분섭취 + 거담제"}
        ],
        "콧물": [
            {"name": "알레르기 비염", "hints": "가려움/재채기", "notes": "2세대 항히스타민"}
        ],
        "인후통": [
            {"name": "바이러스성 인두염", "hints": "기침/콧물", "notes": "진통제/수분섭취"}
        ],
        "속쓰림": [
            {"name": "위식도역류", "hints": "야간 악화/신물", "notes": "야식·과식 회피 + H2RA"}
        ],
        "설사": [
            {"name": "급성 장염", "hints": "복통/구토", "notes": "ORS로 전해질 보충 필수"}
        ],
        "생리통": [
            {"name": "원발성 월경통", "hints": "허리통증", "notes": "온찜질 + NSAID"}
        ],
    }

    red_flags: List[Tuple[str, str, str]] = [
        ("두통", "갑작스럽고 인생 최악의 두통", "즉시 응급실"),
        ("발열", "39℃ 이상 또는 3일 이상 고열", "진료 권장"),
        ("기침", "3주 이상 지속/혈담/호흡곤란", "진료 권장"),
        ("설사", "혈변/고열/심한 탈수", "진료 권장"),
        ("인후통", "호흡 곤란/침 삼키기 어려움", "즉시 진료"),
        ("속쓰림", "흉통/운동 시 악화/식은땀", "심장질환 감별 필요"),
    ]

    return {
        "drugs": drugs,
        "symptom_to_drugs": symptom_to_drugs,
        "condition_rules": condition_rules,
        "red_flags": red_flags,
    }


# =============================
# 2) 추천 로직 (모듈화)
# =============================

def find_drug(kb: Dict[str, Any], name: str) -> Drug | None:
    for d in kb["drugs"]:
        if d.name == name:
            return d
    return None


def match_conditions(kb: Dict[str, Any], selected: List[str], detail: str) -> List[Dict[str, Any]]:
    """증상/상세 키워드로 의심 질환 스코어링."""
    results: List[Dict[str, Any]] = []
    detail_tokens = [t.strip() for t in detail.split() if t.strip()]
    for s in selected:
        for rule in kb["condition_rules"].get(s, []):
            hints = [h.strip() for h in rule["hints"].split("/")]
            score = 1 + sum(1 for h in hints if any(h in tok for tok in detail_tokens))
            results.append({
                "name": rule["name"],
                "symptom": s,
                "score": score,
                "notes": rule["notes"],
            })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def collect_red_flags(kb: Dict[str, Any], selected: List[str], detail: str) -> List[str]:
    alerts: List[str] = []
    for key, rf, action in kb["red_flags"]:
        if key in selected and any(tok in detail for tok in rf.split("/")):
            alerts.append(f"{key}: {rf} → {action}")
    return alerts


def personalize_warnings(drug: Drug, ctx: Dict[str, Any]) -> List[str]:
    """개인 상황(임신, 간/신장, 항응고제 등)에 따른 주의 메시지."""
    warnings: List[str] = []
    is_nsaid = ("NSAID" in drug.dclass) or any(key in drug.name for key in ["이부프로펜", "나프록센"])

    if ctx.get("pregnant") and is_nsaid:
        warnings.append("임신 후기(NSAID 금기) 가능성 시 복용 금지. 전문가 상담 필요")
    if ctx.get("liver") and "Acetaminophen" in ",".join(drug.actives):
        warnings.append("간질환: 아세트아미노펜 용량 엄격 준수 또는 회피 고려")
    if ctx.get("kidney") and is_nsaid:
        warnings.append("신장질환: NSAID는 악화 가능 — 전문가 상담")
    if ctx.get("anticoagulant") and is_nsaid:
        warnings.append("항응고제 병용: 위장출혈 위험 증가")
    if ctx.get("maoi") and "Dextromethorphan" in ",".join(drug.actives):
        warnings.append("MAOI 병용 금기(덱스트로메토르판)")
    if ctx.get("ssri") and "Dextromethorphan" in ",".join(drug.actives):
        warnings.append("SSRI 등과 병용 시 세로토닌 증후군 위험")
    return warnings


def recommend_drugs(kb: Dict[str, Any], selected: List[str]) -> List[Drug]:
    seen = set()
    rec: List[Drug] = []
    for s in selected:
        for name in kb["symptom_to_drugs"].get(s, []):
            if name not in seen:
                d = find_drug(kb, name)
                if d:
                    rec.append(d)
                    seen.add(name)
    return rec


# =============================
# 3) UI 렌더링 (컴포넌트 함수)
# =============================

def header() -> None:
    st.title("💊 증상 맞춤 의약품 추천 (참고용)")
    st.markdown(
        """
        - 증상을 선택/기입하면 **추천 일반의약품**, **의심 질환**, **주의 체질/상황**, **가용성**을 보여줍니다.  
        - ⚠️ *본 정보는 참고용이며 진단이 아닙니다. 심한 증상·빨간 깃발 시 즉시 의료기관 이용.*
        """
    )


def sidebar_inputs() -> Dict[str, Any]:
    st.sidebar.header("🧾 기본 정보")
    age = st.sidebar.number_input("나이", min_value=0, max_value=120, value=20, step=1)
    sex = st.sidebar.selectbox("생물학적 성별", ["여성", "남성", "기타/응답안함"], index=0)
    pregnant = st.sidebar.checkbox("임신/임신 가능성") if sex == "여성" else False

    st.sidebar.header("💡 건강 상태")
    liver = st.sidebar.checkbox("간질환이 있다")
    kidney = st.sidebar.checkbox("신장질환이 있다")
    ulcer = st.sidebar.checkbox("위궤양/위장출혈 병력")

    st.sidebar.header("💊 복용 중 약물")
    anticoagulant = st.sidebar.checkbox("항응고제")
    ssri = st.sidebar.checkbox("SSRI/세로토닌계 항우울제")
    maoi = st.sidebar.checkbox("MAOI")

    st.sidebar.markdown("---")
    st.sidebar.caption("⚠️ 이 앱은 진단이 아닙니다. 빨간 깃발 시 즉시 진료.")

    return {
        "age": age,
        "sex": sex,
        "pregnant": pregnant,
        "liver": liver,
        "kidney": kidney,
        "ulcer": ulcer,
        "anticoagulant": anticoagulant,
        "ssri": ssri,
        "maoi": maoi,
    }


def symptom_inputs(kb: Dict[str, Any]) -> Tuple[List[str], str, List[str]]:
    st.markdown("#### 1) 증상 선택")
    chips = sorted(list(kb["symptom_to_drugs"].keys()))
    cols = st.columns(6)
    picked: List[str] = []
    for i, chip in enumerate(chips):
        if cols[i % 6].toggle(chip, key=f"chip_{chip}"):
            picked.append(chip)

    st.markdown("#### 2) 증상 상세")
    detail = st.text_area(
        "언제부터, 어떤 양상인지 자세히 (예: 한쪽 두통/빛 민감, 39도 고열, 혈변 등)",
        height=100,
        placeholder="예: 어제부터 한쪽이 지끈거리는 두통과 구역감, 빛/소리에 민감함",
    )

    st.markdown("#### 3) 추가 키워드 (선택)")
    tags_str = st.text_input("카페인 민감, 야간근무, 천식 등 쉼표로 구분")
    tags = [t.strip() for t in tags_str.split(',') if t.strip()]

    return picked, detail, tags


def card_conditions(conditions: List[Dict[str, Any]]):
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🩺 의심 질환(참고)</div>', unsafe_allow_html=True)
    if not conditions:
        st.write("선택한 증상으로 특정하기 어렵습니다. 증상 상세를 더 적어주세요.")
    else:
        for c in conditions[:6]:
            st.markdown(
                f"**{c['name']}** · <span class='muted small'>({c['symptom']}, 점수 {c['score']})</span><br><span class='small'>{c['notes']}</span>",
                unsafe_allow_html=True,
            )
    st.markdown('</div>', unsafe_allow_html=True)


def card_alerts(alerts: List[str]):
    if not alerts:
        return
    st.markdown('<div class="app-card" style="border-color:#fecaca;background:#fff7f7">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🚩 즉시 주의/진료 권고</div>', unsafe_allow_html=True)
    for a in alerts:
        st.markdown(f"<span class='tag red'>{a}</span>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def card_drug(drug: Drug, personal_warnings: List[str]):
    with st.container(border=True):
        left, right = st.columns([2, 1])
        with left:
            st.markdown(f"**{drug.name}** · {drug.dclass}")
            st.markdown(
                """
                - 적응증: %s  
                - 복용: %s
                """ % (", ".join(drug.indications), drug.dose_note)
            )
            if drug.cautions:
                st.markdown("**주의사항:** ")
                for c in drug.cautions:
                    st.markdown(f"<span class='pill'>{c}</span>", unsafe_allow_html=True)
            if personal_warnings:
                st.markdown("**개인 상황 주의:** ")
                for w in personal_warnings:
                    st.markdown(f"<span class='pill'>{w}</span>", unsafe_allow_html=True)
        with right:
            tag_class = (
                "red" if drug.availability == "처방전 필요" else
                "yellow" if drug.availability == "약국 + 일부 편의점 소포장" else
                "green"
            )
            st.markdown(
                f"<span class='tag {tag_class}'>가용성: {drug.availability}</span>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<span class='muted small'>*한국 기준: 일부 OTC는 편의점 소포장 판매*</span>",
                unsafe_allow_html=True,
            )


def card_recommendations(kb: Dict[str, Any], selected: List[str], ctx: Dict[str, Any]):
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💡 추천 일반의약품(OTC)</div>', unsafe_allow_html=True)
    rec = recommend_drugs(kb, selected)
    if not rec:
        st.write("해당 증상에 대한 일반의약품 추천 정보가 부족합니다.")
    else:
        for d in rec:
            warns = personalize_warnings(d, ctx)
            card_drug(d, warns)
    st.markdown('</div>', unsafe_allow_html=True)


def card_prescription_examples():
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧠 처방전이 필요한 경우 예시</div>', unsafe_allow_html=True)
    st.markdown(
        """
        - **세균 감염 의심**(중이염/축농증/폐렴 등): 항생제는 **처방전 필요**
        - **역류/위염 장기치료 필요**: 고용량 PPI 등은 **처방전 필요**
        - **천식/만성기침**: 흡입제/장기치료는 **처방전 필요**
        - **심한 통증/염증**: 주사제/강력 진통제는 **처방전 필요**
        """
    )
    st.markdown('</div>', unsafe_allow_html=True)


def card_selfcare():
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🌿 셀프케어 팁</div>', unsafe_allow_html=True)
    st.markdown(
        """
        - **수분/휴식**: 감기/발열/설사 시 수분과 휴식이 중요합니다.
        - **카페인/야식 조절**: 두통·역류성 식도염 악화 요인일 수 있어요.
        - **복약 간격/중복 성분 확인**: 종합감기약 + 해열제 동시 복용 시 성분 중복 주의.
        """
    )
    st.markdown('</div>', unsafe_allow_html=True)


def tools_download_export(report: Dict[str, Any]):
    """현재 결과를 JSON/CSV로 내보내는 도구."""
    st.markdown('<div class="app-card soft">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📦 결과 저장/내보내기</div>', unsafe_allow_html=True)

    # JSON 다운로드
    st.download_button(
        label="JSON 다운로드",
        file_name=f"symptom_reco_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        data=json.dumps(report, ensure_ascii=False, indent=2),
        use_container_width=True,
    )

    # CSV(추천 약) 다운로드
    rec = report.get("recommendations", [])
    if rec:
        df = pd.DataFrame(rec)
        st.download_button(
            label="추천 약 CSV 다운로드",
            file_name=f"recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            data=df.to_csv(index=False),
            use_container_width=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)


def feedback_block():
    st.markdown('<div class="app-card soft">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🗳️ 앱 피드백</div>', unsafe_allow_html=True)
    colA, colB = st.columns([1, 3])
    with colA:
        fb = st.radio("이 정보가 도움이 되었나요?", ("네", "아니오"), horizontal=True)
    with colB:
        note = st.text_input("개선 의견이 있다면 적어주세요")
    if st.button("피드백 제출", use_container_width=True):
        st.success("의견 감사합니다! 다음 업데이트에 반영할게요.")
        st.caption(f"선택: {fb} / 메모: {note}")
    st.markdown('</div>', unsafe_allow_html=True)


# =============================
# 4) 메인 앱 실행 흐름
# =============================

def main() -> None:
    configure_page()
    kb = load_kb()

    header()
    ctx = sidebar_inputs()

    colL, colR = st.columns([1, 1])
    with colL:
        selected, detail, tags = symptom_inputs(kb)
    with colR:
        st.markdown("#### 결과")
        if not selected:
            st.info("왼쪽에서 증상을 선택하면 추천이 표시됩니다.")
        else:
            # 1) 의심 질환
            conditions = match_conditions(kb, selected, detail)
            card_conditions(conditions)

            # 2) 빨간 깃발
            alerts = collect_red_flags(kb, selected, detail)
            card_alerts(alerts)

            # 3) 추천 약
            card_recommendations(kb, selected, ctx)

            # 4) 처방전 필요 예시
            card_prescription_examples()

            # 5) 셀프케어 팁
            card_selfcare()

            # 6) 내보내기/저장
            rec_rows = []
            for s in selected:
                for name in kb["symptom_to_drugs"].get(s, []):
                    d = find_drug(kb, name)
                    if d:
                        rec_rows.append({
                            "증상": s,
                            "약명": d.name,
                            "분류": d.dclass,
                            "성분": ", ".join(d.actives),
                            "가용성": d.availability,
                        })
            report = {
                "timestamp": datetime.now().isoformat(),
                "selected_symptoms": selected,
                "detail": detail,
                "tags": tags,
                "recommendations": rec_rows,
                "alerts": alerts,
                "conditions": conditions,
            }
            tools_download_export(report)

            # 7) 피드백
            feedback_block()

    st.markdown("---")
    st.caption(
        "이 정보는 교육·참고용이며, 전문적인 의료 조언/진단/치료를 대체하지 않습니다. 심한 증상·빨간 깃발 시 즉시 의료기관을 이용하세요. (\u00a9 {year})".format(
            year=datetime.now().year
        )
    )


# =============================
# 5) 엔트리포인트
# =============================
if __name__ == "__main__":
    main()
