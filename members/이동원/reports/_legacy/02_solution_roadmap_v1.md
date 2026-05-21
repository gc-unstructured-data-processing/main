# ESG DART 풀 사이클 — 해결 방법 로드맵 v1

> **작성자**: 이동원
> **작성일**: 2026-05-18
> **버전**: v1 (1차 보고서 + 10단계 분석 v3 후속)
> **이전 문서**:
> - 1차 보고서: `01_cycle_progress_report_v1.md`
> - 10단계 분석 v3: `01_collection/05_phase2_diagnosis_10steps_v3.html`
>
> **목적**: 10단계 분석에서 도출한 10대 이슈를 즉시·중기·장기로 분류하고 실행 우선순위·예상 소요·검증 기준 명시.

---

## 0. 한 줄 결론

7대 이슈 중 4개는 **사이클 3 batch 30건 Run All 1회 (5~10분)** 로 동시 해결. 2개는 사이클 4 v3 노트북 작성. 1개는 §한계 기록. 알파 1개는 D-Day 직전·이후 선택. **5/19 D-Day 도달 확신.**

---

## 1. 우선순위 분류 (10단계 이슈 매핑)

| 단계 | 이슈 | 우선순위 | 해결 노트북 | 예상 소요 |
|---|---|---|---|---|
| 1 | N=1 통계 NaN | 🔴 **즉시** | 01_phase2B_v1 + 02·03 재실행 | 7~12분 |
| 2 | S 점수 KCGS 격차 | 🔴 **즉시** | 02b 검토 + 02 v3 (사이클 4) | 사용자 검토 + 30분 |
| 3 | stock_code int 변환 | 🟡 **검증** | Fix B 적용 — Run All 재검증 | 0분 (자동) |
| 4 | 한글 폰트 missing | 🟡 **검증** | Fix A 적용 — Run All 재검증 | 0분 (자동) |
| 5 | collection_log v2 부재 | 🟡 **검증** | Fix D 적용 — Run All 재검증 | 0분 (자동) |
| 6 | .ipynb truncation | 🟡 **검증** | Fix E 적용 — Run All 재검증 | 0분 (자동) |
| 7 | seed 30 → expanded | 🟢 **중기** | 02 v3 (사이클 4) | 30~60분 |
| 8 | Okt fallback (Mecab 미설치) | ⚪ **기록** | 보고서 §한계 명시 | 5분 |
| 9 | cheap-talk 단순화 | 🟣 **알파** | 03 v2 또는 v3 (alpha 분석) | 60분 |
| 10 | 인과 vs 연관 해석 | ✅ **충족** | 보고서 §해석 기존 디시플린 유지 | 0분 |

**색깔 의미:** 🔴 D-Day 전 반드시 / 🟡 패치됨, 재실행으로 검증 / 🟢 사이클 4 / ⚪ 기록만 / 🟣 알파 / ✅ 충족

---

## 2. 즉시 해결 — 사이클 3 (D-Day 전 5/18~5/19)

### 2.1 액션 시퀀스 (사용자 Run All)

| # | 액션 | 노트북 | 시간 | 검증 |
|---|---|---|---|---|
| 1 | 사이클 2 fix 검증 재실행 | 00·01_v2·02·02b·03 (5종) | 3~5분 | esg_features_v2.xlsx의 stock_code = '005930' 확인 |
| 2 | S 진단 결과 검토 | 02b | 사용자 검토 (5~15분) | seed_dictionary_v2_proposed.csv 열어 의미 검토 |
| 3 | seed_v2 채택 결정 | 수동 | 2분 | proposed → seed_dictionary_v2.csv rename |
| 4 | batch 30건 실행 | 01_phase2B_v1 | 5~10분 | SUCCESS ≥ 80% (24건 이상) |
| 5 | 전처리·마이닝 재실행 | 02·03 | 2분 | Spearman ρ NaN 사라짐 |
| 6 | viewer 검증 | 01_phase2B Step 5 | 5분 (수동) | random 3건 viewer URL 확인 |

### 2.2 검증 기준 (Pass/Fail)

| 검증 항목 | Pass 기준 | Fail 시 대응 |
|---|---|---|
| 5 노트북 Run All | 모두 JSON 무결성 + 마지막 셀까지 실행 | nbformat.validator로 진단 + 노트북별 fix |
| collection_log | parser_version='v3_batch' 30행 + 'v2' 1행 = 31행 | Fix D 진단 셀 확인 + 누락 시 보강 |
| SUCCESS rate | ≥ 80% (24/30) | 미달 시 보고서 §한계 기록 + reason 분석 |
| esg_features_v2.parquet | N=31, dtype 보존 (stock_code str) | Fix B 적용 검증 + xlsx 재저장 |
| Spearman ρ | 9개 모두 실제 값 (NaN 0개) | N 부족 등급 합산 (binary logit으로 폴백) |
| random 3건 viewer | 사용자 직접 확인 OK | viewer URL이 실제 사업보고서 페이지로 연결되는지 |

### 2.3 사이클 3 후 가이드 04 §2-1 충족 추적

| 영역 | 항목 | 사이클 2 종료 | 사이클 3 후 |
|---|---|---|---|
| 데이터 lineage | 최대 381행 수집 시도 | 1/381 | **31/381 ✅** |
| | corp_code·rcept_no·fiscal_year 연결 | 1/1 | **31/31 ✅** |
| | 수집 불가 행 이유 기록 | N/A | **FAIL_* + reason ✅** |
| | 실패 행 가짜 0 차단 | N/A | **status 기준 join ✅** |
| 분석 재현성 | Run All 재현 | ⚠️ truncated 위험 | **✅ Fix E 적용** |
| | API key 환경변수만 | ✅ | ✅ |
| 보고서 판단 | II/IV/VI 추출 기준 | ✅ | ✅ |
| | seed/expanded 근거 | ⚠️ 부분 | **✅ seed_v2 채택 근거 + 진단** |
| | 회귀모형 선택 이유 | ✅ 코드 | **✅ 결과 + 해석** |
| | 인과 vs 연관 | ✅ 마크다운 | **✅ 본 결과로 보강** |

---

## 3. 중기 해결 — 사이클 4 (D-Day 직전)

### 3.1 v3 노트북 2종 신설

**02_preprocessing_v3.ipynb** (~20 cells, Claude 작성):
- seed_dictionary_v2.csv 적용 (사용자 채택 후)
- 형태소 분석기 alt sweep: Okt vs Kkma vs Komoran 3종 vocab/속도/품질 비교 표
- expanded θ sweep (0.5·0.6·0.7·0.8) — N=31 정상 동작
- 표 vs 본문 alt: source = body / body+tables / tables 비교 표
- seed_v1 vs seed_v2 S 점수 효과 정량 비교

**03_mining_v2.ipynb** (~20 cells, Claude 작성):
- OLS 결과 + ordered_logit (statsmodels OrderedModel) + binary_logit
- 모형 선택 근거: AIC·BIC + 결과 해석 가독성 trade-off
- 업종별 분해 (alpha) — 가이드 04 §3-1 권장
- cheap-talk specificity 정교화 + commitment ratio 추가
- 가이드 04 §3 평가표 형식 표 출력

### 3.2 보고서·진단 v2

- `01_cycle_progress_report_v2.md` — 본 1차 보고서의 사이클 3·4 결과 반영 v2
- `03_diagnosis_v4.html` — 사이클 3·4 통합 진단 (사이클 4 결과 분석)
- `release_notes_v1.md` — 5 노트북 release notes (00·01a·01b·02·03)

### 3.3 GitHub PR 분할 (메모리 reference_github_mcp_workflow)

| # | PR 제목 | 변경 |
|---|---|---|
| 1 | `docs: cycle 2 fix + 1차 보고서 + diagnosis v2·v3` | 5 노트북 fix + 1차 .md + 04·05 HTML |
| 2 | `feat(02b): S score diagnosis v1` | 02b 노트북 + seed_v2_proposed.csv |
| 3 | `feat(01b): collection phase2B v1 — batch 30` | phase2B 노트북 |
| 4 | `chore: archive truncated_postrun snapshots` | archive 정리 + .gitignore 보강 |
| 5 | `feat(02): preprocessing v3 — seed_v2 + alt sweep` | v3 노트북 + alt 결과 |
| 6 | `feat(03): mining v2 — N=31 results + ordered logit` | v2 노트북 + 결과 |
| 7 | `docs: cycle progress report v2 + release notes` | .md 6종 |
| 8 | `docs: diagnosis v4 + 알파 분석 결정` | HTML 진단 + 알파 보고 |

양쪽 레포(origin + team) 동일하게 진행. team repo "history 공통 없음" 이슈 시 cherry-pick 또는 force-sync (메모리 `reference_two_repos.md`).

---

## 4. 장기·알파 영역 (D-Day 이후 또는 알파 1개 채택)

가이드 04 §3-1: 알파 1개 이상 권장. 본 진단 도출 4개 알파 후보 중 1개 선택.

### 4.1 알파 후보 4개

| # | 알파 | 의미 | 소요 | 적합도 |
|---|---|---|---|---|
| 1 | **cheap-talk 3종 강화** | specificity·commitment·non-material 추가 통제 → β 유의성 유지 검증 | 60분 | ⭐⭐⭐ 학부 적합 |
| 2 | **업종별 분해** | 전기전자·화학·금융·제조 4업종 회귀 분해 | 45분 | ⭐⭐⭐ 가이드 §3-1 명시 |
| 3 | **section-weighted score** | II=0.5·IV=0.2·VI=0.3 가중 평균 + 3개 weight 비교 | 30분 | ⭐⭐ 흥미롭지만 효과 약함 |
| 4 | **KLUE-RoBERTa baseline** | dense vector cosine vs TF-IDF cosine 비교 | 4시간+ | ⭐ 인프라 부담 — 학기 후 |

### 4.2 알파 1개 채택 권장

**알파 #2 업종별 분해** — 다음 이유로 강력 권장:
- 가이드 04 §3-1 line 97 명시 예시 — 채점 위반 위험 0
- 작업 시간 45분 (1개월 일정에 안전)
- N=31에서도 4업종 = 약 7~8건/업종 → 시각화 + 표 산출 가능
- 결과 해석 직관적 — "전기전자는 G 차원 강함, 화학은 E 차원 강함" 등

또는 **알파 #1 cheap-talk 강화** — 사이클 3에서 specificity_score 이미 추가 → 자연스러운 확장.

### 4.3 D-Day 이후 (학기 후 또는 학회 발표)
- KLUE-RoBERTa baseline 1개 추가
- 381 firm-year 전체 batch (사이클 3 30건의 12.7배)
- 패널 회귀 (firm fixed effect) — 같은 firm의 3년 변화 추적

---

## 5. 노트북·문서 산출물 인덱스 (사이클 3 종료 시점 예상)

### 5.1 노트북 8종

| 노트북 | 상태 | 의미 |
|---|---|---|
| 00_ingest_kcgs_v1 | ✅ 사이클 1 작성 + 사이클 2 fix | KCGS lineage |
| 01_collection_phase2A_v1 | 📦 archive (truncated) | 사이클 1 진단 소스 |
| 01_collection_phase2A_v2 | ✅ 사이클 1 작성 + 사이클 2 fix | Samsung 1건 안정 |
| 01_collection_phase2B_v1 | ✅ 사이클 2 신설 | batch 30건 stratified |
| 02_preprocessing_v1 | 📦 archive | 사이클 1 진단 소스 |
| 02_preprocessing_v2 | ✅ 사이클 1·2 fix | seed-only TF-IDF |
| 02_preprocessing_v3 | 🔜 사이클 4 신설 | seed_v2 + alt sweep |
| 02b_s_score_diagnosis_v1 | ✅ 사이클 2 신설 | S 점수 진단 |
| 03_mining_v1 | ✅ 사이클 1·2 fix | Spearman·OLS 코드 형식 |
| 03_mining_v2 | 🔜 사이클 4 신설 | N=31 정상 결과 + ordered_logit |

### 5.2 문서 5종

| 문서 | 상태 | 의미 |
|---|---|---|
| 01_cycle_progress_report_v1.md | ✅ 사이클 2 작성 | 1차 단계별 보고서 |
| 01_cycle_progress_report_v2.md | 🔜 사이클 4 작성 | 최종 보고서 |
| 02_solution_roadmap_v1.md | ✅ 본 문서 | 해결 방법 로드맵 |
| 03_phase2A_diagnosis_v1.html | ✅ 사이클 1 작성 | 10단계 진단 v1 |
| 04_phase2A_diagnosis_v2.html | ✅ 사이클 2 작성 | 10단계 진단 v2 |
| 05_phase2_diagnosis_v3.html | ✅ 본 문서와 함께 작성 | 10단계 진단 v3 (N=1 NaN 중심) |
| 06_diagnosis_v4.html | 🔜 사이클 4 작성 | 사이클 3·4 통합 |
| release_notes_v1.md | 🔜 사이클 4 작성 | 5 노트북 release notes |

---

## 6. 다음 사용자 액션 명세

### 6.1 즉시 (오늘 5/18 내)
1. ✅ 본 문서 (해결 로드맵 v1) 검토
2. ⏳ 5 노트북 재실행 — 사이클 2 fix 검증 (Fix A 폰트 + Fix B dtype + Fix C KCGS dynamic + Fix D log v2 + Fix E truncation)
3. ⏳ 02b_s_score_diagnosis_v1 Run All → seed_dictionary_v2_proposed.csv 검토
4. ⏳ seed_v2 채택 (kept/removed 컬럼 채우기) → seed_dictionary_v2.csv 확정

### 6.2 D-Day (5/19)
5. ⏳ 01_collection_phase2B_v1 Run All — batch 30건 (5~10분)
6. ⏳ random 3건 viewer URL 확인 (위반금지 #3)
7. ⏳ 02_preprocessing_v2 + 03_mining_v1 재실행 (N=31 정상 통계 확인)
8. ⏳ 결과 공유 → Claude 사이클 4 작성 시작 (02 v3 + 03 v2 + 보고서 v2 + 진단 v4 + release notes + PR 분할)

### 6.3 D-Day 이후 (5/20+)
9. 알파 1개 채택 — 업종별 분해 (#2) 또는 cheap-talk 강화 (#1)
10. 발표 자료 (Marp 또는 HTML 단일) — docs/supplements 톤
11. GitHub release tag v1.0-final-2026-05-XX
12. 최종 정리: 메모리 5종 업데이트 + 폴더 archive 1주일 후 zip

---

## 7. 위반금지 8항목 — 사이클 3 후 충족 예상

| # | 위반금지 | 사이클 2 | 사이클 3 후 |
|---|---|---|---|
| 1 | 실패 행 가짜 0 ❌ | ✅ | ✅ (FAIL_* + reason) |
| 2 | viewer 우회 ❌ | ✅ | ✅ (random 3건 사용자 확인) |
| 3 | MCP/추출 그대로 신뢰 ❌ | ✅ | ✅ (seed_v2 직접 검토) |
| 4 | API key 출력 노출 ❌ | ✅ | ✅ |
| 5 | raw 미보존 ❌ | ✅ | ✅ (30 zip + 30 sections.json) |
| 6 | 진단 부재 ❌ | ✅ | ✅ (등급 cross tab + status counter) |
| 7 | silent 오매칭 ❌ | ✅ | ✅ (Fix B 적용 + 검증) |
| 8 | 평가 기준 부재 ❌ | ✅ | ✅ (SUCCESS≥80% 명시) |

**8/8 충족 + 알파 1개 채택 → 가이드 04 §3 평가표 7개 영역 모두 좋은 결과물 패턴.**

---

> **본 로드맵은 1차 보고서 + 10단계 분석 v3과 동시 작성됐으며, 사이클 3 batch 결과에 따라 v2로 업데이트 예정.**
