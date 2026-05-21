# 팀 작업물 1차 비교·진단 보고서 (회의 토론용)

> **버전**: v0.1 (rev 2026-05-19 — 김지우 반영) · **분석 단계**: 데이터 수집 ↔ 전처리 ↔ 마이닝
> **분석 대상**: 이동원(00→01→02→03 풀파이프) · 신지영(전처리) · 김혜성(수집+전처리) · 김지우(풀파이프+검정+회귀)
> **참고 자료**: `docs/professor_md/01~04`, `docs/supplements/versions/v0.2~v0.4`
> **본 보고서는 회의 토론용 1차 진단입니다.** 회의 결정에 따라 v0.2부터 통합 ipynb를 구성합니다.

---

## TL;DR — 회의에서 가장 먼저 합의해야 할 4가지

⚠️ **김지우 작업물이 학기 본 결론을 흔드는 핵심 발견을 포함합니다.** 회의의 첫 안건이어야 합니다.

**1. 부호 역전 발견 (가장 중요)**

| 분석자 | 표본 | 측정 | Spearman ρ | p-value |
|---|---|---|---|---|
| 이동원 | N=29 (KCGS stratified pilot) | seed_tfidf_E ↔ esg_grade | **+0.606** | 0.0005 ⭐⭐ |
| 김지우 | N=30 (KOSPI 상위 10×3) | g_signal_ratio ↔ kcgs_grade | **+0.444** | <0.05 ⭐ |
| 김지우 | **N=210 (77 firm × 3)** | g_signal_ratio ↔ kcgs_grade | **-0.197** | 0.004 ⭐⭐ |
| 김지우 | N=210 | esg_tfidf_concentration ↔ kcgs_grade | **-0.185** | 0.007 ⭐⭐ |
| 김지우 | N=210 | total_tokens ↔ kcgs_grade | **+0.263** | <0.001 ⭐⭐⭐ |

⭐ **김지우는 파일럿(n=30)에서 양의 상관이 전체(n=210)에서 음의 상관으로 역전됨을 직접 관측했고, 그 원인을 "KOSPI 상위 10개 대형주 표집 편의(spurious positive correlation)"로 진단했습니다.** 이동원의 N=29 ρ=+0.606도 KCGS stratified pilot이므로 동일한 표집 편의 위험에 노출되어 있습니다. 통합 corpus에서 재실행 시 어느 쪽으로 수렴하는지가 본 학기 핵심 결과.

다만 두 사람의 **측정 단위가 다릅니다** — 이동원의 `seed_tfidf_E`(환경 차원, 단어 TF-IDF 합)와 김지우의 `g_signal_ratio`(거버넌스 차원, 토큰 분류 비율). 같은 차원·같은 메트릭으로 통합 N=381 재실행 후 부호를 확정해야 합니다. **이는 회의 최우선 결정 사항**.

**2. 통합 corpus 채택 기준** — 김혜성 381/381(SUCCESS 100%) · 신지영 365/381(95.8%) · 김지우 210/213(stratified 77×3) · 이동원 29/30(pilot). 가이드 04 §2-1 "최대 381행 시도" 원칙에 가장 정직한 것은 김혜성 381건. 단 **김지우의 stratified 77개 기업 선정 로직**이 표집 편의를 줄이는 데 더 합리적일 수 있으므로 합의 필요.

**3. seed/사전 보존 전략** — 김혜성 `kiwi.add_user_word(score=50)` 30/30 보존 ⭐ · 신지영 사용자 사전 미등록 11/30 손실 · 김지우 **Taxonomy 사전(G_SIGNAL 13 + ESG_SIGNAL 31 + BOILERPLATE 27)으로 토큰 분류 기반 메트릭** 도입. 김지우 방식은 가이드 03 §2단계의 seed TF-IDF와 다른 패러다임 — `g_signal_ratio` = (G_SIGNAL 토큰 수) / (전체 토큰 수). 통합 시 **두 메트릭(seed TF-IDF + signal ratio) 병행 보고** 권장.

**4. 회귀 모형 + robustness check 통합** — 김지우의 **3종 전처리 실험(exp_B/E/F) robustness check**, **Bootstrap 95% CI**, **Mann-Whitney U**가 가이드 04 §3 "측정 validity" 평가표에 가장 완벽하게 부합. 통합 03 노트북에 그대로 채택 권장.

---

## 1. 분석 프레임 — 10단계 비교 기준

본 비교는 가이드 04 §3 평가표(데이터이해·DART lineage·텍스트처리·측정validity·모형선택·해석한계·알파) 7개 영역을 작업 흐름 순서로 풀어 **10단계 진단 프레임**으로 재구성한 결과입니다.

| # | 진단 단계 | 가이드 매핑 |
|---|---|---|
| 1 | 표본 단위 · 식별자 정규화 | 02 §"먼저 이해할 세 가지 식별자" / Fix B `zfill(6)` |
| 2 | corp_code · rcept_no 매핑 lineage | 02 §"전체 분석 흐름" 1~2 |
| 3 | XML 다운로드 · 파싱 robustness | 02 §"전체 분석 흐름" 3~4 |
| 4 | 섹션(II·IV·VI) 추출 전략 | 02 §"MCP로 ESG 문단 추출" / 03 §1단계 |
| 5 | ESG passage 후보 정의 | 03 §1단계 |
| 6 | 형태소 분석기 + seed 보존 | 02 §"전체 분석 흐름" 7 |
| 7 | 불용어 사전 정의 + 문장 필터 | 03 §2단계 stopwords_ko_esg.txt |
| 8 | seed 빈도 진단 · expanded 근거 | 03 §2단계, line 90~122 |
| 9 | TF-IDF · cosine · signal_ratio feature | 03 §2~4단계 |
| 10 | 회귀 + Spearman/MWU/Bootstrap + 알파 | 03 §3~5단계, 04 §3-1 |

---

## 2. 작업물 한눈에 보기

| 항목 | 이동원 | 신지영 | 김혜성 | 김지우 |
|---|---|---|---|---|
| **노트북 수** | 4개 (00·01·02·03) | 1개 병합형 | 1개 병합형 | **1개 메가형 (129 cells)** |
| **셀 수** | 17/13/15/13 = 58 | 36 | 56 | **129 (MD 69 + CODE 60)** |
| **수집 표본** | batch 30 pilot | 381 시도 | 381 시도 | **77 기업 stratified × 3 = 213 firm-year** |
| **수집 SUCCESS율** | 28/30 (93.3%) | 365/381 (95.8%) | **381/381 (100%)** | 243건 수집 → KCGS join 후 **210 firm-year (98%)** |
| **재수집·복구** | Fix F (recover XML) | — | 13건 진단 → 재수집 v2 | 신규상장 firm 2개 결측 인정 (가짜 0 ❌) |
| **XML 파서** | lxml recover=True + 정규식 | BS4 lxml (XMLParsedAsHTMLWarning) | lxml ElementTree | (모듈화 — `src/passage_filter.py`) |
| **형태소 분석기** | Okt PRIMARY | Kiwi | Kiwi 0.23.1 + user dict | (다중 실험 — 분석기 추정 Kiwi 계열) |
| **사용자 사전 / 토큰 정책** | TfidfVectorizer `\b\w+\b` | ❌ 미등록 → seed 11개 손실 | ✅ NNP score=50 → 30/30 보존 | **Taxonomy 사전 + 회사명 4변형 제거 + 문장 패턴 18종** |
| **불용어 단계** | max_df=0.95 자동 | 216개 | 회사명 1자/2자 분리 | **standard/extended 두 단계 + sentence-level filter** |
| **passage / document** | sections.json 29 | passage 13,610 → doc 365 | corpus 381 | firm_year_documents 243 |
| **TF-IDF feature** | seed_tfidf + expanded_tfidf 9개 | 미실행 | 미실행 | **g_signal_ratio · esg_tfidf_concentration · esg_signal_ratio · total_tokens · bp_contamination_rate** |
| **3종 전처리 실험** | — | — | — | **exp_B / exp_E / exp_F robustness check** ⭐ |
| **Bootstrap CI** | — | — | — | **95% CI 명시** ⭐ |
| **Mann-Whitney U** | — | — | — | **고등급 vs 저등급** ⭐ |
| **회귀** | OLS · OrderedLogit · BinaryLogit | — | — | **OLS + Ordered Logit (kcgs ~ g_signal + log_tokens)** |
| **핵심 발견** | **ρ=+0.606 E↔ESG (N=29)** ⭐ | seed 11개 손실 발견 | 5개 희소 seed → expanded 근거 | **⭐ 부호 역전: N=30→N=210, ρ=+0.444→-0.197** |
| **알파** | 업종별 분해 시도 (N≥3 1업종) | — | 핵심 발견 마크다운 | **cheap-talk 해석 + 9개 시행착오 기록 + Precision/Recall trade-off** |
| **Decision Box 형식** | 부분 | — | — | **✅ Alternative/Choice/Justification/Limitation 완전 적용** ⭐ |
| **위반금지 충족** | 8/8 (v_final) | (명시 안 됨) | 명시적 충족 | 신규상장 결측 가짜 0 ❌ 명시 |

---

## 3. 단계별 진단 — 누가 무엇을 잘했고 무엇이 미흡한가

### 3.1 표본 단위 · 식별자 정규화 (단계 1)

네 명 모두 `stock_code.zfill(6)` (Fix B)를 적용. 다만 **표본 모수가 갈립니다**.

- 이동원: KCGS stratified 5×7=30 (S 등급 0건이라 30 시도)
- 신지영: company_master.csv 전체 381 시도
- 김혜성: company_master.csv 전체 381 시도
- 김지우: **별도 stratified 추출 77개 기업** × 3 = 213 → KCGS inner join 후 210

김지우의 77개 stratified가 가이드 02 §"company_master.csv 기준 최대 127개 기업"과 차이가 있으므로 회의에서 **김지우의 표본 선정 기준을 공유**받고 통합 corpus 결정에 반영해야 합니다.

### 3.2 corp_code · rcept_no 매핑 lineage (단계 2)

김혜성의 `find_business_report_v2`(비12월 결산 유연 + 정정 회피)가 가장 robust. 김지우는 모듈화된 `collected_reports.csv` + corp_code_map.csv 구조 — 외부 모듈 의존이지만 lineage 자체는 분명합니다. 김지우 셀 5에서 "3,965건 전체 DART 매핑 중 stratified 81개만 사용" 명시.

### 3.3 XML 다운로드 · 파싱 robustness (단계 3)

이동원의 Fix F + 김혜성의 lxml ElementTree가 가장 robust. 신지영의 BS4 lxml HTML 파서는 권장 사항 위반. 김지우는 `src/passage_filter.py` 외부 모듈화 — 노트북에서 직접 보이지 않으나 통합 시 모듈 자체 검토 필요.

### 3.4 섹션(II·IV·VI) 추출 전략 (단계 4)

김혜성의 `section_chars_*` 로깅이 가장 알파 분석에 유리. 김지우는 firm_year_documents.csv 단계에서 이미 섹션 처리 완료된 형태로 로드 — passage_filter 모듈에 흐름이 캡슐화. 신지영은 섹션 분리 없이 전체 텍스트에서 seed 매칭.

### 3.5 ESG passage 후보 정의 (단계 5)

김지우는 **`sentence_density_filter`** 함수로 sentence-level density 계산 (esg_density, signal_density, generic_density, finance_density) — 가장 정교한 정의. 셀 30 예시: "주 관련 자세한 사항은 'VII. 주주에 관한 사항'을 참조하시기 바랍니다." → esg_density 2.381 계산. 이는 가이드 03 §1 Decision box "sentence-level + 가중치"의 가장 충실한 구현.

### 3.6 형태소 분석기 + seed 보존 (단계 6) ⭐

김혜성의 30/30 보존 + 김지우의 G_SIGNAL/ESG_SIGNAL/BOILERPLATE 색상 분류 + 사라진/새로 등장 토큰 추적 (셀 45)이 가장 진단력 높음. 김지우는 셀 39에서 G_SIGNAL 13개 토큰별 보존 상태를 3개 실험 모두에서 빨강/녹색 셀로 색상 분류, "G_SIGNAL 5종이 본문에 거의 안 나옴" 발견 → "보호 정책 실패가 아니라 사업보고서가 KCGS G 항목을 거의 언급하지 않는다는 발견으로 기록" (셀 67).

신지영의 11개 seed 손실은 김지우의 Taxonomy 분류 방식으로 우회 가능하나, 통합 시 **김혜성의 user dict + 김지우의 Taxonomy** 결합이 가장 robust.

### 3.7 불용어 사전 정의 + 문장 필터 (단계 7)

김지우의 **3단계 실험 설계**가 가장 정교:
- **exp_B (baseline)**: standard 불용어, 숫자 모두 제거, 문장 필터 ❌
- **exp_E**: extended 불용어, 숫자 모두 제거, **문장 필터 18개 패턴** → BP% 13.3% → 0%
- **exp_F**: extended 불용어, **수치 보존(keep_quantity)**, 문장 필터 18개 → **ESG 정량 약속 보존**

세 실험 모두 동일 부호·비슷한 ρ → **robustness 확인**. 통합 02 노트북에 그대로 채택 권장.

### 3.8 seed 빈도 진단 · expanded dictionary 근거 (단계 8)

김혜성의 5개 희소 seed 발견 + 김지우의 G_SIGNAL 5종 본문 부재 발견이 상호 보완적. 김지우 셀 45는 `exp_B → exp_E top-50` 사라진/새로 등장 토큰을 G_SIGNAL/ESG_SIGNAL/BOILERPLATE로 분류, "boilerplate를 비운 자리를 실제 ESG 신호가 채웠다" 검증 (셀 63).

### 3.9 TF-IDF · cosine · signal_ratio feature 생성 (단계 9)

이동원과 김지우가 도달했으며 **feature 패러다임이 다릅니다**:

- **이동원** (가이드 03 line 90-122 충실): `seed_tfidf` + `expanded_tfidf` × E·S·G 차원 = 6개 + cosine × 3 = 9 feature
- **김지우** (Taxonomy 기반 ratio): `g_signal_ratio`, `esg_tfidf_concentration`, `esg_signal_ratio`, `total_tokens`, `bp_contamination_rate`, `esg_g_relative`

두 패러다임은 상호보완적입니다. 가이드 03 §2단계 line 90의 "seed dictionary는 TF-IDF matrix를 만든 뒤 관심 있는 단어 열만 고르는 기준"은 이동원 방식에 더 가깝지만, 김지우의 **signal_ratio**는 보고서 전체 토큰 대비 ESG 토큰 비중을 직관적으로 보여줍니다. 통합 시 둘 다 보고 권장.

### 3.10 회귀 + Spearman/MWU/Bootstrap + 알파 (단계 10) ⭐

**이동원의 결과 (N=29)**:
- seed_tfidf_E ↔ esg_grade: ρ=+0.606 (p=0.0005) ⭐⭐
- OLS β=7.365, p=0.029, R²=0.295 ⭐ baseline
- BinaryLogit β=41.09, p=0.075 (약한 효과)
- OrderedLogit β≈0 (N 부족 불안정)

**김지우의 결과 (N=210)**:
- g_signal_ratio ↔ kcgs_grade_7: **ρ=-0.197 (p=0.004), 95% CI [-0.326, -0.059]** ⭐⭐
- esg_tfidf_concentration ↔ kcgs_grade_7: ρ=-0.185 (p=0.007), CI [-0.311, -0.045]
- total_tokens ↔ kcgs_grade_7: **ρ=+0.263 (p<0.001)** ⭐⭐⭐ (verbosity bias)
- OLS Adj.R²=0.061, g_signal_ratio β=-1.729 (p=0.312), log_tokens β=+0.114 (p=0.145) — 다중공선성으로 개별 비유의, **F-stat p=0.0006 (전체 유의)**
- Ordered Logit β=-2.697 (p=0.464) — 방향성 일관, n=209에서 검정력 부족
- 3종 전처리(exp_B/E/F)에서 부호 일관 → robustness 확인
- 파일럿 n=30: g_signal_ratio +0.444 → 전체 n=210: -0.197 **부호 역전**

**이동원·김지우 결과 충돌 해석**:

| 요인 | 이동원 | 김지우 |
|---|---|---|
| **표본 크기** | N=29 (작음) | N=210 (큼) — 통계적으로 우위 |
| **표본 구성** | KCGS stratified pilot | 77개 stratified, 다양 업종 |
| **차원** | E (환경) | 주로 G (거버넌스) |
| **메트릭** | seed_tfidf 합 | signal_ratio (토큰 비율) |
| **결론 방향** | 공시 언어 ↔ 등급 양의 상관 | cheap-talk 가설 지지, 부호 역전 |

가능성: (a) 이동원의 N=29가 김지우 파일럿 N=30과 같은 표집 편의에 노출되었을 가능성 — 통합 N=381(또는 N=210)로 재실행하면 부호 역전이 재현될 가능성. (b) 차원·메트릭 차이로 E 신호는 양, G 신호는 음일 가능성 — 김지우의 esg_signal_ratio는 +0.093 (미미·유의 ❌). 다만 김지우의 esg_tfidf_concentration -0.185는 음의 방향이라 (b)만으로 설명은 약함.

⭐ **통합 N=381(또는 김지우 N=210) corpus에서 이동원의 seed_tfidf_E와 김지우의 g_signal_ratio·esg_tfidf_concentration·total_tokens·esg_signal_ratio를 모두 회귀에 넣어 부호와 유의성을 동시 확인하는 것이 학기 본 결과**.

---

## 4. 공통 강점 (네 명 모두 잘한 부분)

첫째, **식별자 lineage 명확** — `stock_code.zfill(6)`, `corp_code` 매핑, `rcept_no` 기록을 네 명 모두 구현. 김지우는 추가로 "회사명 merge 금지" (`docx` 표 0)를 명시.

둘째, **회사명 불용어 제거** — 네 명 모두 적용. 김혜성 1자/2자 분리, 신지영 216개 사전, 이동원 `max_df=0.95`, 김지우 4변형 사전 (`remove_company_names()`).

셋째, **timing rule(`esg_year = fiscal_year + 1`) 명시** — 네 명 모두 코드 또는 마크다운에 기록.

넷째, **API key `.env` 분리** — 가이드 04 §5 위반금지 충족.

다섯째, **재현성 장치** — 신지영 체크포인트 CSV, 김혜성 메타 CSV + corpus JSON 캐시, 이동원 incremental checkpoint, 김지우 모듈화 + `eval_comparison.csv` 산출물 분리. 모두 중간 실패 시 재실행 가능.

여섯째, **인과 vs 연관 디시플린** — 네 명 모두 가이드 04 §4 line 99 "결과는 연관성이지 인과관계가 아니다"를 보고서에 명시. 김지우의 docx §4 cheap-talk 가설 정합성 분석이 가장 정교.

---

## 5. 공통 약점 (네 명 모두 보강 필요)

첫째, **fastText 확장 미완** — 가이드 03 line 90~122 θ sweep + 상위 100단어 직접 검토 + 회사명 제외 정당화 → 네 명 모두 미실행. 김혜성 5개 희소 seed + 김지우 G_SIGNAL 5종 부재 발견을 결합하면 확장 근거가 가장 강력.

둘째, **section_weighted feature 부재** — 가이드 04 §3-1 알파 1순위. 김혜성 `section_chars_*` 로깅까지만, 점수화 미실행.

셋째, **cheap-talk 통제 정교화 부족** — 이동원 word_count + specificity 2종, 김지우 log_tokens 1종. ClimateBert 라인의 specificity + commitment + non-material 3종 도입은 알파 후보. **다만 김지우의 total_tokens +0.263★★★ 발견 자체가 cheap-talk 통제의 시급성을 입증**.

넷째, **분석기 robustness 비교 부재** — Okt vs Kiwi vs Komoran vs Kkma의 seed 보존율·TF-IDF 분포 비교 없음. 김지우의 3종 전처리 실험과 형태소 분석기 비교를 결합하면 robustness check 깊이 향상 가능.

다섯째, **표본 정의 불일치** — 이동원 30, 신지영 365, 김혜성 381, 김지우 210. 회의에서 통합 모수 합의 후 모든 분석을 단일 corpus로 재실행 필요.

여섯째, **기업·연도 고정효과 미통제** — 김지우 docx §6 한계로 명시. 패널 회귀 robustness check는 알파 후보.

---

## 6. 회의 시 토론 포인트 (우선순위 순)

회의 시간이 90~120분이라면 다음 순서를 권장합니다.

**[T+0~20분] ⭐ 부호 역전 해석 (가장 중요)**
- 이동원 N=29 ρ=+0.606 (E 차원, seed_tfidf) vs 김지우 N=210 ρ=-0.197 (G 차원, signal_ratio) 정반대 방향
- 김지우의 파일럿→전체 부호 역전 자체 관측 (n=30 +0.444 → n=210 -0.197) + 원인 진단 (상위 대형주 표집 편의)
- 이동원의 N=29도 동일 위험에 노출 → **통합 corpus에서 어느 쪽으로 수렴하는지가 학기 본 결과**
- 통합 표본에서 두 메트릭(seed_tfidf_E + g_signal_ratio + esg_tfidf_concentration + total_tokens) 동시 회귀 합의

**[T+20~35분] 통합 corpus 결정**
- 김혜성 381건 (가이드 02 §"company_master.csv 최대 381행" 가장 정직)
- 김지우 77×3=210 (stratified 다양성 우수)
- 회의에서 김지우의 stratified 기준 공유 후 결정: (a) 김혜성 381 채택, (b) 김지우 77+ 추가 기업 50개 확장, (c) 김지우 stratified 그대로 사용
- 회귀 안정성·표집 편의 trade-off

**[T+35~50분] seed/사전 보존 전략**
- 김혜성의 Kiwi + user dict (score=50) 30/30 보존을 통합 02 PRIMARY
- 김지우의 Taxonomy 사전 (G_SIGNAL 13 + ESG_SIGNAL 31 + BOILERPLATE 27)을 보조 분류로 채택
- 신지영의 11개 seed 손실 사례 공유 (왜 분리되었는지)
- 이동원의 token_pattern 방식은 §한계에 비교 결과 명시

**[T+50~65분] expanded dictionary 확장 방향**
- 김혜성의 5개 희소 seed (넷제로·산업재해·교육훈련·부패방지·컴플라이언스) + 김지우의 G_SIGNAL 5종 부재 → fastText 확장 근거
- 이동원의 manual 7개를 출발점으로 fastText 자동 확장 (θ 0.70/0.80/0.85 sweep + 상위 100단어 검토 + 회사명 제외) 합의
- 최종본을 `data/expanded_dictionary_v1.csv`로 통합

**[T+65~80분] 회귀·검정 통합**
- 김지우의 OLS + Ordered Logit + **Bootstrap 95% CI** + **Mann-Whitney U** 통합 03 노트북에 채택
- 이동원의 BinaryLogit (A 이상) 추가 후보로 보조
- 김지우의 **3종 전처리 robustness check (exp_B/E/F)**를 통합 02·03 노트북에 채택
- cheap-talk 통제 변수: log_tokens 필수 + specificity 옵션

**[T+80~95분] 알파 분석 1개 합의**
- 후보 1 — section_weighted (II/IV/VI 가중): 김혜성 section_chars 활용, 가이드 04 §3-1
- 후보 2 — 업종별 분해: N=381이면 4~6 업종 회귀 가능
- 후보 3 — 파일럿 vs 전체 부호 역전 자체를 알파로 정식화 (김지우 docx §3 핵심 발견 활용)
- 후보 4 — 기업·연도 고정효과 robustness check (김지우 §6 한계 보완)
- **후보 3이 김지우 발견을 학기 본 메시지로 끌어올릴 수 있어 가장 권장**

**[T+95~120분] 모형 선택 + D-Day 일정 분담**
- N=통합 corpus로 OLS · OrderedLogit · BinaryLogit 셋 다 비교 후 결정
- 보고서 §모형 선택 정당화 누가 작성
- 통합 01·02·03·04(알파) ipynb · 보고서 .md · 발표 슬라이드 4명 분담

---

## 7. 다음 단계 산출물 권장 (회의 후)

| 산출물 | 위치 | 통합 권장 |
|---|---|---|
| `01_collection.ipynb` | `_integrated/notebooks/` | 김혜성 v2 + 이동원 Fix F |
| `02_preprocessing.ipynb` | `_integrated/notebooks/` | 김혜성 Kiwi+user dict + 김지우 Taxonomy + 김지우 exp_B/E/F + 이동원 TF-IDF·cosine |
| `03_mining.ipynb` | `_integrated/notebooks/` | **김지우 Spearman+Bootstrap+MWU+OLS+OrderedLogit** + 이동원 BinaryLogit |
| `04_alpha.ipynb` | `_integrated/notebooks/` | 합의된 알파 (부호 역전 robustness 또는 section_weighted 또는 업종 분해) |
| `expanded_dictionary_v1.csv` | `data/` | 김혜성 진단 + 김지우 G_SIGNAL/ESG_SIGNAL/BP + fastText 확장 |
| `integration_decisions.md` | `_integrated/reports/` | 회의록 기반 채택 기록 |
| 최종 보고서 .md | `_integrated/reports/` | 5~10 페이지 (김지우 docx 형식 베이스로 추천) |

---

## 8. 부록 — 데이터 출처와 근거

- **이동원**: `notebooks/00~03/v_final/*.ipynb` + HTML 보고서 6개
- **신지영**: `신지영 0519_전처리.ipynb` (36 cells)
- **김혜성**: `김혜성 0519_전처리.ipynb` (56 cells, 수집+전처리 통합)
- **김지우**: `김지우0519_전처리.ipynb` (129 cells, 00 ingest → 01 token → 02 eval → 03 validation → 04 statistical test 통합) + `김지우_전처리.docx` (전체 표본 검증 보고서 8개 절)
- **가이드 문서**: `docs/professor_md/01~04` (교수님), `docs/supplements/versions/v0.2~v0.4` (이동원 정리)
- **분석 작성**: 2026-05-19, Claude (Cowork) · v0.1 rev 김지우 반영

본 보고서는 회의 토론용 1차 진단입니다. 회의에서 위 7개 토론 포인트의 결정 사항을 `integration_decisions.md`에 기록하고, 그 결정에 따라 v0.2 통합 작업을 시작합니다.
