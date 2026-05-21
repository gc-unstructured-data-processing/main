# GitHub MCP PR 8개 분할 안 — 사이클 4·5 v_final 통합

> **작성**: 이동원 · **2026-05-18**
> **목적**: 사이클 4·5 모든 산출물을 양쪽 레포 (origin + team)에 작업 단위 PR로 분할 push
> **메모리 근거**: `reference_two_repos.md` + `reference_github_mcp_workflow.md` (작업 단위 분리)

---

## 양쪽 레포

| 레포 | URL | 역할 |
|---|---|---|
| origin | https://github.com/mygithub05253/unstructured-data-processing-final-project | 이동원 개인 1차 작업 |
| team | https://github.com/gc-unstructured-data-processing/main | 가천대 organization 최종 |

각 PR은 origin·team 양쪽 동일하게 진행 (history 충돌 시 `reference_two_repos.md` 절차 따름).

---

## PR 8개 분할

### PR #1 — `docs(reports): cycle 4·5 종합 보고서·진단 HTML`
**포함**:
- `members/이동원/reports/03_cycle4_v_final_종합_회의용.md`
- `members/이동원/reports/04_cycle4_v_final_진단.html`
- `members/이동원/reports/05_cycle5_v_final_실측_회의용_v2.md` ⭐
- `members/이동원/reports/RELEASE_NOTES_v_final.md`
- `members/이동원/reports/PR_BREAKDOWN.md` (본 문서)
- `members/이동원/reports/01_cycle3_종합진단_seed결정_FAIL진단.md`

**우선순위**: 🔴 즉시 (가장 중요한 회의용 문서)

---

### PR #2 — `feat(00): ingest_kcgs v_final + lineage + 시각 3종`
**포함**:
- `members/이동원/notebooks/00_ingest/v_final/00_ingest_kcgs.ipynb` (17 cells)
- `members/이동원/reports/00_ingest/v_final/보고서.md`
- `members/이동원/reports/00_ingest/v_final/진단_발전제안.html` (image embed)
- `logs/kcgs_lineage.csv` (381×15)
- `logs/kcgs_lineage_meta.json`
- `data/processed/fig_v_final_kcgs_grade_year.png`
- `data/processed/fig_v_final_kcgs_dim.png`
- `data/processed/fig_v_final_kcgs_industry.png`

**우선순위**: 🟢 사이클 4 작업

---

### PR #3 — `feat(01a): collection phase2A v_final + Fix F`
**포함**:
- `members/이동원/notebooks/01_collection/phase2A/v_final/01_collection.ipynb` (23 cells)
- `members/이동원/reports/01_collection/phase2A/v_final/보고서.md`
- `members/이동원/reports/01_collection/phase2A/v_final/진단_발전제안.html`

**중심 변경**: Fix F (recover XML + 정규식 pre-처리). Samsung 1건은 v2 결과 그대로 SUCCESS.

---

### PR #4 — `feat(01b): collection phase2B v_final batch 28/30 SUCCESS`
**포함**:
- `members/이동원/notebooks/01_collection/phase2B/v_final/01_collection.ipynb` (13 cells)
- `members/이동원/reports/01_collection/phase2B/v_final/보고서.md`
- `members/이동원/reports/01_collection/phase2B/v_final/진단_발전제안.html`
- `logs/checkpoint_batch_{10,20,30}.csv`
- `data/processed/fig_v_final_batch_status.png`
- `logs/collection_log.csv` (112행 누적, v_final 31행)

**핵심 성과**: 사이클 3 30/30 FAIL → 사이클 4 28/30 SUCCESS (Fix F 효과 검증)

**우선순위**: 🟢 사이클 4 작업

**⚠️ 주의**: `data/raw/*.zip` 30개 + `data/interim/*_sections.json` 30개는 **.gitignore 적용** (대용량). PR에 포함 X. 검증은 sections.json 1개 sample만 포함하거나 별도 zenodo 등에 업로드.

---

### PR #5 — `feat(02): preprocessing v_final — seed + expanded TF-IDF`
**포함**:
- `members/이동원/notebooks/02_preprocessing/v_final/02_preprocessing.ipynb` (15 cells)
- `members/이동원/reports/02_preprocessing/v_final/보고서.md`
- `members/이동원/reports/02_preprocessing/v_final/진단_발전제안.html`
- `data/seed_dictionary_v2_proposed.csv` (02b 산출)
- `data/expanded_dictionary_manual_v1.csv` (방향 1, 7개)
- `data/processed/esg_features_v_final.parquet/.xlsx` (29×25)
- `data/processed/fig_v_final_preprocess.png`
- `data/processed/seed_v2_decision_analysis.csv`

**핵심**: 방향 1 채택 — seed v1 30 + expanded_manual 7

---

### PR #6 — `feat(03): mining v_final — Spearman·OLS·ordered·binary + 알파`
**포함**:
- `members/이동원/notebooks/03_mining/v_final/03_mining.ipynb` (13 cells)
- `members/이동원/reports/03_mining/v_final/보고서.md`
- `members/이동원/reports/03_mining/v_final/진단_발전제안.html`
- `data/processed/regression_results_v_final.csv` (19행)
- `data/processed/fig_v_final_mining_spearman.png`
- `data/processed/fig_v_final_mining_industry.png`

**핵심 발견**: seed_tfidf_E ↔ ESG ρ=0.606 (p<0.001) ⭐. OLS β=7.36 (p=0.029), R²=0.295.

**우선순위**: 🔴 가장 중요한 결과 PR

---

### PR #7 — `chore: 폴더 재정비 + 원본 데이터 보존 + archive`
**포함**:
- `members/이동원/notebooks/README.md` (인덱스)
- `members/이동원/reports/README.md` (인덱스)
- `data/_originals_professor/README.md` + `v0/` 3 파일 (교수님 원본)
- `data/_archive/seed_dictionary_v2_cycle2_decision.csv` (사이클 2 history)
- 폴더 구조 재정비: `phase/version` 이중 하위 + notebooks·reports 1:1

**우선순위**: 🟡 사이클 5 작업 (구조 변경 — 큰 PR)

---

### PR #8 — `docs: 단계별 v_final 보고서·진단 5쌍 + 메모리 업데이트`
**포함**:
- 5 단계별 보고서.md + 진단_발전제안.html (사이클 5 산출)
- 메모리 파일 업데이트 (`project_seed_v2_decisions.md` 등)

**우선순위**: 🟡 사이클 5 마지막 작업

---

## 양쪽 레포 동기화 절차 (각 PR마다)

메모리 `reference_two_repos.md` 따라:

1. `git checkout -b feature/cycle4-PR-N` (origin·team 동일 branch 명)
2. 변경 파일 stage + commit (message 동일)
3. `git push origin feature/cycle4-PR-N`
4. `git push team feature/cycle4-PR-N`
5. `mcp__github__create_pull_request` × 2 (origin + team)
6. `mcp__github__merge_pull_request(merge_method='squash')` × 2
7. 메모리 `project_team_workspaces.md`의 "커밋된 PR 기록" 섹션에 양쪽 PR 번호 추가

⚠️ team repo 'history 공통 없음' 422 에러 시 cherry-pick 또는 사용자 확인 후 force-sync (`reference_two_repos.md` "team repo 대응" 섹션).

---

## .gitignore 보강 (PR #2~6에 포함 권장)

```
# 대용량 raw·interim
data/raw/*.zip
data/interim/*_sections.json
data/interim/*_aux_*.json

# 사이클 임시
*.ipynb.repaired.json
logs/checkpoint_batch_*.csv
logs/collection_log.csv.bak_*

# 캐시
data/cache/
.venv/
__pycache__/
```

단 `data/processed/fig_v_final_*.png`·`esg_features_v_final.*`·`regression_results_v_final.csv` 등 최종 산출은 git에 포함 (재현성 검증용).

---

## 사용자 액션 (PR 진행 순서)

1. 본 PR_BREAKDOWN 검토 — 분할 안 동의 시 진행
2. Claude가 `mcp__github__*` 도구로 PR #1부터 순차 진행
3. 각 PR 머지 후 메모리 업데이트
4. 8개 모두 완료 후 양쪽 레포 main SHA 일치 확인

---

> **본 분할 안은 메모리 reference_github_mcp_workflow + reference_two_repos 100% 부합. 사용자 confirm 후 진행.**
