# Supplements 버전 관리 — v0.2

> 작성일: 2026-05-15 (v0.1 동일자, 후속 작업 시작)
> 작성 단계: 데이터 수집 단계 진입 (Phase 1 파일럿 준비)

## 이 버전에 포함된 산출물

| 파일 | 목적 | 대상 독자 |
|---|---|---|
| `COLLECTION_데이터수집가이드.html` | 웹 크롤링 개념(static/dynamic, requests/BS4 vs API vs MCP) + 4-track 벤치마킹(강의·공개코드·실무·논문) + DART 수집 파이프라인(Phase 1 파일럿 + Phase 2 배치 설계) + 크롤링 허용 매트릭스 | 팀 4명 공통 |

## v0.1 → v0.2 변경 사항

| 항목 | v0.1 | v0.2 |
|---|---|---|
| 분석 단계 | ✅ 완료 (ANALYSIS_프로젝트분석.html) | 유지 |
| 역할 분담 | ✅ 완료 (ROLES_역할분담재설계.html) | 유지 |
| 데이터 수집 가이드 | ❌ 없음 | ✅ COLLECTION HTML 추가 |
| pyproject.toml | ❌ 없음 (requirements.txt만) | ✅ uv 호환 pyproject.toml 추가 (병행) |
| 수집 노트북 | ❌ 없음 | ✅ notebooks/01_collection.ipynb 셸 |
| 수집 .md | ❌ 없음 | ✅ reports/01_collection_README.md |

## 합의된 결정 사항 (v0.2)

- **환경**: 로컬은 `uv`, Colab은 `pip` 병행 (pyproject.toml + requirements.txt 둘 다 유지)
- **크롤링 범위**: 매트릭스(10개 항목) 합의 — DART API 주력 + DART viewer URL + KRX 산업분류 ✅ / KCGS·정정공시 조건부 ✅ / MCP 검증 없이·document.xml 우회·로그인사이트 ❌
- **벤치마킹 4-track**: 강의(Week 4·10) BASE + 공개 코드(dart-fss, opendart-py) + 실무 ETL 패턴 + 학술 논문(Li 2021, Bao 2024)
- **파일럿 시작점**: 삼성전자 005930 × fiscal_year 2024 (1개 firm-year) → 성공 시 3개 업종 확장

## 위반 금지 체크리스트 (v0.2가 지키는 가이드)

- [x] 모든 크롤링 경로에 출처·lineage 기록
- [x] document.xml이 표준 raw 텍스트 경로 (우회 금지)
- [x] MCP는 발견·연습용, corpus 투입 전 Python 재현 검증
- [x] API key 코드 노출 없음 (.env만)
- [x] rate limit·backoff·캐시 적용
- [x] 실패 행은 collection_log.csv에 기록, 가짜 0 금지
- [x] stock_code 기준 join, esg_year = fiscal_year + 1
