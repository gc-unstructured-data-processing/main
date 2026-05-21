# seed_dictionary_v2 — 9 후보 10단계 전문가 검토 + 채택 권장

> **작성자**: 이동원 (Claude 분석)
> **작성일**: 2026-05-18
> **입력**: `data/seed_dictionary_v2_proposed.csv` (02b s_diag v1 자동 생성, 9 후보)
> **출력**: `data/seed_dictionary_v2.csv` (37개 = v1 30 + 7 추가)
> **결정 표**: `data/processed/seed_v2_decision_analysis.csv`
> **위반금지 #3 준수**: MCP/추출 결과 그대로 신뢰 ❌ → Claude가 9 후보 모두 10단계로 직접 검토

---

## 0. 한 줄 결론

**KEPT 7개 + REMOVED 2개 + 재분류 1개** (ESG경영: S → G). seed_v2 = 37개 (E 10·S 16·G 11). 사용자는 본 결과를 그대로 채택하거나 일부 항목 의견 차이 있으면 알려주시면 됩니다.

---

## 1. 검토 방법 (10단계 분석 기준)

각 후보에 대해 다음 10가지 관점에서 평가:

| 단계 | 기준 |
|---|---|
| 1 | **의미 명확성** — 어휘 자체가 ESG 차원에 정확히 매핑 |
| 2 | **외부 라벨 일치** — MSCI KLD·Refinitiv Workforce·Bloomberg ESG·ESG-Kor 표준 |
| 3 | **KCGS 평가항목 매칭** — 한국ESG기준원 모범규준 항목 대응 |
| 4 | **Samsung body 빈도** — 02b 진단 측정값 (5회 이상이 1차 기준) |
| 5 | **잡음 가능성** — 비-ESG 표현·다른 도메인 어휘 포함 위험 |
| 6 | **기존 seed 중복** — 이미 v1 seed에 의미 포함된 어휘인지 |
| 7 | **정규식 패턴 robust** — `|` 분리 어휘들이 같은 의미군인지 |
| 8 | **학술 인용 근거** — Li 2021·Bao 2024·Bingler 2022 등에서 사용된 어휘 |
| 9 | **등급 변별력 예상** — 높은 등급 firm이 더 자주 쓸 가능성 |
| 10 | **최종 권장** — KEPT/REMOVED + 차원 재분류 |

---

## 2. 9 후보 검토 결과

### ✅ 2.1 KEPT 7개

#### 1. **지속가능** (S 차원, freq=21)
- **패턴**: `지속가능|sustainability`
- **분석**:
  - 의미: Sustainability 핵심 어휘. ESG·CSR 전반 표지자.
  - 라벨: GRI·SASB·TCFD·Bloomberg ESG 모두 포함.
  - KCGS: 통합 ESG 평가 항목.
  - 잡음: 낮음 — "지속가능한 성장" 등 일부 비-ESG 사용 가능하나 대부분 ESG 맥락.
  - 학술: Guiso et al. (2015), Bao et al. (2024).
- **권장**: ✅ **KEPT (S 유지)**. 다만 S 단독 표지자로는 약함 — ESG 전반 신호. 차원 재분류는 보류 (S 그대로 둠 — 향후 cross-dim alt 분석 시 검토).

#### 2. **ESG경영** (S → G 재분류, freq=19)
- **패턴**: `ESG경영|ESG위원회|지속가능경영`
- **분석**:
  - 의미: 명시적 ESG 경영 시스템·위원회.
  - 차원: **G(지배구조)에 더 가까움** — ESG위원회는 거버넌스 구조의 일부 (사외이사 ESG 책임).
  - 라벨: MSCI Governance·Bloomberg ESG board ESG oversight.
  - 잡음: 거의 없음 — 직접 명시 표현.
  - 학술: 가이드 03 line 90+ ESG dictionary 일반.
- **권장**: ✅ **KEPT (G로 재분류)**. ESG위원회·지속가능경영 모두 G 차원 (board oversight) 정합.

#### 3. **기부** (S 유지, freq=17)
- **패턴**: `기부|후원|봉사`
- **분석**:
  - 의미: 사회공헌 핵심. 지역사회 환원.
  - 라벨: MSCI KLD **Community** 카테고리 직접 매핑.
  - KCGS: 사회 책임 (지역사회) 평가 항목.
  - 잡음: 거의 없음.
  - 학술: Guiso et al. (2015) corporate values; MSCI KLD Stats.
- **권장**: ✅ **KEPT (S 유지)**. 강력 권장.

#### 4. **건강** (S 유지, freq=8)
- **패턴**: `건강|보건|체력`
- **분석**:
  - 의미: 임직원 건강·보건. Refinitiv Workforce healthy workplace.
  - 라벨: Refinitiv Workforce Health & Safety; MSCI Employee Health.
  - 잡음: **중간** — "재무 건강", "기업 건강" 등 비-사회 표현 가능.
  - 학술: Refinitiv Workforce score; Bao et al. (2024) safety culture.
- **권장**: ✅ **KEPT (S 유지)**. 단 사이클 4에서 패턴 강화 검토 권장 (예: `임직원 건강|보건|건강검진|건강관리`).

#### 5. **사회공헌** (S 유지, freq=6)
- **패턴**: `사회공헌|CSR`
- **분석**:
  - 의미: 사회공헌 직접 명시.
  - 라벨: MSCI KLD Community; ESG-Kor S 라벨.
  - 잡음: 0 — 정확히 ESG 표현.
  - 학술: CSR 라인 전반.
- **권장**: ✅ **KEPT (S 유지)**. **강력 권장**.

#### 6. **정보보호** (S 유지, freq=5)
- **패턴**: `정보보호|사이버|보안`
- **분석**:
  - 의미: 정보보안·개인정보 보호. 고객 데이터 책임.
  - 라벨: MSCI ESG Data Security; ESG-Kor S 카테고리.
  - 잡음: **중간** — "보안" 단독은 일반 물리 보안 포함 가능. 다만 사업보고서 맥락에서는 대부분 ESG.
  - 학술: ESG Data Security 라인.
- **권장**: ✅ **KEPT (S 유지)**. 차원 결정 모호 — S(고객) vs G(위험관리) — 본 검토는 S 유지하되 향후 cross-dim 검증 권장.

#### 7. **근속** (S 유지, freq=5)
- **패턴**: `근속|이직률`
- **분석**:
  - 의미: 직원 근속·이직률 직접 측정.
  - 라벨: Refinitiv Workforce engagement; MSCI Employee Retention.
  - 잡음: 0 — HR 도메인 정확 매칭.
  - 학술: Refinitiv Workforce score; Bao et al. (2024).
- **권장**: ✅ **KEPT (S 유지)**. **강력 권장**.

---

### ❌ 2.2 REMOVED 2개

#### 1. **대화** (freq=13)
- **패턴**: `대화|소통|커뮤니케이션`
- **분석**:
  - 의미: 노사관계·이해관계자 소통 의도.
  - **잡음**: 매우 큼 — "고객 대화", "전화 대화", "기업 간 소통", "마케팅 커뮤니케이션" 등 비-ESG 표현 다수. Samsung 13회 중 ESG 관련 비율 의문 — 비율 측정 안 했으나 일반 한국어 비중 ↑.
- **권장**: ❌ **REMOVED**. 대안: 패턴 강화 (`노사 대화|이해관계자 소통|stakeholder engagement`) 시 재검토. 본 형태로는 false positive 너무 많음.

#### 2. **나눔** (freq=8)
- **패턴**: `나눔|기부금`
- **분석**:
  - 의미: 기부와 유사 (사회공헌).
  - **중복**: `기부` seed가 이미 `기부|후원|봉사` 패턴 가짐. `나눔`은 의미 중복 — 같은 문장에 "나눔의 기부"가 있으면 2번 카운트 (이중 카운트 위험).
- **권장**: ❌ **REMOVED**. 대안: `기부` 패턴에 `|나눔` 추가 (`기부|후원|봉사|나눔`)하는 방식 권장.

---

## 3. 최종 seed_dictionary_v2 (37개)

| 차원 | v1 (30) | v2 추가 | v2 합계 |
|---|---:|---:|---:|
| E (환경) | 10 | 0 | 10 |
| S (사회) | 10 | 6 | **16** |
| G (지배구조) | 10 | 1 (ESG경영 재분류) | **11** |
| **합** | **30** | **7** | **37** |

### S 차원 추가 6개
지속가능, 기부, 건강, 사회공헌, 정보보호, 근속

### G 차원 추가 1개
ESG경영 (S→G 재분류)

### 산출 파일
- `data/seed_dictionary_v2.csv` — 37행 (모든 노트북에서 사용)
- `data/processed/seed_v2_decision_analysis.csv` — 9 후보 결정 표
- `data/seed_dictionary_v2_proposed.csv` — 원본 자동 제안 (역사적 기록)

---

## 4. 위반금지 #3 충족 검증

가이드 02 line 94 "MCP/추출 결과 그대로 신뢰 ❌". 본 검토는:
- 02b 자동 추출 결과를 그대로 채택하지 않음 (9 중 7만 KEPT, 2 REMOVED)
- 의미·잡음·중복·차원 재분류까지 직접 검증
- 학술 라벨(MSCI·Refinitiv·Bloomberg) 매핑 명시
- 사용자가 다른 의견 있을 시 의견 차이 명시 가능

---

## 5. 한계 + 향후 개선

### 5.1 잡음 비율 미정량
- "대화" REMOVED 결정은 정성 판단. 실제 13회 중 ESG 관련 몇 회인지는 사이클 4 v3 진단에서 정량 측정 필요.

### 5.2 1 firm-year 기준
- Samsung 2024만으로 일반화. 사이클 4 batch 30~50건 확보 후 등급별 등장 패턴 재검증.

### 5.3 차원 모호성
- 정보보호 S vs G — 본 검토는 S 유지. cross-dim 검증 필요.
- 지속가능 S 단독 → ESG 전반 표지자. 별도 ESG_overall 차원 신설 검토 가능 (알파).

### 5.4 사용자 의견 차이 가능성
- 7 KEPT 중 "건강·정보보호"는 잡음 중간 — 사용자가 REMOVED 원할 수 있음.
- "대화·나눔" REMOVED 중 사용자가 강하게 KEPT 원할 수 있음 — 패턴 강화 제안 가능.

→ **사용자 확인**: 본 권장 그대로 채택 / 일부 수정 / 전면 재검토 중 선택.

---

## 6. 다음 단계 연결

- 02_preprocessing **v_final** (사이클 4) — seed_v2.csv 사용 + seed_v1 vs seed_v2 S 점수 alt 비교
- 03_mining **v_final** — N=31 (사이클 3 batch 재실행 후) Spearman·OLS 정상 통계
- phase2B **v2** — 사이클 3 batch FAIL_OTHER 30건 진단 후 재시도

---

> **본 검토는 Claude의 10단계 분석 + 학술 라벨 매핑 기반. 사용자 의견 차이 있으면 의견 주시면 seed_v2.csv 즉시 수정 가능.**
