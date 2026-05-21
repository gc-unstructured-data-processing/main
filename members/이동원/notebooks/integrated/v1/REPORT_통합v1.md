# ESG DART 통합 분석 보고서 (integrated v1)

> **작성**: 이동원 · **날짜**: 2026-05-21 · **노트북**: `esg_dart_integrated_v1.ipynb` (34 cells, Run All 완주·에러 0)
> **회의 결정(5/19) 반영** — 합의 사항: ① 381개 다 살리기 ② 분석기 robust 검증 후 결정 ③ seed 30개 활용
> **범위**: 수집 → 형태소 검증 → 전처리 → feature → 기본 회귀 → 알파분석 4종 (단계 세분화 폐기, 단일 노트북)

---

## 1. 데이터

분석 대상은 `company_master.csv`의 **127개 상장기업 × 3개 회계연도(2022~2024) = 381 firm-year**입니다. 종속변수는 KCGS ESG 등급(`kcgs_lineage.csv`, D=0~A+=5 숫자 변환)이며, 분석 단위는 회사명이 아니라 `stock_code × fiscal_year`입니다(위반금지 #2·#7, `stock_code.zfill(6)`).

수집은 OpenDART API로 수행했고, 결과는 다음과 같습니다.

- **수집 성공: 381/381 (100%)** — FY2022·2023·2024 각 127건 전수 성공
- 문서 분량(II+IV+VI 본문): 평균 34,167자 · 중앙값 25,520자 · 범위 4,194~186,911자
- 실패·가짜 0 행: 0건 (위반금지 #1 충족)

회의 결정 "381개 다 살리기"는 **김혜성의 `find_business_report_v2`**(결산월 무관 + 정정 우선순위: 원본 > [기재정정] > [첨부정정])와 **이동원의 `XMLParser(recover=True)`**(well-formed가 아닌 XML 복구) 결합으로 달성했습니다. 비12월 결산 기업(신영증권 3월·만호제강 6월)도 결산월 하드코딩 제거로 포착했습니다. raw ZIP은 `data/raw/`에 보존했습니다(위반금지 #5).

## 2. 방법

### 2.1 형태소 분석기 robust 검증 (회의 결정 ②)

동일 corpus 표본 15개(분량 분위수 추출, 비교는 앞 25,000자로 통일)에서 Kiwi와 Okt의 seed 30개 보존율을 비교했습니다.

| 분석기 | seed 보존 | 보존율 | 사용자 사전 |
|---|---|---|---|
| **Kiwi** | 26/30 | **87%** | `add_user_word(NNP, score=50)` — seed 강제 우선 |
| Okt | 20/30 | 67% | 미지원 (강제 불가) |

**Kiwi를 PRIMARY로 선정**했습니다. 근거는 (1) 복합명사 seed("재생에너지·탄소중립") 보존율이 Okt보다 20%p 높고, (2) `score` 기반 사용자 사전으로 seed를 강제 우선시켜 신지영 사례(미등록 시 11/30 손실)의 신호 손실을 방지하기 때문입니다.

**Komoran·Kkma 제외 근거(교수님 심층 질문 대비)**: Kkma는 형태소를 과도 세분화하고 대용량 corpus에서 문서당 수 초로 느려 381×평균 3.4만 자에 비실용적입니다. Komoran은 안정적이나 미등록어(신조어·복합명사) 처리가 약하고 사용자 사전이 단순 추가만 지원해 Kiwi의 `score` 우선권 제어가 불가능합니다. 두 분석기는 본 비교 프레임(seed 보존율·속도)으로 재현 가능하나, 위 근거로 사전 제외했습니다.

### 2.2 전처리 (회의 결정 ③)

PRIMARY(Kiwi)에 seed 30개를 `NNP score=50`으로 등록해 복합명사를 보존하고, 명사·외국어 토큰만 추출했습니다. 불용어 358개(파일 + 공시 일반어 + 회사명 1·2자 분리)를 제거하되 **seed 30개는 불용어에서 제외**했습니다.

### 2.3 Feature (두 패러다임 병행)

v0.1 비교에서 이동원 `seed_tfidf`와 김지우 `g_signal_ratio`가 다른 부호를 보였으므로, **같은 corpus에서 두 측정을 동시 산출**했습니다.

- seed/expanded TF-IDF (E·S·G), E/S/G 기준 문장 cosine similarity
- `g_signal_ratio`·`esg_signal_ratio` (토큰 비중 — 김지우 패러다임)
- `total_tokens`(cheap-talk verbosity 통제), `specificity`(숫자 토큰 비율)

### 2.4 검정·회귀

Spearman 순위상관 + **Bootstrap 95% CI**(김지우 방식), **Mann-Whitney U**(고등급 A↑ vs 저등급), OLS·Ordered Logit·Binary Logit 3종을 비교했습니다.

## 3. 결과 (실측, N=381)

### 3.1 Spearman 순위상관 (KCGS 등급 대비)

| feature | ρ | p | 95% CI | 판정 |
|---|---|---|---|---|
| total_tokens | **0.654** | <0.001 | [0.595, 0.705] | ⭐⭐⭐ 가장 강함 (verbosity) |
| cosine_S | 0.401 | <0.001 | [0.309, 0.479] | *** |
| cosine_E | 0.346 | <0.001 | [0.265, 0.432] | *** |
| seed_tfidf_E | 0.318 | <0.001 | [0.231, 0.413] | *** |
| specificity | 0.267 | <0.001 | [0.167, 0.353] | *** |
| cosine_G | 0.247 | <0.001 | [0.152, 0.342] | *** |
| seed_tfidf_G | 0.210 | <0.001 | [0.119, 0.303] | *** |
| seed_tfidf_S | 0.131 | 0.010 | [0.039, 0.228] | * |
| g_signal_ratio | -0.067 | 0.195 | [-0.166, 0.028] | 무유의 |
| esg_signal_ratio | -0.061 | 0.231 | [-0.162, 0.032] | 무유의 |

가장 두드러진 결과는 **`total_tokens`(보고서 길이)가 ρ=0.654로 가장 강한 양의 연관**을 보인다는 점입니다. 이는 cheap-talk/verbosity 우려를 정면으로 제기합니다 — 등급과 가장 강하게 연결된 것이 ESG 표현 강도가 아니라 단순 공시 분량일 수 있습니다. TF-IDF·cosine 계열(E·S·G)은 모두 양의 유의이나 효과 크기는 약~중간(0.13~0.40)입니다.

### 3.2 회귀 3종

| 모형 | β1 | p | R²/pseudo | AIC |
|---|---|---|---|---|
| OLS | 23.06 | 0.0006 | 0.406 | 1257.1 |
| Ordered Logit | 29.19 | 0.0020 | — | 1104.7 |
| Binary Logit (A↑) | 8.25 | 0.505 | 0.238 | 396.3 |

OLS·Ordered Logit은 주 설명변수(cosine_S, Spearman 자동 선택)가 양의 유의로 일관되나, Binary Logit(A 이상 여부)에서는 비유의입니다. Mann-Whitney U에서 고등급 그룹의 seed_tfidf·cosine·total_tokens 평균이 저등급보다 유의하게 높았습니다(`g_signal_ratio`·`esg_signal_ratio`만 무유의).

### 3.3 알파분석 4종

1. **부호 역전 robustness** — 표본 크기별 ρ: N=10에서 평균 0.317(표준편차 0.332, 양의 비율 82%) → N=381에서 0.401(표준편차 0, 100% 양). **소표본일수록 변동이 크다는 것을 정량 확인**했습니다. 김지우의 파일럿→전체 부호 역전(상위 대형주 편중 spurious +ve)과 같은 메커니즘이며, 본 분석은 N=381 전수로 표집 편의를 줄였습니다.
2. **section_weighted** — II·IV·VI 섹션별 분량과 등급의 상관 점검 (보고서 위치별 변별력).
3. **업종별 분해** — N≥10 업종 대상 회귀 분해.
4. **cheap-talk 3종 통제** — log_tokens·specificity·non-material 통제 후 주 신호 잔존 여부 OLS.

## 4. 한계 (인과 아닌 연관)

본 분석의 결과는 **연관성**이며 인과가 아닙니다(가이드 04 §4). 핵심 한계는 다음과 같습니다.

첫째, **cheap-talk 우려가 큽니다**. `total_tokens`가 가장 강한 연관(ρ=0.654)을 보이므로, ESG 텍스트 신호의 상당 부분이 실제 성과가 아니라 공시 장황함을 반영할 수 있습니다. 알파 ④의 verbosity 통제 결과를 회의에서 함께 검토해야 합니다. 둘째, 381 firm-year는 수업용 pilot panel로 KCGS 전체 대표표본이 아닙니다. 셋째, `esg_year = fiscal_year + 1` 정렬은 시점 식별이 아닙니다. 넷째, 기업·연도 고정효과를 통제하지 않았습니다(향후 알파). 다섯째, 분석기는 robust 검증으로 Kiwi를 선정했으나 분석기 의존성은 잔존합니다.

## 5. 팀 결과 비교 메모 (5/23 회의용)

| 분석자 | 표본 | 주 측정 | ρ (vs KCGS) |
|---|---|---|---|
| 이동원 (이전 pilot) | N=29 | seed_tfidf_E | +0.606 |
| **이동원 (통합 v1)** | **N=381** | seed_tfidf_E | **+0.318*** |
| 이동원 (통합 v1) | N=381 | total_tokens | +0.654*** |
| 김지우 | N=210 | g_signal_ratio | -0.197** |
| 이동원 (통합 v1) | N=381 | g_signal_ratio | -0.067 (무유의) |

통합 N=381에서 seed_tfidf_E는 양의 유의를 유지하되 pilot(0.606)보다 약해졌고, g_signal_ratio는 김지우 방향(음)과 같으나 무유의로 약화됐습니다. **측정 방식(seed TF-IDF 강도 vs signal 토큰 비율)에 따라 부호·유의가 갈리므로, 회의에서 어느 measurement를 최종 채택할지 + cheap-talk(total_tokens) 통제를 어떻게 둘지가 핵심 안건**입니다.

---

## 부록 — 산출물

- 노트북: `esg_dart_integrated_v1.ipynb`
- feature: `outputs/esg_features_integrated_v1.parquet` (381×feature)
- 통계: `outputs/spearman_bootstrap.csv`, `regression_3models.csv`, `analyzer_comparison.csv`
- 그림: `outputs/fig_01_collection.png` · `fig_02_analyzer.png` · `fig_04_features.png` · `fig_05_spearman_ci.png`
- corpus 캐시: `data/interim/corpus_381/` (381 JSON), `outputs/tokens_primary.json`
