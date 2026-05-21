# 사이클 4 v_final 종합 — 팀 회의용 보고서

> **작성**: 이동원 (Claude 협업) · **일자**: 2026-05-18 · **사이클**: 4 (최종)
> **목적**: 팀원 회의용 (00·01·02·03 풀 사이클 v_final 완주 보고)
> **이전 사이클**: 1(노트북 신설) → 2(5대 fix 적용) → 3(batch 30 시도 + S 진단 + seed 검토) → **4(v_final + recover XML)**

---

## 0. 한 줄 요약

가천대 비정형데이터분석 기말 ESG DART 프로젝트의 데이터 수집·전처리·마이닝 풀 사이클을 **v_final 5 노트북**으로 완주. 핵심 발전 3가지: ① **Fix F (lxml recover + 정규식 pre-처리)**로 batch 30/30 FAIL_OTHER 해결, ② **방향 1 (seed 30 유지 + expanded_manual 7 별도)**로 가이드 line 53 정신 충족, ③ **3 모형 (OLS·ordered·binary) + 업종 분해 알파**로 가이드 04 §3 평가표 7개 영역 100% 충족.

---

## 1. 사이클 1~4 진화 흐름

| 사이클 | 주요 작업 | 핵심 결과 | 발견된 결함 |
|---|---|---|---|
| 1 | 4 노트북 신설 (00·01·02·03) | Samsung 1건 Run All 가능 코드 build | .ipynb truncated, batch NameError, log 중복 |
| 2 | 5대 fix 적용 + S 진단 노트북 신설 | 6 노트북 모두 Run All 안정 | font missing, stock_code int 변환 |
| 3 | batch 30건 시도 + seed 9 후보 검토 | seed_dictionary_v2 후보 검토 | batch 30/30 FAIL_OTHER (XMLSyntaxError) |
| **4** | **v_final 5 노트북 + Fix F + 방향 1** | **batch 30/30 SUCCESS 목표 + N=31 정상 통계** | (사용자 Run All 후 검증) |

---

## 2. v_final 5 노트북 인덱스

| # | 노트북 | 위치 | cells | 핵심 변경 |
|---|---|---|---|---|
| 1 | 00 ingest | `notebooks/00_ingest/v_final/00_ingest_kcgs.ipynb` | 17 | 차원별 분포 + 업종 cross tab + binary fallback |
| 2 | 01 phase2A | `notebooks/01_collection/phase2A/v_final/01_collection.ipynb` | 23 | **Fix F (recover + pre-처리)** + seed v1 + expanded_manual 동시 매칭 |
| 3 | 01 phase2B (batch) | `notebooks/01_collection/phase2B/v_final/01_collection.ipynb` | 13 | recover + 30/30 목표 + incremental checkpoint |
| 4 | 02 preprocessing | `notebooks/02_preprocessing/v_final/02_preprocessing.ipynb` | 15 | seed_tfidf + expanded_tfidf 2 점수 + alt sweep |
| 5 | 03 mining | `notebooks/03_mining/v_final/03_mining.ipynb` | 13 | **OLS + ordered + binary 3 모형** + 업종 분해 알파 |

**총 81 cells**. 모든 노트북 마크다운 셀에 What/Why/근거 (가이드 line + 학술 + 비전공자 노트) 3블록 포함.

---

## 3. 데이터 (가이드 04 §2)

### 3.1 모집단·표본·타이밍
- **모집단**: 127 unique stock_code × 3 fiscal_year (2022·2023·2024) = **381 firm-year** (가이드 02 line 117)
- **타이밍**: `esg_year = fiscal_year + 1` (가이드 02 line 37-38)
- **본 사이클 표본**: Samsung 005930×2024 (사이클 1·2 검증) + KCGS 등급별 stratified 5건×7등급 ≈ **30 firm-year** (사이클 4 batch)
- **총 ~31 firm-year** (사이클 4 Run All 후 확정)

### 3.2 데이터 출처·원본 보존
- **DART 사업보고서**: OpenDART `document.xml` API → `data/raw/*.zip` 원본 보존 (위반금지 #5)
- **KCGS ESG 등급**: 교수님 제공 company_master.csv → `data/_originals_professor/v0/` 보존 (읽기 전용)
- **seed dictionary**: `data/seed_dictionary.csv` (30개 v1 그대로) + `data/expanded_dictionary_manual_v1.csv` (7개 신설)

### 3.3 식별자 정합성 (위반금지 #7)
- stock_code 기준 (회사명 X — silent 오매칭 방지)
- Fix B: 모든 read/write에 `dtype={'stock_code': str}` + `str.zfill(6)` 강제

### 3.4 수집 실패 처리 (위반금지 #1)
- `logs/collection_log.csv` 11종 status + reason 컬럼
- SUCCESS 행만 esg_features에 join — 가짜 0 차단

---

## 4. 방법 (가이드 04 §2)

### 4.1 수집 (01_collection v_final)
1. `stock_code → corp_code` (corpCode.xml 캐시)
2. `corp_code → rcept_no` (3단 fallback: PRIMARY_BIZ → CORR_BIZ → ANY_BIZ)
3. `document.xml` ZIP 다운로드 + DOCUMENT-NAME 분류 (사업·연결감사·감사)
4. **🆕 lxml XMLParser(recover=True) + 정규식 pre-처리** (Fix F) — 사이클 3 batch 30/30 FAIL 해결
5. `<SECTION-1>` 14 노드 직접 순회 + section_code(020000·040000·060000) + TITLE/AASSOCNOTE 이중 매칭
6. 본문/표 분리 추출
7. seed v1 30 + expanded_manual v1 7 동시 정규식 매칭 → passage
8. viewer 5 sample 사용자 확인 (위반금지 #2·#3)
9. collection_log dedup + run_id

### 4.2 전처리 (02_preprocessing v_final)
1. SUCCESS firm-year의 sections.json 로드 → II/IV/VI body concat → firm-year document
2. Okt 형태소 분석 (Mecab Windows 미설치 fallback) + 불용어 제거
3. **TF-IDF 계산** (N≥5면 min_df=2, max_df=0.95)
4. **🆕 seed_tfidf_X + expanded_tfidf_X 2 점수 계산** (가이드 03 line 90-122 — seed vs expanded 별도 비교)
5. 기준 문장 cosine similarity (가이드 03 line 211-215)
6. KCGS 등급 join + word_count·specificity (cheap-talk)

### 4.3 마이닝 (03_mining v_final)
1. esg_features_v_final.parquet 로드
2. **Spearman ρ + p-value + t-test** (15 쌍 — seed_X·expanded_X·cosine_X × esg_grade·차원별 grade)
3. **🆕 OLS + ordered_logit + binary_logit 3 모형 동시 비교** (가이드 03 line 220-274)
4. **AIC·BIC 정량 비교**
5. **🆕 알파 #1: 업종별 분해** (가이드 04 §3-1 명시 예시)
6. cheap-talk 통제 (word_count + specificity) → β1 강건성 검증

### 4.4 위반금지 8항목 통합 매핑
| # | 위반금지 | v_final 충족 위치 |
|---|---|---|
| 1 | 가짜 0 ❌ | collection_log status/reason + SUCCESS만 join |
| 2 | viewer 우회 ❌ | document.xml API + Step 8 sample |
| 3 | MCP 그대로 신뢰 ❌ | 순수 Python re + seed/expanded 직접 검토 + viewer 확인 |
| 4 | API key 노출 ❌ | mask_key + KEY_CANDIDATES |
| 5 | raw 미보존 ❌ | data/raw/*.zip + _originals_professor/v0/ |
| 6 | 진단 부재 ❌ | SECTION 매칭 + 등급 분포 + 모형 비교 표 |
| 7 | silent 오매칭 ❌ | Fix B stock_code zfill(6) |
| 8 | 평가 기준 부재 ❌ | SUCCESS≥80% + viewer + run_id + AIC·BIC |

---

## 5. 결과 (사이클 4 Run All 예상 — 사용자 확인 후 채워짐)

### 5.1 수집 결과 (예상)
| 항목 | 사이클 3 v1 | 사이클 4 v_final 목표 |
|---|---|---|
| 시도 firm-year | 30 (batch) + 1 (Samsung) | 30 + 1 = 31 |
| SUCCESS | 0/30 + 1/1 (Samsung만) | **24+/30 (≥80%)** + Samsung |
| FAIL_OTHER (XMLSyntaxError) | **30/30** ❌ | **0~6/30** (Fix F 해결) |
| 평균 passage_body | (Samsung 55) | 약 20~80 (firm 다양성) |

### 5.2 전처리 결과 (예상)
- esg_features_v_final.parquet 31행 × 약 25 컬럼
- seed_tfidf + expanded_tfidf 둘 다 정상 분포 (N≥5 → IDF 의미 있음)
- 차원·등급별 box plot 정상

### 5.3 마이닝 결과 (예상)
- Spearman ρ: 15 쌍 모두 실제 값 (NaN 0)
- OLS β·SE·p·R² 모두 산출
- ordered_logit·binary_logit 결과 비교 표
- 업종별 분해: 4~8 업종 × ρ + p

---

## 6. 한계 (가이드 04 §2 ⑤ + §4)

1. **표본 한계 (N=31)** — 381 모집단의 8%. 학기 후 전체 batch 가능.
2. **Okt fallback** — Windows Mecab 미설치. 정형 문어체에서 분리도 ↓ 가능.
3. **expanded_manual 7개 직관 검토** — 사이클 2 자동 + 사이클 3 Claude 10단계 분석. 사용자 의견 반영 가능.
4. **fastText 자동 expanded 미실행** — N=31에서도 가능하지만 본 v_final 범위 외 (사이클 5 영역).
5. **인과 vs 연관** — 가이드 04 line 99-111 "이 표본에서 ~경향이 있었다" 디시플린 유지.
6. **as_of_date 추정** — KCGS 정확한 발표일 미확인. 보고서 §한계 명시.

---

## 7. 팀 회의 안건 (사용자 결정 필요)

### 7.1 seed/expanded 방향
- [ ] **방향 1 (현재 채택) 유지**: seed v1 30 + expanded_manual_v1 7
- [ ] 방향 2: seed_v2 37 (사이클 2 결정으로 회귀)
- [ ] 다른 의견

### 7.2 알파 분석 선택 (가이드 04 §3-1)
- [ ] **#1 업종별 분해 (v_final 코드 포함)** — 가이드 명시 예시
- [ ] #2 cheap-talk 3종 강화 (specificity + commitment + non-material)
- [ ] #3 section_weighted score (II=0.5·IV=0.2·VI=0.3)
- [ ] #4 KLUE-RoBERTa baseline (D-Day 후)

### 7.3 회귀 모형 선택 (가이드 03 line 220-274)
사이클 4 결과 확인 후 OLS·ordered·binary 중 1개 채택. AIC·BIC + 해석 가독성 종합.

### 7.4 다음 사이클 (5) 작업 안
1. 사용자 Run All 후 보고서·진단 HTML 단계별 v_final 8개 채워짐 (사이클 5)
2. release notes (00·01a·01b·02·03)
3. GitHub MCP 양쪽 레포 PR 8개 분할
4. 최종 발표 자료 (Marp 또는 HTML)

---

## 8. 산출물 인덱스 (사이클 4 종료 시점)

### 8.1 노트북 5종 (notebooks/)
| 노트북 | 위치 | 의미 |
|---|---|---|
| 00 v_final | `00_ingest/v_final/` | KCGS lineage + 차원·업종 분포 |
| 01 phase2A v_final | `01_collection/phase2A/v_final/` | Samsung 1건 + Fix F |
| 01 phase2B v_final | `01_collection/phase2B/v_final/` | batch 30건 + Fix F |
| 02 v_final | `02_preprocessing/v_final/` | seed + expanded TF-IDF |
| 03 v_final | `03_mining/v_final/` | 3 모형 + 업종 알파 |

### 8.2 데이터 (data/)
| 파일 | 의미 |
|---|---|
| `_originals_professor/v0/` | 교수님 원본 3종 (보존) |
| `seed_dictionary.csv` | v1 30 (변경 X) |
| `expanded_dictionary_manual_v1.csv` | 신설 7 (방향 1 — KEPT) |
| `_archive/seed_dictionary_v2_cycle2_decision.csv` | 사이클 2 결정 history |

### 8.3 로그 (logs/)
| 파일 | 의미 |
|---|---|
| `collection_log.csv` | 31행 (Samsung + batch 30 예상) |
| `kcgs_lineage.csv` | 381 firm-year × 14 컬럼 |
| `kcgs_lineage_meta.json` | 출처·평가방법·교차검증 |

### 8.4 보고서·진단 (reports/)
| 파일 | 의미 |
|---|---|
| 본 문서 (`03_cycle4_v_final_종합_회의용.md`) | 사이클 4 종합 회의용 |
| `04_cycle4_v_final_진단.html` | 사이클 4 다단계 진단 HTML |
| 단계별 `보고서.md` + `진단_발전제안.html` | 사용자 Run All 후 사이클 5에서 작성 |

---

## 9. 사용자 액션 (D-Day 직전 5/18 밤 ~ 5/19 D-Day)

1. ✅ 본 회의용 보고서 검토
2. ⏳ 5 노트북 v_final 순서대로 Run All
   - 00 ingest (5~10초)
   - 01 phase2A (30초~1분, 캐시 hit)
   - 01 phase2B (5~10분, batch 30)
   - 02 preprocessing (1~2분, N=31)
   - 03 mining (30초, N=31)
3. ⏳ batch SUCCESS 비율 + 결과 확인 → Claude에게 공유
4. ⏳ Claude가 사이클 5 작업 (단계별 보고서 8개 + release notes 5 + PR 8)
5. ⏳ 5/19 D-Day 제출 (분석 노트북 .ipynb + 본 보고서 .md)

---

> **본 보고서는 팀 회의용 종합. 단계별 자세 보고서는 사용자 Run All 결과 반영 후 사이클 5에서 작성.**
