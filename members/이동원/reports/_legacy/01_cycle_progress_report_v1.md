# ESG DART 풀 사이클 v1·v2 1차 단계별 진행 보고서

> **작성자**: 이동원
> **작성일**: 2026-05-18
> **버전**: v1 (사이클 2 Run All 완료 시점)
> **보고서 형식**: 가이드 04 §1 (.md) + §2 (데이터·방법·결과·한계 순)
> **본 보고서 위치**: `members/이동원/reports/01_cycle_progress_report_v1.md`
> **상위 진단 HTML**: `01_collection/03_phase2A_diagnosis_v1.html` (사이클 1), `01_collection/04_phase2A_diagnosis_v2.html` (사이클 2/3)

---

## 0. 한 줄 요약

가천대 비정형데이터분석 기말 프로젝트로 DART 사업보고서 ESG 언어와 KCGS 등급의 연관성을 분석. 사이클 2 종료 시점에 Samsung 2024 1 firm-year 풀 파이프(수집 → 전처리 → 마이닝) 코드·표·시각화 완성. 그러나 **N=1이라 Spearman ρ·t-test 모두 NaN**으로 통계 의미 없음. 사이클 3 batch 30건 stratified가 즉시 해결.

---

## 1. 데이터

### 1.1 모집단·표본
- **모집단**: `data/company_master.csv` — 127 unique stock_code × 3 fiscal_year (2022·2023·2024) = **381 firm-year** (가이드 02 line 117)
- **타이밍 규칙**: `esg_year = fiscal_year + 1` (가이드 02 line 37-38)
- **현재 표본 (사이클 2 종료)**: 005930 × 2024 = **1 firm-year** (Samsung)
- **계획 표본 (사이클 3)**: KCGS 등급별 stratified 5건 × 7등급 ≈ 30 firm-year (Samsung 제외)

### 1.2 데이터 출처·획득
- **DART 사업보고서**: OpenDART `document.xml` API → raw zip → lxml SECTION-1 14 노드 직접 순회
- **KCGS ESG 등급**: company_master.csv (esg_grade·e/s/g_grade) — `logs/kcgs_lineage.csv`에 출처 메타 (URL·as_of_date·method_url) 별도 보존
- **교차검증**: KRX ESG 포털(`esg.krx.co.kr`)에서 Samsung 2024 등급 수동 확인 절차 안내 (00_ingest Step 5)

### 1.3 식별자 정합성 (위반금지 #7 silent 오매칭)
- **stock_code** 기준 (회사명 X). company_name 133개 ≠ stock_code 127개 차이 사전 인지.
- **dtype 보존**: 모든 read/write에 `dtype={'stock_code': str}` + `str.zfill(6)` 강제 (사이클 2 Fix B).
- **Samsung 005930** → corp_code `00126380` → rcept_no `20250311001085` 매핑, viewer 5/5 확인.

### 1.4 수집 성공·실패 처리 (위반금지 #1)
- `logs/collection_log.csv` — SUCCESS/FAIL_*/WARN_* status + reason 컬럼.
- 실패 행은 `data/processed/esg_features_v2.parquet` join에서 제외 → 가짜 0 채우기 차단.
- Samsung 2024: status=SUCCESS, n_passages_body=55, viewer 5/5 사용자 확인 완료.

---

## 2. 방법

### 2.1 수집 (01_collection_phase2A_v2.ipynb, 29 cells)

| Step | What | 가이드 매핑 |
|---|---|---|
| 1 | `.env` API key 마스킹 + 후보 리스트 매칭 | line 216-222 |
| 2 | company_master 행수·unique·연도 검증 | line 117 |
| 3 | stock_code → corp_code (corpCode.xml 캐시) | line 153 |
| 4 | corp_code → rcept_no (PRIMARY_BIZ → CORR_BIZ → ANY_BIZ_2024 fallback 3단) | line 154 |
| 5 | document.xml ZIP raw 보존 + DOCUMENT-NAME 분류 (사업보고서·연결감사·감사) | line 155 |
| 6 | `<SECTION-1>` 14 노드 lxml 순회 + section_code (020000·040000·060000) + TITLE/AASSOCNOTE 이중 매칭 + 본문/표 분리 | line 156-157 |
| 7 | seed 30 단어 정규식 매칭 → body passage 추출 | line 158 |
| 8 | viewer 5 sample 사용자 확인 절차 | line 67 |
| 9 | collection_log dedup + run_id 컬럼 (벤치마킹 5번 arXiv 2208.01712) | line 69 |
| 10 | 위반금지 8항목 self-check 표 | 04 §2-1 |

### 2.2 KCGS lineage (00_ingest_kcgs_v1.ipynb, 15 cells)
- 등급 분포 분석 (S·A+·A·B+·B·C·D × 2023·2024·2025)
- stratified sampling 가능성 평가 (등급별 5건 충족 여부)
- `logs/kcgs_lineage.csv` 생성 (출처 URL·as_of_date·evaluation_method 컬럼)
- KRX 교차검증 수동 절차 안내 (Fix C dynamic 출력: 사용자 실제 데이터 등급 표시)

### 2.3 전처리·feature (02_preprocessing_v2.ipynb, 15 cells)
- **Q1 분석 단위**: source='body', sections=II·IV·VI, dimensions=E·S·G
- **Q2 형태소 분석기**: Okt PRIMARY (Mecab 미설치 Windows 환경. 보고서 §한계 명시)
- **Q3 expanded**: 본 v2 범위 외 — N≥30 확보 후 진행 (진단 Step 6 권장)
- **TF-IDF**: `TfidfVectorizer(min_df=1, max_df=1.0, token_pattern=r'\b\w+\b', lowercase=False)`
- **seed score**: 가이드 03 line 76-88 공식 그대로. `seed_tfidf_E·S·G = Σ TF-IDF(term) for term in seed`
- **cosine similarity**: 가이드 03 line 211-215 기준 문장 3개 vs firm-year body TF-IDF.

### 2.4 S 점수 진단 (02b_s_score_diagnosis_v1.ipynb, 15 cells, 사이클 2 신설)
- **가설**: H1 seed_S 10단어가 body에 거의 안 등장, H2 누락 어휘(복리후생·다양성·정보보호) 다수, H3 II/IV/VI 구조적으로 S 비중 낮음.
- **검증**: 정규식 빈도 직접 카운트 → section × dim cross tab → seed_dictionary_v2_proposed.csv 자동 생성 (5회 이상 등장 후보)

### 2.5 마이닝 (03_mining_v1.ipynb, 15 cells)
- **Spearman ρ + p-value**: 9개 (feature, grade) 쌍
- **t-test + Mann-Whitney**: 상위/하위 등급 그룹 평균 차이
- **OLS baseline**: `esg_grade_num = β0 + β1·seed_tfidf_X + β2·word_count + ε`
- **cheap-talk 통제**: word_count (가이드 03 line 234) + specificity_score (alpha, 벤치마킹 4번 ClimateBert)
- **모형 선택 근거 표**: OLS·ordered_logit·binary_logit 비교

### 2.6 v3 batch 계획 (01_collection_phase2B_v1.ipynb, 15 cells, 사이클 3 신설)
- KCGS 등급별 stratified 5건 × 7등급 = 약 30 firm-year (S 등급 부족 시 가용 전체)
- try/except 격리 + status 11종 + reason — 위반금지 #1 보장
- random 3건 viewer 검증 — 위반금지 #2·#3
- 평가 기준 SUCCESS ≥ 80% 명시 (위반금지 #8)

---

## 3. 결과 (사이클 2 종료 시점)

### 3.1 수집 결과 (Samsung 2024)
| 항목 | 값 |
|---|---|
| stock_code | 005930 |
| corp_code | 00126380 |
| rcept_no | 20250311001085 (PRIMARY_BIZ fallback) |
| viewer | https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20250311001085 |
| SECTION-1 노드 | 14 / 14 매칭 |
| n_passages_body | 55건 (II=24, IV=1, VI=30) |
| n_passages_tables | 84건 (G에 집중) |

**SECTION-1 매칭 method 분포 (Samsung 2024 검증)**:
- AASSOCNOTE 매칭: I·II·III·IV·V·VII·IX·X·XI (9개)
- TITLE_text 매칭: VI·VIII·I (TITLE 보조)
- no_match: 표지·전문가확인 등 SECTION-1 비ESG 노드 (4개)

### 3.2 전처리·feature 결과 (Samsung 2024, 1행)

| feature | 값 | 비고 |
|---|---:|---|
| seed_tfidf_E | 0.051 | 중간 수준 |
| **seed_tfidf_S** | **0.010** | **E의 1/5, G의 1/35 — KCGS s_grade=A+와 큰 격차** |
| seed_tfidf_G | 0.359 | VI 거버넌스 절 영향 |
| cosine_E | 0.037 | 기준 문장 vs body |
| cosine_S | 0.040 | seed_tfidf보다 균등 |
| cosine_G | 0.168 | |
| word_count | 12,159 | cheap-talk 통제 |
| specificity_score | (alpha) | 숫자/연도/단위 비율 |

**토큰화 결과 (Okt)**: 평균 9,274 토큰 / 2,069 vocab (Samsung 1건 기준).

### 3.3 KCGS 등급 분포 (lineage, 381 행)
- 등급 분포: A·B+·A+ 가 다수 (전체의 약 65%). S·D 등급은 적음.
- stratified 5건 가능성: A·B+·A+ 등급은 충분, S·D는 ≤ 5건 추정. 사이클 3 batch에서 가용 전체 사용.

### 3.4 마이닝 결과 (N=1, 가이드 04 §3 평가표 형식)

| feature | grade | n | Spearman ρ | p-value | t_stat | t_p | 판단 |
|---|---|---:|---:|---:|---:|---:|---|
| seed_tfidf_E | esg_grade_num | 1 | NaN | NaN | NaN | NaN | ⚠️ N 부족 |
| seed_tfidf_S | esg_grade_num | 1 | NaN | NaN | NaN | NaN | ⚠️ N 부족 |
| seed_tfidf_G | esg_grade_num | 1 | NaN | NaN | NaN | NaN | ⚠️ N 부족 |
| cosine_E | esg_grade_num | 1 | NaN | NaN | NaN | NaN | ⚠️ N 부족 |
| cosine_S | esg_grade_num | 1 | NaN | NaN | NaN | NaN | ⚠️ N 부족 |
| cosine_G | esg_grade_num | 1 | NaN | NaN | NaN | NaN | ⚠️ N 부족 |
| seed_tfidf_E | e_grade_num | 1 | NaN | NaN | NaN | NaN | ⚠️ N 부족 |
| seed_tfidf_S | s_grade_num | 1 | NaN | NaN | NaN | NaN | ⚠️ N 부족 |
| seed_tfidf_G | g_grade_num | 1 | NaN | NaN | NaN | NaN | ⚠️ N 부족 |

**해석 (N=1 한계)**:
- `scipy.stats.spearmanr(x, y)`는 두 벡터의 길이 ≥ 3이어야 통계 정의. N=1은 단일 점이라 순위 정의 불가 → NaN.
- t-test·Mann-Whitney도 그룹별 ≥ 2 표본 필요. N=1은 그룹 분할 불가.
- OLS도 모수 추정에 자유도 부족 (요인 ≥ 2개면 N ≥ 3 필요).
- **이는 v1 본 의도의 정상 결과**. 코드·표 형식·시각화 형식 검증 완료, 통계 추정은 사이클 3 N≥30 이후.

### 3.5 사이클 2 발견 5종 (사용자 Run All 결과 분석)

1. **한글 폰트 missing** → 시각화 PNG 한글 깨짐 → **Fix A (matplotlib font_manager 자동 detect 셀)** 6 노트북 적용
2. **stock_code int 변환** (`5930` → 위반금지 #7 위험) → **Fix B (dtype=str + zfill(6) 강제)** 6 노트북 적용
3. **collection_log v2 행 부재** → Step 9 dedup 후 미보강 의심 → **Fix D (진단 + 강제 보강 셀)** 01_collection 추가
4. **S 점수 비정상 낮음** (seed_tfidf_S=0.010 vs s_grade=A+) → **02b_s_score_diagnosis_v1.ipynb 신설** (3가설 정량 검증 + seed_v2 제안)
5. **KCGS Step 5 메모 하드코딩** → **Fix C (dynamic 출력)** 00_ingest 적용
6. **Bonus**: Run All 후 .ipynb truncated → **Fix E** (`display(df) → print(to_string())` + `pd.set_option` 제한)

---

## 4. 한계

### 4.1 표본 한계
- **N=1 (Samsung 2024)** — 모든 통계 추정 NaN. 본 v1은 코드·표·시각화 형식 검증용. **사이클 3 batch 30건이 즉시 해결**.
- Samsung은 KCGS A 등급 + 시가총액 1위 대표성 ↑이지만 단일 기업이라 산업 분포·등급 분포 모두 0. 표본 대표성 단정 불가.

### 4.2 형태소 분석기 한계
- Windows 환경 Mecab 미설치 → **Okt fallback**. 정형 사업보고서 문어체에서 Mecab 대비 분리도·속도 ↓. 본 보고서 §한계로 기록 필요.
- 대안 비교 셀(kkma·komoran)이 02_preprocessing_v2에 가용성 확인까지만. 본격 alt sweep은 v3에서.

### 4.3 seed dictionary 한계
- **seed_S 10단어가 Samsung II/IV body에 거의 안 등장** (진단 노트북 H1 잠정 지지) → seed 재설계 필요.
- expanded dictionary 채택은 N≥30 corpus 확보 후 (사이클 1 진단 Step 6).

### 4.4 표 vs 본문 한계
- VI 80% 표 비중 — 본 v2는 body only 사용. tables alt 분석은 v3에서.

### 4.5 KCGS 등급 한계
- `as_of_date='2026-05-15'` 추정 (company_master 시드 작성 일자). 정확한 KCGS 평가 결과 발표일 미확정.
- 정정공시 이력 미반영. KRX 교차검증 절차만 안내. 사용자 수동 확인 권장.

### 4.6 cheap-talk 한계
- 본 v1은 word_count + specificity_score 2종. ClimateBert 기준의 commitment ratio·non-material share는 alpha+ 영역.

### 4.7 인과 vs 연관
- 가이드 04 line 99-111 (해석 주의): 본 분석은 인과관계 식별 ❌, 연관성만 ⭕. 모형 결과는 모두 "이 표본에서 ~ 경향이 있었다" 형식으로 조심스럽게 해석.

---

## 5. 산출물 인덱스

### 5.1 노트북 6종 (members/이동원/notebooks/)
| 노트북 | cells | size | 역할 |
|---|---:|---:|---|
| 00_ingest/00_ingest_kcgs_v1.ipynb | 15 | 21KB | KCGS lineage 생성 + 등급 분포 + 교차검증 안내 |
| 01_collection/01_collection_phase2A_v2.ipynb | 29 | 57KB | Samsung 1건 안정 Run All (Steps 1-10 + Fix D 진단) |
| 01_collection/01_collection_phase2B_v1.ipynb | 15 | 33KB | (사이클 3) batch 30건 stratified |
| 02_preprocessing/02_preprocessing_v2.ipynb | 15 | 26KB | seed-only TF-IDF + cosine + cheap-talk control |
| 02_preprocessing/02b_s_score_diagnosis_v1.ipynb | 15 | 22KB | S 점수 H1/H2/H3 정량 진단 + seed_v2_proposed |
| 03_mining/03_mining_v1.ipynb | 15 | 25KB | Spearman·t-test·OLS 코드 형식 + specificity alpha |

### 5.2 로그·산출 (logs/·data/processed/)
| 파일 | 내용 |
|---|---|
| logs/collection_log.csv | firm-year × 29 컬럼 (status·reason·section size·run_id 등) |
| logs/kcgs_lineage.csv | 381행 × KCGS 등급 + source URL + as_of_date |
| logs/kcgs_lineage_meta.json | 출처 메타·교차검증 절차 |
| logs/correction_log.csv | 정정공시 fallback 후보 기록 (가이드 02 line 69) |
| logs/section_match_v_final.csv | SECTION-1 14 매칭 method·문자수·table_ratio |
| data/processed/esg_features_v2.parquet/xlsx | Samsung 1행 × 20 컬럼 |
| data/processed/seed_dictionary_v2_proposed.csv | (사이클 2 진단 후) S 확장 후보 |
| data/processed/fig_v1_kcgs_grade_distribution.png | 등급 × 연도 분포 |
| data/processed/fig_v2_preprocess_scores.png | seed_tfidf·cosine E/S/G bar |
| data/processed/fig_v1_mining_cheaptalk.png | word_count·specificity bar |
| data/processed/regression_results_v1.csv | placeholder (N=1 NaN) |

### 5.3 진단 보고서 (members/이동원/reports/)
| 파일 | 의미 |
|---|---|
| 01_collection/03_phase2A_diagnosis_10steps_v1.html | 사이클 1 진단 (6 tab — 10단계·위반·벤치마킹·로드맵·폴더) |
| 01_collection/04_phase2A_diagnosis_10steps_v2.html | 사이클 2/3 통합 (6 tab — 새 발견 5개·S 진단·batch·D-Day 액션) |
| 01_cycle_progress_report_v1.md | 본 1차 보고서 |

---

## 6. 다음 단계 (사이클 3·4 액션)

### 6.1 사용자 즉시 액션 (D-1)
1. 6 노트북 재실행 — 사이클 2 fix 검증
2. 02b_s_score_diagnosis_v1 실행 → seed_dictionary_v2_proposed.csv 검토 → 채택
3. 01_collection_phase2B_v1 Run All — batch 30건 (5~10분)
4. 02·03 재실행 (N=31 정상 통계)
5. random 3건 viewer 확인 (위반금지 #3)

### 6.2 Claude 액션 (사용자 batch 결과 공유 후)
1. 02_preprocessing_v3 — seed_v2 적용 + Okt/Kkma/Komoran alt sweep
2. 03_mining_v2 — N=31 Spearman·OLS·ordered_logit 비교
3. release notes 5종 (00·01a·01b·02·03)
4. GitHub MCP 양쪽 레포 PR 분할
5. 최종 보고서 .md (본 보고서 v2)

### 6.3 알파 분석 후보
- specificity_score (commitment vs non-commitment 비율) 정교화 — 벤치마킹 4번 ClimateBert
- section-weighted score (II=0.5·IV=0.2·VI=0.3) alt 분석
- 업종별 결과 분해 (가이드 04 §3-1 알파 예시)
- 보조 보고서(연결감사·감사) 흡수 alt 비교

---

## 7. 위반금지 8항목 + 가이드 04 §2-1 자가 점검

| # | 위반금지 | 사이클 2 종료 시점 |
|---|---|---|
| 1 | 실패 행 가짜 0 ❌ | ✅ status/reason + dedup + SUCCESS만 join |
| 2 | viewer 우회 ❌ | ✅ document.xml API only + 5 sample 확인 |
| 3 | MCP/추출 그대로 신뢰 ❌ | ✅ Python re + viewer 확인 + seed 직접 검증 (02b) |
| 4 | API key 출력 노출 ❌ | ✅ mask_key + KEY_CANDIDATES |
| 5 | raw 미보존 ❌ | ✅ data/raw/*.zip + interim/sections.json |
| 6 | 진단 부재 ❌ | ✅ SECTION 매칭 표·collection_log·section_match.csv |
| 7 | silent 오매칭 ❌ | ✅ stock_code dtype=str + zfill(6) (Fix B) |
| 8 | 평가 기준 부재 ❌ | ✅ viewer 5/5 + self-check 표 + SUCCESS≥80% (사이클 3) |

가이드 04 §2-1 데이터 lineage·재현성·보고서 판단 모두 사이클 3 batch 후 100% 충족 예상.

---

> **본 보고서는 사이클 2 종료 시점의 1차 정리이며, 사이클 3 batch 결과 + 10단계 분석 v3 + 해결 방법 로드맵은 후속 문서로 분리 작성한다.**
