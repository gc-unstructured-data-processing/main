# ESG DART 전체진행 3인 비교 — 30단계 정밀 점검

> **목적**: 김지우 · 김혜성 · 이동원 세 사람의 "전체진행" 노트북을, **(1) 실무·학술 방법론(웹 벤치마킹)** + **(2) 교수님 가이드 필수/위반** + **(3) 교수님의 숨은 의도/핵심 사항** 세 잣대로 30단계에 걸쳐 나란히 비교합니다.
> **작성**: 2026-05-23 · 5/23 추합 회의용 (4번째 팀원 신지영 노트북은 추후 업로드 예정 — 본 문서 N/A 처리)
> **대상 파일**: `김지우 0523_전체 진행.ipynb` · `김혜성 0523_전체 진행.ipynb` · `이동원_전체진행.ipynb`

---

## 0. 어떻게 읽는가 (범례)

각 단계는 아래 4블록으로 구성됩니다.

- **🎯 기준** — 가이드 + 실무 best practice가 요구하는 "이상적 모습"
- **📕 가이드 근거** — 교수님 가이드 문서(01~04)의 출처. `[필수]` `[위반금지]` `[가점]` `[선택]` `[숨은의도]`로 표시
- **🌐 실무/학술 벤치마킹** — 실제 논문·도구 문서에서 확인한 기준 (출처는 문서 끝 참고문헌)
- **3인 판정** — `✅ 충족` · `🟡 부분` · `⛔ 미흡/누락` · `➖ 해당 없음`, 한 줄 근거 포함

판정은 "누가 더 잘했나"의 줄세우기가 아니라, **어느 노트북의 어느 조각을 최종 통합본에 가져갈지** 고르기 위한 지도입니다.

---

## 1. 종합 스코어보드

| 블록 | 단계 | 김지우 | 김혜성 | 이동원 |
|---|---|:--:|:--:|:--:|
| **A. 표본·식별자** | 1–6 | 🟡🟡 | ✅✅ | ✅✅ |
| **B. 텍스트 추출** | 7–9 | ✅ | ✅✅ | ✅ |
| **C. 전처리·형태소** | 10–13 | 🟡 | ✅✅ | ✅ |
| **D. Feature·사전확장** | 14–20 | 🟡⛔ | ✅✅ | 🟡 |
| **E. 측정 validity** | 21–23 | ✅✅ | ✅ | ✅✅ |
| **F. 회귀** | 24–26 | ✅✅✅ | ✅ | ✅ |
| **G. 알파·해석·제출** | 27–30 | ✅✅ | ✅ | ✅ |

**한 줄 요약**
- **김혜성** = 가이드 *문자 그대로* 가장 충실. **fastText 사전확장(θ sweep+직접검토+v2)과 차원별(E/S/G) 등급 매칭**이 3인 중 유일하게 완성형. 표본 381 실행 보존.
- **이동원** = **통합·재현성**의 축. 두 측정 패러다임 병행 + Bootstrap CI + 알파 4종. 단, expanded는 manual 7단어로 **θ sweep 미실행**(본인 진단서도 인정).
- **김지우** = **방법론적 깊이(robustness·cheap-talk·고정효과)**가 압도적. 단 **표본 N=210(KOSPI 한정)**으로 가이드의 381과 다르고, **업로드본에 셀 출력이 없어 재현 증빙이 비어 있음**, fastText는 frame만(미구현).

---

## 2. 교수님의 "숨은 의도" 9가지 — 점수의 갈림길

가이드를 표면적으로 읽으면 "수집→TF-IDF→회귀"지만, 평가표(04)와 개요(01)의 행간에는 **진짜 시험 포인트**가 숨어 있습니다. 이 9가지가 상·중·하를 가릅니다.

| # | 숨은 의도 | 가이드 단서 | 누가 가장 잘 짚었나 |
|---|---|---|---|
| H1 | **"정답 재현이 아니라 선택의 정당화"** 가 과제의 본질 | 01 line 39–42 "정해진 정답 결과값을 재현하는 과제가 아닙니다" | 김지우 (Decision Box) · 이동원 (What/Why) |
| H2 | **cheap-talk이 핵심 시험** — `total_word_count` 통제를 *왜* 넣는지 이해했는가 | 04 line 46 / 03 line 234 | 김지우(verbosity-adjusted) · 이동원(specificity 3종) |
| H3 | **분석기 선정·제외 근거**는 교수 심층질문 대비용 | 03 평가표 "왜 이 도구?" + 5/19 회의 | 이동원·김혜성 (Komoran/Kkma 제외 근거) |
| H4 | **expanded dictionary는 "정답 사전"이 아니라 팀이 만든 것** — θ sweep·직접검토 *과정 자체*가 평가 대상 | 01 line 102 / 03 line 120 (Bao 2024) | **김혜성** (유일하게 완주) |
| H5 | **측정 validity(Spearman+평균차) 없이 회귀 직행 = 흔한 실패** | 04 평가표 "측정 validity" 행 | 3인 모두 충족 |
| H6 | **약한 연관(ρ 0.1–0.2)을 강한 예측력으로 과장 금지** | 03 line 188 / 04 line 89 | 김지우 (ρ 해석 기준표) |
| H7 | **381은 pilot 표본 — 대표표본·일반화 금지** | 04 line 101 | 3인 모두 명시 (단 김지우는 N=210로 축소) |
| H8 | **거버넌스(G) 어휘·등급은 의무공시(IDF≈1.0)라 cheap-talk 함정** | 03 line 234 해석 | **김혜성**(IDF 진단) · 김지우(Alpha 4) |
| H9 | **차원별(E/S/G) 점수 ↔ 차원별 등급 매칭이 자연스러움** (Bai 2024) | 03 line 146 | **김혜성** (e/s/g_grade 분리 매칭) |

> 회의 결론용 핵심: **H4(fastText 완주)는 김혜성, H2·H6(cheap-talk·과장금지)는 김지우, H3·재현성은 이동원**이 모범. 최종본은 이 세 강점을 합쳐야 합니다.

---

## 3. 30단계 정밀 비교

### 블록 A — 표본·식별자 (1–6)

#### 1단계. 표본 규모 — "최대 381 firm-year 시도"
- **🎯 기준**: company_master 127사 × 3년 = 최대 381 firm-year를 *시도*하고, 성공 행으로 corpus 구성.
- **📕 가이드**: `[필수]` 01 line 127 / 02 line 117·123 "모든 팀은 최대 381행을 기준으로 수집을 시도".
- **🌐 벤치마킹**: 텍스트-등급 연구는 표본 편의(selection bias)가 ρ 부호까지 뒤집을 수 있어, 가용 모집단 전수 시도가 표준.
- **김지우 🟡** N=210 (KOSPI·FY2021–2023 한정). 검정력은 충분하나 가이드의 381 모집단과 다름 → 회의에서 "왜 KOSPI만"의 정당화 필요.
- **김혜성 ✅** N=381 전수 수집·실행 확인(`SUCCESS 381`).
- **이동원 ✅** N=381 전수 (`시도 381 | SUCCESS 381 100%`).

#### 2단계. 식별자 키 — `stock_code × fiscal_year` (회사명 join 금지)
- **🎯 기준**: 종목코드+회계연도 복합키로 join. 회사명 join은 silent 오매칭.
- **📕 가이드**: `[위반금지]` 02 line 35 "회사명으로 merge하면 silent 오매칭".
- **🌐 벤치마킹**: 한국 상장사는 사명변경·분할로 company_name 133 ≠ stock_code 127. 패널 데이터 표준은 안정적 ID 키.
- **김지우 ✅** 5-key 원칙 `stock_code→corp_code→rcept_no→fiscal_year→esg_year` 명문화.
- **김혜성 ✅** stock_code join 명시, corpCode.xml 전체 매핑(127개 1회).
- **이동원 ✅** `stock_code × fiscal_year` 키만 사용 (위반금지 #2).

#### 3단계. `stock_code` zfill(6) 정규화
- **🎯 기준**: CSV 로드 시 앞자리 0 손실(`005930→5930`) 복구.
- **📕 가이드**: `[숨은의도]` 직접 명시 없으나 02 식별자 정합성의 전제. 평가표 "DART lineage".
- **🌐 벤치마킹**: pandas `dtype=str`/`zfill(6)`은 한국 종목코드 처리 정석.
- **김지우 ✅** zfill(6) 명시 ("CSV는 앞자리 0을 잃는다").
- **김혜성 ✅** `005930→5930` 복구 + 길이분포 `{6: 381}` 검증.
- **이동원 ✅** `zfill(6)` (위반금지 #7 silent 오매칭 방지).

#### 4단계. 타이밍 — `esg_year = fiscal_year + 1`
- **🎯 기준**: KCGS 평가연도 t ↔ 직전 회계연도 t−1 사업보고서 연결.
- **📕 가이드**: `[필수]` 01 line 70 / 02 line 37 / 04 line 111.
- **🌐 벤치마킹**: 공시→평가 lag 정렬은 disclosure 연구의 기본. (단, 인과 식별 아님 명시 필요)
- **김지우 ✅** `esg_year = fiscal_year+1` ("KCGS가 전년도 보고서 평가").
- **김혜성 ✅** 검색기간 `fiscal_year+1`년 공시로 적용 + 비12월 결산 한계 명시.
- **이동원 ✅** `esg_year = fiscal_year+1` (위반금지 #8).
- **공통 메모**: 등급 수치 변환 스케일이 갈림 — 가이드는 `S=6…D=0`(0–6). 이동원=가이드 일치, 김혜성/김지우=7-scale(A+=7…) 표기. 순서는 보존되나 **회의에서 스케일 1개로 통일** 권장.

#### 5단계. 실패행 처리 — 가짜 0 금지 + 사유 기록
- **🎯 기준**: 수집·추출 실패 행은 삭제/사유기록, **0점으로 채워 corpus에 넣지 않음**.
- **📕 가이드**: `[위반금지]` 01 line 98 / 02 line 172 / 04 line 58 "실패 행을 가짜 0으로 채우지 않는다".
- **🌐 벤치마킹**: 결측을 0으로 대체하면 분포·계수 모두 왜곡 — missingness 명시가 표준.
- **김지우 ✅** `salvage_log.csv`에 INCLUDE/EXCLUDE_NO_RCEPT/EXCLUDE_KCGS_NA 기록, NaN 보존.
- **김혜성 ✅** 실패 13건 status=FAIL+사유 기록 → 진단 후 전수 복구(가짜 0 없음).
- **이동원 ✅** 실패 행 status·reason 기록, corpus 제외 (위반금지 #1).

#### 6단계. raw 원문 보존 + lineage 로그 (재현성)
- **🎯 기준**: 원문 ZIP/XML 보존, 어디서 행이 사라졌는지 추적 가능한 lineage 로그.
- **📕 가이드**: `[필수]` 02 line 145·176 "재현성 보강" / 04 재현성 체크.
- **🌐 벤치마킹**: 원자료 보존+감사로그는 reproducible research 핵심.
- **김지우 ✅** `lineage_audit_v2.csv` + `salvage_log.csv` 2종 감사 로그.
- **김혜성 ✅** `collection_meta.csv` + `corpus/{code}_{year}.json` + 캐시 ZIP, 체크포인트 재개.
- **이동원 ✅** `data/raw/*.zip` 보존 + `corpus_381/` JSON 캐시(idempotent) (위반금지 #5).

---

### 블록 B — 텍스트 추출 (7–9)

#### 7단계. II/IV/VI 섹션 선택 + 출처 기록
- **🎯 기준**: II(사업의 내용)·IV(경영진단)·VI(이사회)에서 ESG 문장 추출, section 출처 컬럼 보존.
- **📕 가이드**: `[필수]` 01 line 99 / 02 line 137 / 04 line 37.
- **🌐 벤치마킹**: ESG 텍스트 연구는 보고서 전체보다 관련 섹션 한정이 잡음을 줄임(GRI 기반 word-list 관행).
- **김지우 ✅** II/IV/VI 추출 + 섹션별 컬럼 별도 보존(Alpha 4 입력).
- **김혜성 ✅** TITLE 로마숫자 경계 + `<P>`만 추출(`<TABLE>` 재무숫자 제외), 섹션 출처 기록.
- **이동원 ✅** II·IV·VI 본문 추출 (TITLE+TABLE 제거+P 추출).

#### 8단계. XML 직접 파싱 — MCP/LLM passage 신뢰 금지
- **🎯 기준**: MCP/LLM이 만든 passage를 그대로 쓰지 않고 Python으로 직접 파싱·재현.
- **📕 가이드**: `[위반금지]` 02 line 94 "MCP passage는 실제 공시와 다를 수 있으므로 반드시 코드로 재현".
- **🌐 벤치마킹**: LLM 생성 발췌는 hallucination 위험 — 원문 파싱이 audit 가능.
- **김지우 ✅** XBRL→text 직접 추출 파이프라인.
- **김혜성 ✅** "MCP passage는 다를 수 있으므로 원문 XML 직접 파싱"을 단계 목적으로 명시.
- **이동원 ✅** `XMLParser(recover=True)`로 직접 파싱(비정상 XML도 복구).

#### 9단계. firm-year 1행 집계
- **🎯 기준**: 같은 firm-year의 여러 passage를 하나의 document로 묶어 회귀표 1행 생성.
- **📕 가이드**: `[필수]` 01 line 100 / 03 line 32.
- **🌐 벤치마킹**: Li et al.(2021) firm-year document 단위 = 표준 분석 단위.
- **김지우 ✅** `firm_year_documents_v2.parquet` (섹션별 컬럼도 보존).
- **김혜성 ✅** II/IV/VI를 firm-year당 1 document로 통합.
- **이동원 ✅** firm-year 단위 document → feature 1행.

---

### 블록 C — 전처리·형태소 (10–13)

#### 10단계. 형태소 분석기 robust 비교 (Kiwi vs Okt 정량)
- **🎯 기준**: 분석기를 *근거 기반*으로 선정 — seed 보존율·속도·vocab 정량 비교.
- **📕 가이드**: `[숨은의도/회의결정]` 5/19 회의 결정 ② "robust 검증 후 결정". 04 평가표 "텍스트 처리".
- **🌐 벤치마킹**: Kiwi 공식 벤치마크상 모호성 해소 평균 정확도 **86.7%**로 통계+Skip-Bigram 기반 우수, 속도도 경량(C++). Okt/Mecab는 카테고리별 혼재. → "정량 비교 후 선택"이 모범.
- **김지우 🟡** Kiwi(exp_F) 채택을 Decision Box로 정당화하나, Okt 정량 표는 본문에 미수록(별도 분석으로 언급).
- **김혜성 ✅** 8지표 정량표: 속도 Kiwi 1.31s vs Okt 2.97s(2.3배), seed 사전등록 후 30/30 vs 20/30, Jaccard 0.649. 가장 상세.
- **이동원 ✅** 동일 corpus 표본에서 seed 보존 Kiwi 87%(26/30) vs Okt 67%(20/30), 처리시간 11.5s → PRIMARY=Kiwi.

#### 11단계. 분석기 제외 근거 (Komoran·Kkma) — 교수 심층질문 대비
- **🎯 기준**: 왜 Kiwi/Okt만? 왜 Komoran·Kkma는 제외? 정성·정량 근거.
- **📕 가이드**: `[숨은의도]` 5/19 회의 메모 "교수님 심층 질문 대비 — 선정/제외 근거 명확히".
- **🌐 벤치마킹**: KoNLPy 멀티분석기(Hannanum/Kkma/Komoran/Mecab/Okt) 중 Kkma는 과세분화·저속, Komoran은 미등록어·사용자사전 우선권 제어 약함 — 문헌 정합.
- **김지우 ➖** Kiwi/Okt/Mecab/KoBERT만 비교 후보로 언급, Komoran/Kkma 제외 근거는 없음.
- **김혜성 🟡** Kiwi vs Okt 정량 비교에 집중, Komoran/Kkma 명시적 제외 근거는 약함.
- **이동원 ✅** Kkma(과세분화·저속)·Komoran(미등록어·score 미지원)·Okt(복합명사 분리) 제외/선정 근거를 정성+정량으로 명문화.

#### 12단계. seed 복합명사 보존 (user dict score)
- **🎯 기준**: "재생에너지·감사위원회" 등 복합명사가 분리되면 TF-IDF 매칭 실패 → 사용자 사전 NNP 등록.
- **📕 가이드**: `[필수]` 03 line 90 expanded 전제 / 5/19 회의 결정 ③ seed 30 활용.
- **🌐 벤치마킹**: seed-based dictionary 방법은 seed 토큰의 무결성이 측정의 전제(Li et al. 2021).
- **김지우 ✅** 30 seed + 14 복합어를 NNP·score=50 등록, 단위테스트로 보존 검증(≈100%).
- **김혜성 ✅** `add_user_word(term,"NNP",50)` → 15/30→30/30 보존. 신지영 미등록 손실 회피 근거.
- **이동원 ✅** seed 30개 user dict 등록(score=50), 보존 정량 확인.

#### 13단계. 불용어 (회사명/boilerplate 제거 기준)
- **🎯 기준**: 회사명·연도·반복 법률용어 등 비-ESG 잡음 제거, 기준을 보고서에 기록.
- **📕 가이드**: `[필수]` 03 line 56–58 "stopwords_ko_esg.txt 초안 + 회사명·연도·법률용어 추가".
- **🌐 벤치마킹**: boilerplate/회사명 제거는 ESG 텍스트 readability·greenwashing 연구의 표준 전처리.
- **김지우 ✅** `STOPWORDS_EXTENDED` + `G_SIGNAL_PROTECT` 보호집합(겹침 검증), `bp_contamination_rate`로 정량화.
- **김혜성 ✅** stopwords 초안 + 회사명/숫자/법률용어 제거, 358개 불용어(seed 제외).
- **이동원 ✅** 회사명(1·2자 분리 포함) boilerplate 불용어 제거, seed는 불용어에서 제외.

---

### 블록 D — Feature·사전확장 (14–20)  ← **점수 가장 크게 갈리는 구간**

#### 14단계. seed TF-IDF 점수 (E/S/G 차원별)
- **🎯 기준**: TF-IDF 행렬에서 차원별 seed 단어 값 합산 → firm-year 점수.
- **📕 가이드**: `[필수]` 03 §2 line 124–130 / 01 line 101.
- **🌐 벤치마킹**: seed-word TF-IDF 합산 = Li et al.(2021) firm-year 점수화의 직접 적용.
- **김지우 ✅** `seed_tfidf_E/S/G` + ratio·concentration 등 위계적 feature.
- **김혜성 ✅** E/S/G seed_score (M1a), IDF 진단(G≈1.0) 동반.
- **이동원 ✅** `seed_tfidf_E/S/G` (E ρ=0.318***, G=0.210***, S=0.131*).

#### 15단계. expanded dictionary = seed→embedding→팀 기준 걸러내기
- **🎯 기준**: seed 10개씩→embedding 후보 확장→**팀 기준으로 직접 걸러낸** 사전으로 *설명*.
- **📕 가이드**: `[필수]` 01 line 101 / 03 line 90–93 / 04 line 40.
- **🌐 벤치마킹**: 금융 텍스트 키워드 확장(word2vec/fastText cosine 임계)은 확립된 방법 — 단, 후보를 그대로 쓰지 않고 큐레이션이 필수.
- **김지우 🟡** 절차 frame + 4기준(채택/기각) 명시하나, **manual_v1 7단어가 N=29 subset에서만 계산**되어 final(N=210)에 미통합(honest gap 자인).
- **김혜성 ✅** seed 30 → expanded **56단어**(v1 39 → v2 27 추가), 차원별 직접 검토표(keep/drop+사유) 완비.
- **이동원 🟡** `expanded_manual` 7단어 사용. 절차 설명은 있으나 embedding 기반 확장은 manual 대체.

#### 16단계. fastText 직접 학습 (사전학습 모델 X = 가점)
- **🎯 기준**: 사업보고서 corpus로 fastText/Word2Vec를 *직접 학습*해 도메인 벡터 확보.
- **📕 가이드**: `[가점]` 03 line 90 word embedding / 김혜성 노트북 "가이드 가점 조건 = 직접 학습".
- **🌐 벤치마킹**: 산업특화 임베딩이 산업-불가지론 확장보다 금융 불확실성 설명력이 유의하게 큼(Theil et al.). 직접 학습이 도메인 정합.
- **김지우 ⛔** "본 final 코드베이스에 fastText 모델이 없어 미생성" — 미구현(자인).
- **김혜성 ✅** 사업보고서 corpus로 fastText 직접 학습(문장단위 재토큰화), 도메인 벡터 확보.
- **이동원 ⛔** fastText 학습 없이 manual 확장 — 본인 GUIDE_발전제안에서 "θ sweep 미충족(가이드 03 line 90–122)"으로 발전과제 ③ 등록.

#### 17단계. θ sweep — 여러 임계값 비교 (상위 100단어 검토)
- **🎯 기준**: cosine θ를 여러 값으로 바꿔 확장 사전 크기·잡음 비율을 표로 정리, θ 정당화.
- **📕 가이드**: `[필수]` 01 line 102 / 03 line 120–122 (Bao et al. 2024) — **명시적 요구**.
- **🌐 벤치마킹**: 임계값 calibration + 상위 N 후보 검토는 lexicon expansion의 표준 절차.
- **김지우 ⛔** θ 비교표가 **빈 frame**(0.50/0.60/0.70/0.80 칸 미기입) — 재계산 시 채우도록 남김.
- **김혜성 ✅** θ=0.55/0.60/0.65/0.70 sweep, 후보수·잡음비율표, θ=0.60 선택 근거(20/39/83개 비교) + v2에서 차등 θ까지.
- **이동원 ⛔** θ sweep 미실행 (발전과제로 명시).

#### 18단계. 후보 단어 직접 검토·잡음 제거 (회사명 등)
- **🎯 기준**: fastText 결과를 그대로 확정하지 않고, 회사명·인명·일반어를 직접 검토해 걸러냄.
- **📕 가이드**: `[필수]` 02 line 76 / 03 line 122 / 04 line 41·76.
- **🌐 벤치마킹**: 자동 확장은 회사명·고유명사 잡음을 포함 → 인간 검토(human-in-the-loop)가 dictionary validity 핵심.
- **김지우 🟡** 채택/기각 4기준 명시(개념적). 실제 후보 리스트 검토 산출물은 미생성(모델 없음).
- **김혜성 ✅** θ=0.60의 39개 직접 검토표 + 한국 성씨 30개·subword 부작용(`이사무엘`,`감사선`)·법률접미사 자동분류 v3 + 수동 drop 사유. 가장 철저.
- **이동원 🟡** seed 직접 검토는 했으나 expanded 후보 대량 검토는 manual 7단어로 제한.

#### 19단계. 기준 문장 cosine similarity (baseline)
- **🎯 기준**: E/S/G 기준 문장과 firm-year 문서의 TF-IDF 벡터 cosine — 보조 baseline.
- **📕 가이드**: `[선택/baseline]` 01 line 55–59 / 03 §4 line 209–215.
- **🌐 벤치마킹**: 단어겹침 cosine은 보조지표 — semantic이 아닌 lexical 유사도임을 명시해야.
- **김지우 ➖** cosine보다 ratio·concentration 패러다임 중심(직접 미구현).
- **김혜성 ✅** E/S/G 기준문장 cosine(M2), 동일 vocab/IDF 공간 → 직접 비교. **S 차원에서 cosine만 유의(β=0.359**)**라는 측정방식 효과 발견.
- **이동원 ✅** `cosine_E/S/G` feature 생성(03 §4 근거).

#### 20단계. 다중공선성 회피 (seed/expanded 동시 투입 금지)
- **🎯 기준**: seed와 expanded를 동시에 회귀에 넣지 않음(계수 불안정).
- **📕 가이드**: `[필수]` 03 line 132 "동시에 넣으면 다중공선성".
- **🌐 벤치마킹**: 상관 0.8+ 변수 동시투입은 VIF 폭증 — 독립 모델 비교가 정석.
- **김지우 ✅** VIF 사전 진단(>10 주의) + 변수 분리.
- **김혜성 ✅** seed/v2/cosine 상관 0.80~0.97 → "동시 투입 금지, 독립 회귀식".
- **이동원 ✅** seed와 expanded 동시 투입 안 함 명시.

---

### 블록 E — 측정 validity (21–23)

#### 21단계. Spearman 순위상관 (회귀 *전* 검증)
- **🎯 기준**: 회귀 직행 전에 feature↔등급 Spearman ρ로 연관 확인(등급=서열변수).
- **📕 가이드**: `[필수]` 03 §3 line 166 / 04 평가표 "측정 validity".
- **🌐 벤치마킹**: 서열 종속변수엔 Pearson보다 Spearman — 비선형 단조관계도 포착.
- **김지우 ✅** exp_F Spearman + ρ 해석기준표(<0.10 무시 / 0.10–0.20 약함…).
- **김혜성 ✅** 차원매칭 Spearman (E 0.402, S 0.229, G −0.130) 회귀 전 보고.
- **이동원 ✅** Spearman + **Bootstrap 95% CI**(CI_excl_0) 동반 — 가장 강한 형태.

#### 22단계. 등급 그룹 평균차 (t-test/Mann-Whitney)
- **🎯 기준**: 고등급 vs 저등급 그룹 feature 평균차 검정으로 연관을 다른 각도에서 확인.
- **📕 가이드**: `[필수]` 03 line 190–192 / 04 평가표.
- **🌐 벤치마킹**: 분포 비교는 상관과 독립적 증거 — 효과크기(rank-biserial) 동반이 모범.
- **김지우 ✅** Mann-Whitney U(high≥B+ vs low) + rank-biserial effect size.
- **김혜성 ✅** Shapiro 정규성 검정 후 t-test 또는 Mann-Whitney 분기.
- **이동원 ✅** Mann-Whitney U(A 이상 vs 미만).

#### 23단계. 약한 연관 신중 해석 (ρ 0.1–0.2)
- **🎯 기준**: p<0.05라도 ρ가 작으면 "강한 예측력" 아닌 "약한 연관"으로 해석.
- **📕 가이드**: `[숨은의도]` 03 line 188 / 04 line 89.
- **🌐 벤치마킹**: 통계적 유의 ≠ 실질적 의미 — 효과크기 보고가 책임 있는 해석.
- **김지우 ✅** "통계적 유의성 ≠ 실질적 의미" 명문화, robust evidence 기준 엄격.
- **김혜성 ✅** "약한 연관" 라벨링(G −0.13 약한 음).
- **이동원 ✅** 약/중/강 구분, total_tokens cheap-talk 우려로 신중.

---

### 블록 F — 회귀 (24–26)

#### 24단계. 모형 선택 (OLS/Ordered/Binary) + 선택 근거
- **🎯 기준**: 세 모형 중 *팀 질문에 맞는* 모형 선택 + 버린 대안 한계 서술.
- **📕 가이드**: `[필수]` 03 §5 line 221–274 / 04 평가표 "모형 선택".
- **🌐 벤치마킹**: 서열 등급엔 ordered logit이 통계적 적합(등급-신용평가 연구 다수). OLS는 해석용 baseline.
- **김지우 ✅** M1~M5 (OLS 3종 + Ordered + Binary), "셋이 같은 방향일 때만 신호 인정" 원칙.
- **김혜성 ✅** 9식×3모형=27회귀, 부호·유의 일관성 점검 후 메인=Ordered Logit 선택근거 4가지.
- **이동원 ✅** OLS/Ordered/Binary 3종 비교(OLS β=23.06 p=0.0006 R²=0.406, Ordered β=29.19 p=0.002).

#### 25단계. cheap-talk 통제 변수 (`total_word_count`/`log_tokens`)
- **🎯 기준**: 분량 통제 후에도 텍스트 신호가 살아남는지로 cheap-talk 판별 — **과제의 핵심 시험**.
- **📕 가이드**: `[필수/숨은의도]` 03 line 234·266 / 04 line 46.
- **🌐 벤치마킹**: greenwashing 연구는 verbal vs substantive 비율·분량 통제로 cheap-talk 측정. 분량 통제는 필수.
- **김지우 ✅** `log_tokens` 항상 통제, M1→M2 계수변화를 cheap-talk 진단 핵심으로.
- **김혜성 ✅** `n_tokens`/`log_n_tokens` 통제, S차원 TF-IDF 신호가 통제 후 소멸 = cheap-talk 정량 증거.
- **이동원 ✅** `total_tokens`(ρ=0.654 최강!) 통제. 단 total_tokens가 최강신호라 verbosity 환원 위험을 본인 GUIDE에서 1순위 발전과제로.

#### 26단계. 고정효과/통제변수 (industry·year FE)
- **🎯 기준**: 기업 특성·연도 교란을 통제하는 패널 고정효과.
- **📕 가이드**: `[선택/best practice]` 03 line 164 재무통제 "(선택)". 가이드 필수 아님 → **실무 가점 영역**.
- **🌐 벤치마킹**: firm/year fixed-effects ordered logit이 ESG-등급 패널의 표준(feologit 등). 시간불변 교란 제거.
- **김지우 ✅** **유일하게** `industry_FE + year_FE` 투입(M3~M5). 실무 수준 가장 높음.
- **김혜성 🟡** 차원·섹션·measure 분해는 깊으나 명시적 FE 패널은 미투입.
- **이동원 🟡** pooled OLS — 기업·연도 FE 미투입(본인 GUIDE 발전과제 ④로 명시).

---

### 블록 G — 알파·해석·제출 (27–30)

#### 27단계. cheap-talk 가설 정면 검토 (verbosity vs 실질)
- **🎯 기준**: 단어빈도 강한 ρ가 진짜 ESG인지 단순 disclosure 장황함인지 구분 논의.
- **📕 가이드**: `[필수/숨은의도]` 04 line 46 / 01 line 106.
- **🌐 벤치마킹**: cheap-talk·greenwashing은 ESG 공시 텍스트 연구의 중심 주제(저성과 기업이 언어로 보완).
- **김지우 ✅** 4 alpha 전부 cheap-talk 축(verbosity-adjusted·저등급 전략공시·sign reversal·거버넌스 역설). 가장 정면.
- **김혜성 ✅** G IDF≈1.0 의무공시 → cheap-talk 후보 진단 + S 차원 TF-IDF 소멸로 정량 증거.
- **이동원 ✅** specificity/commitment/non-material 3종 cheap-talk + total_tokens 우려 명시.

#### 28단계. 알파분석 — 왜 필요/무엇을 더/한계
- **🎯 기준**: 기법 난이도 아닌 "왜·무엇을 더 확인·어떤 한계"가 분명한 추가 검증 1개+.
- **📕 가이드**: `[필수]` 01 line 105 / 04 §3-1 line 93–97.
- **🌐 벤치마킹**: 섹션별·업종별 분해, 통제 변형 등 robustness가 좋은 알파의 예.
- **김지우 ✅** Alpha 1~4 + 발표용 메시지 매트릭스. 각 한계 명시.
- **김혜성 ✅** 섹션별(II/IV/VI × E/S/G) 1,143 측정단위 mechanism 해부 — 본문 발견을 섹션으로 정밀 검증.
- **이동원 ✅** 부호역전·section_weighted·업종분해·cheap-talk 3종 4축.

#### 29단계. 인과 아닌 연관·표본 한계 명시
- **🎯 기준**: 인과 단정 금지, 381=pilot·표현≠성과·KCGS validity 한계 서술.
- **📕 가이드**: `[위반금지급]` 01 line 142–148 / 04 §4.
- **🌐 벤치마킹**: ESG 등급 제공자 간 상관 0.38~0.71(Berg et al. 2022) — 외부 anchor 자체가 불일치 → validity 한계 인정이 정직.
- **김지우 ✅** "association만", KCGS 방법 비공개·KOSPI 편향 한계 명시. ESG 등급 divergence 인식 우수.
- **김혜성 ✅** 비12월 결산 회계기간 불일치·차원 직접비교 금지 등 한계 구체적.
- **이동원 ✅** pilot·cheap-talk·timing·분석기 의존·FE 미통제까지 한계 6종.

#### 30단계. 제출 형식·재현성 (Run All 재현, API key .env, .md 보고서)
- **🎯 기준**: 위→아래 Run All 재현, API key는 .env만, 보고서 .md.
- **📕 가이드**: `[필수]` 04 §1·§2-1·§5 / 01 line 113.
- **🌐 벤치마킹**: 실행 가능 노트북 + 비밀키 분리 = reproducible submission 기본.
- **김지우 ⛔(재현 증빙)** 코드 구조·Decision Box는 우수하나 **업로드본에 셀 출력이 0개**(미실행 상태) → "Run All 재현" 증빙이 비어 있음. 회의 전 전체 실행·출력 보존 필요.
- **김혜성 ✅** 67개 코드셀 출력 보존(실행 완료), 캐시로 재실행 0호출.
- **이동원 ✅** Run All 완주·출력 보존, idempotent 캐시, `.env`의 `API_KEY`만 사용.

---

## 4. 회의(5/23) 결정용 — "최종본에 무엇을 가져갈까"

| 영역 | 채택 권장 베이스 | 이유 |
|---|---|---|
| **수집·표본** | 김혜성/이동원 (N=381) | 가이드 381 충족 + 실행 보존. 김지우 N=210은 KOSPI 한정 |
| **수집 함수** | 김혜성 `find_business_report_v2` + 이동원 `recover` parser | 결산월 무관+정정 우선 + 비정상 XML 복구 (이미 이동원이 통합) |
| **형태소 근거** | 이동원(제외근거) + 김혜성(8지표 정량) | 교수 심층질문 H3 대비 |
| **fastText·expanded** | **김혜성** (θ sweep + 직접검토 + v2) | H4·H5 유일 완주 — 가장 큰 가점 영역 |
| **차원별 등급매칭** | **김혜성** (e/s/g_grade 분리) | H9, Bai 2024 정합 |
| **회귀·고정효과** | **김지우** (industry+year FE) + 3모형 일관성 | H2·실무 최고 수준 |
| **robustness·cheap-talk** | **김지우** (sign reversal·verbosity-adjusted) | H2·H6·H8 정면 |
| **알파(섹션)** | 김혜성(섹션 mechanism) + 이동원(section_weighted) | 보고서 위치별 점수 가이드 1순위 |
| **재현성·통합 골격** | **이동원** (단일 노트북·캐시·.env) | Run All 완주 검증됨 |

### 즉시 액션 (회의 전)
1. **김지우 노트북 전체 실행 → 출력 보존** (현재 재현 증빙 공백 / 30단계).
2. **등급 스케일 1개로 통일** (가이드 0–6 권장 / 4단계).
3. **fastText·θ sweep을 통합본에 김혜성 방식으로 이식** (이동원·김지우의 D블록 공백 메우기 / 15–18단계).
4. **표본 정의 합의**: 381 전수(가이드) vs 210 KOSPI(검정력·동질성) — 1단계.

---

## 5. 참고문헌 (웹 벤치마킹 출처)

**ESG 공시 텍스트분석 · cheap-talk · greenwashing**
- Peeking into Corporate Greenwashing through the Readability of ESG Disclosures, *Sustainability* 16(6):2571 — https://www.mdpi.com/2071-1050/16/6/2571
- Detecting Greenwashing in ESG Disclosure: An NLP-Based Analysis, *Sustainability* 18(3):1486 — https://www.mdpi.com/2071-1050/18/3/1486
- Textual Attributes of Corporate Sustainability Reports and ESG Ratings, *Sustainability* 16(21):9270 — https://www.mdpi.com/2071-1050/16/21/9270
- Identifying greenwashing in CSR reports using NLP, *European Financial Management* (2025) — https://onlinelibrary.wiley.com/doi/full/10.1111/eufm.12509

**word embedding 사전 확장 (seed → cosine θ)**
- Financial Keyword Expansion via Continuous Word Vector Representations — https://www.researchgate.net/publication/274314819_Financial_Keyword_Expansion_via_Continuous_Word_Vector_Representations
- Explaining Financial Uncertainty through Specialized Word Embeddings (산업특화 임베딩 우위) — https://www.researchgate.net/publication/339896379_Explaining_Financial_Uncertainty_through_Specialized_Word_Embeddings
- LEXpander: automated lexicon expansion, *Behavior Research Methods* (2023) — https://link.springer.com/article/10.3758/s13428-023-02063-y

**한국어 형태소 분석기 (Kiwi vs Okt/Mecab)**
- kiwipiepy benchmark (disambiguation) — https://github.com/bab2min/kiwipiepy/tree/main/benchmark/disambiguate
- Kiwi: Korean Morphological Analyzer Based on Statistical LM & Skip-Bigram (정확도 86.7%) — https://accesson.kr/kjdh/v.1/1/109/43508

**KCGS ESG 등급 방법론 · 등급체계**
- 한국ESG기준원 KCGS ESG Rating 자료 — https://www.hyosung.com/resources/en/file/management/credit-rating/KCGS-ESG-Rating(Hyosung).pdf
- KCGS 지배구조 평가 가이드 (S~D 7등급, 부문별 E/S/G) — https://esgconsulting.co.kr/wiki/esg/kcgs/

**ordered logit · 고정효과 패널 (서열 등급 회귀)**
- feologit: fixed-effects ordered logit, *Stata Journal* (2020) — https://journals.sagepub.com/doi/full/10.1177/1536867X20930984
- Estimating effects of ESG scores on credit ratings using multivariate ordinal logit, *Empirical Economics* (2022) — https://link.springer.com/article/10.1007/s00181-021-02121-4

**방법론 핵심 anchor (가이드 인용 문헌)**
- Li, Mai, Shen, Yan (2021), Measuring Corporate Culture Using Machine Learning, *RFS* 34(7):3265 — https://academic.oup.com/rfs/article-abstract/34/7/3265/5869446
- Berg, Kölbel, Rigobon (2022), Aggregate Confusion: The Divergence of ESG Ratings, *Review of Finance* 26(6):1315 — https://academic.oup.com/rof/article/26/6/1315/6590670

---

*본 비교는 업로드된 3개 노트북과 교수님 가이드 01~04, 이동원 GUIDE_발전제안_v1을 교차 검증해 작성. 수치는 각 노트북의 실제 셀 출력(이동원·김혜성) 및 서술(김지우)에서 인용. 4번째 팀원(신지영) 노트북 업로드 시 동일 30단계로 갱신 예정.*
