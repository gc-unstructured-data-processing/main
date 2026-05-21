# 사이클 4·5 v_final 통합 Release Notes

> **작성**: 이동원 · **2026-05-18**
> **사이클**: 4 (노트북) + 5 (실측 보고서) — D-Day 직전 통합

---

## 00 ingest v_final

**변경 사항** (v1 → v_final):
- 🆕 차원별 (E·S·G) 등급 분포 시각화 추가
- 🆕 업종 × 등급 cross tab + heatmap 추가
- 🆕 stratified sample 함수 + A 이상 binary fallback
- 🔧 Fix A·B·E 통합 적용 (한글 폰트·dtype·display)

**실측 결과**: kcgs_lineage.csv 381×15. 등급 분포: A(123) · B+(76) · D(64) · C(53) · B(36) · A+(29) · S(0). 22 unique 업종.

**산출**: `notebooks/00_ingest/v_final/00_ingest_kcgs.ipynb` (17 cells) + `logs/kcgs_lineage.csv` + 시각 3종 + `reports/00_ingest/v_final/{보고서.md, 진단_발전제안.html}`

---

## 01 collection phase2A v_final

**변경** (v2 → v_final):
- 🆕 lxml `XMLParser(recover=True)` + 정규식 `&` escape pre-처리 (Fix F) — phase2B batch 핵심
- 🆕 seed v1 30 + expanded_manual v1 7 동시 매칭 (방향 1)
- 🆕 run_id에 git_sha 추가

**실측 결과** (Samsung 2024): status=SUCCESS, SECTION-1 14/14, n_passages_body=55. Samsung은 well-formed XML이라 recover/strict 결과 동일.

**산출**: 23 cells + `data/raw/005930_2024_disclosure.zip` (660KB) + sections.json (2.8MB) + 보고서·진단 1쌍.

---

## 01 collection phase2B v_final

**변경** (v1 → v_final):
- 🆕 Fix F 적용 — recover XML parser
- 🆕 incremental checkpoint 매 10건 (collection_log flush)
- 🆕 SUCCESS≥80% 평가 기준 명시

**실측 결과** (batch 30):
- ⭐ **SUCCESS 28/30 (93.3%)** — 위반금지 #8 통과
- WARN_NO_PASSAGES 2 (010130 LG화학, 000480 CR홀딩스)
- **FAIL_OTHER 0/30 — Fix F 완전 효과** (사이클 3 30/30 FAIL → 사이클 4 0/30)

**산출**: 13 cells + raw zip 30개 + sections.json 30개 + checkpoint 3개 + `fig_v_final_batch_status.png` + 보고서·진단 1쌍.

---

## 02 preprocessing v_final

**변경** (v2 → v_final):
- 🆕 seed_tfidf + expanded_tfidf 2 점수 동시 계산 (방향 1)
- 🆕 N≥5 시 min_df=2·max_df=0.95 자동 조정 (가이드 03 line 56 stopwords 정신)
- 🆕 형태소 분석기 4종 가용성 확인 (Okt PRIMARY, Mecab fallback)

**실측 결과** (N=29):
- esg_features_v_final.parquet 29×25
- seed_tfidf E·S·G 평균: 0.034 · **0.012** · 0.147 (S 차원 여전히 약함)
- expanded_S 평균 0.021 — manual 6개 추가 효과 (50~70% 증가)
- specificity 평균 0.223

**산출**: 15 cells + esg_features_v_final.parquet/xlsx + `fig_v_final_preprocess.png` + 보고서·진단 1쌍.

---

## 03 mining v_final

**변경** (v1 → v_final):
- 🆕 OLS + ordered_logit + binary_logit 3 모형 동시 비교 (가이드 03 line 220-274)
- 🆕 AIC·BIC 정량 비교
- 🆕 알파 #1 업종별 분해 (가이드 04 §3-1)

**⭐ 실측 결과** (N=29):
- **seed_tfidf_E ↔ esg_grade_num: Spearman ρ = 0.606, p = 0.0005** ⭐ 강한 유의
- cosine_E ↔ ESG: ρ = 0.525, p = 0.003 ⭐
- cosine_S ↔ ESG: ρ = 0.427, p = 0.021 ⭐
- OLS_seed_E: β₁=7.365, p=0.029, R²=0.295 ⭐ baseline 채택 권장
- BinaryLogit (A이상): β₁=41.09, p=0.075, pseudo-R²=0.364 (약한 효과)
- OrderedLogit: 불안정 (N=29 + 6 등급 자유도 부족)

**산출**: 13 cells + regression_results_v_final.csv (19행) + spearman·industry 시각 2종 + 보고서·진단 1쌍.

---

## 사이클 4·5 종합 진단 문서

- `reports/03_cycle4_v_final_종합_회의용.md` (사이클 4, Run All 전 예상)
- `reports/04_cycle4_v_final_진단.html` (사이클 4, 6 tab)
- `reports/05_cycle5_v_final_실측_회의용_v2.md` ⭐ (사이클 5, **실측 100% 기반**)

---

## 위반금지 8/8 충족 (사이클 5 실측)

1. ✅ 가짜 0 차단 — SUCCESS 29만 esg_features에 join
2. ✅ viewer 우회 — Samsung 5 + batch random 3 sample
3. ✅ MCP 그대로 신뢰 — seed_v2 9 후보 Claude 10단계 검토
4. ✅ API key 노출 — mask_key + KEY_CANDIDATES
5. ✅ raw 미보존 — data/raw/*.zip 31개 + interim/*_sections.json 31개
6. ✅ 진단 부재 — SECTION 매칭 + status counter + 모형 비교
7. ✅ silent 오매칭 — Fix B stock_code zfill(6)
8. ✅ 평가 기준 부재 — SUCCESS≥80% (실측 93.3%) + AIC·BIC

## 가이드 04 §3 평가표 7개 영역 100% 충족

데이터 이해 · DART lineage · 텍스트 처리 · 측정 validity · 모형 선택 · 해석과 한계 · 알파 — 모두 v_final로 충족.

---

> 사이클 5 종료 — D-Day 5/19 제출 준비 완료. GitHub MCP PR 분할은 별도 문서 (`reports/PR_BREAKDOWN.md`).
