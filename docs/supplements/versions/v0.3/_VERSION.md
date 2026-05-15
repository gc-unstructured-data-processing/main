# Supplements 버전 관리 — v0.3

> 작성일: 2026-05-15 (v0.2 동일자, 후속 정책 반영)
> 작성 단계: 데이터 수집 진행 중 + 노트북 운영 규칙 정식화

## 이 버전에 포함된 산출물

| 파일 | 목적 | 대상 독자 |
|---|---|---|
| `COLLECTION_데이터수집가이드_v0.3.html` | v0.2 COLLECTION의 업데이트 — nbstripout 제거 + 노트북 6 규칙 + 출력 보존 정책 + API key 안전 강화 + archive 컨벤션 + tqdm/시각화 예제 | 팀 4명 공통 |

## v0.2 → v0.3 변경 사항

| 항목 | v0.2 | v0.3 |
|---|---|---|
| nbstripout 사용 | ✅ 권장 (`nbstripout --install`) | ❌ **금지** (출력 보존 정책) |
| 노트북 출력 GitHub 커밋 | 제거 (nbstripout) | ✅ **유지** (재현·비교용) |
| API key 안전 수칙 | `.env` 사용 + URL 출력 금지 | + `mask_key()` 헬퍼 함수 + `<MASKED>` placeholder (출력 보존 환경 대응) |
| 노트북 버전 관리 | git history만 | + `notebooks/archive/` 폴더 (rollback용 스냅샷) |
| 진행률 표시 | tqdm | + ipywidgets (tqdm.notebook 사용) |
| 결과 시각화 | 선택 | **의무** (matplotlib·seaborn·plotly·wordcloud) |
| 마크다운 셀 | 선택 | What/Why/근거 3블록 의무 |
| 노트북 6 규칙 | 미정의 | ✅ 정식 규칙 6개 합의 |

## v0.2 산출물과의 관계

- `v0.2/COLLECTION_데이터수집가이드.html` — **base 데이터 수집 워크플로우** 유지 (Phase 1 파일럿, Phase 2 배치, 크롤링 매트릭스). 단, nbstripout 관련 안내는 **무효**.
- `v0.2/ROADMAP_5일_데드라인.html` — 5/15~5/19 일정 그대로 유효.
- 본 `v0.3/COLLECTION_v0.3.html` — v0.2 + 노트북 운영 규칙 delta. 두 버전을 함께 참조.

## 합의된 결정 사항 (v0.3)

- **노트북 6 규칙**: 모든 .ipynb 파일에 적용 (members/README.md + _TEMPLATE_노트북_표준헤더.md)
- **nbstripout 제거**: pyproject.toml + requirements.txt에서 삭제됨 (PR #9 / org PR #3)
- **출력 보존 의무**: 노트북 셀 출력은 GitHub commit에 유지. API key 노출 방지는 코드 레벨에서 처리.
- **archive/ 컨벤션**: `members/{이름}/notebooks/archive/{원본명}_{YYYY-MM-DD}_{descriptor}.ipynb` 스냅샷으로 rollback 가능성 확보.
- **표준 헤더**: `members/_TEMPLATE_노트북_표준헤더.md`를 모든 새 노트북 첫 셀에 적용.

## 위반 금지 체크리스트 (v0.3가 지키는 가이드)

- [x] 모든 크롤링 경로에 출처·lineage 기록 (v0.2 계승)
- [x] document.xml이 표준 raw 텍스트 경로 (v0.2 계승)
- [x] MCP는 발견·연습용, corpus 투입 전 Python 재현 검증 (v0.2 계승)
- [x] API key 코드 노출 없음 (.env만) + **출력 노출도 없음** (v0.3 신규 강조)
- [x] rate limit·backoff·캐시 적용 (v0.2 계승)
- [x] 실패 행은 collection_log.csv에 기록, 가짜 0 금지 (v0.2 계승)
- [x] stock_code 기준 join, esg_year = fiscal_year + 1 (v0.2 계승)
- [x] **노트북 버전·출력 보존, 진행률 시각화, 결과 시각화, What/Why/근거 마크다운** (v0.3 신규)
