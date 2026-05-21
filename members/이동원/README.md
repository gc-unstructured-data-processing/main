# 이동원 작업 폴더

## 작업 방식
전체 파이프라인 개별 진행 (수집 → 전처리 → 마이닝 → 분석) + **GitHub 레포 솔로 관리**.

## 진행 상황 (5/15~5/19)

### Day 1 — 5/15 (금)
- [ ] (관리자) v0.2 supplements + ROADMAP HTML PR 머지
- [ ] (관리자) 4명에게 ROADMAP HTML 공유
- [ ] (관리자) members/ 폴더 구조 안내
- [ ] 환경 셋업 (uv venv + .env)
- [ ] company_master.csv 확인, corp_code 매핑 노트북 실행

### Day 2 — 5/16 (토)
- [ ] Phase 2 1차 batch 50건 시범 (수집)
- [ ] 02_preprocessing.ipynb 작성 시작
- [ ] (관리자) 다른 팀원 PR 리뷰

### Day 3 — 5/17 (일)
- [ ] Phase 2 잔여 batch (~330건)
- [ ] 전처리 본격 가동

### Day 4 — 5/18 (월)
- [ ] TF-IDF · 임베딩 · cosine similarity 산출
- [ ] analytical_dataset 1차 생성

### Day 5 — 5/19 (화, D-Day)
- [ ] 데이터 품질 게이트 12개 self-check
- [ ] (관리자) 통합 회의 진행 + FREEZE 선언
- [ ] (관리자) `_integrated/`에 최종 산출물 push

## 폴더 구조 (2026-05-21 정리)
- `notebooks/integrated/v1/` — ⭐ **최종 통합 노트북** (회의 결정 반영: 381 수집·분석기 robust·seed 30 + 알파 4종). `esg_dart_integrated_v1.ipynb` + 보고서(REPORT)·발전가이드(GUIDE) HTML/MD + `_build_scripts/`
- `notebooks/_legacy/` — 단계별 구버전 이력 (00~05, phase1/2A/2B, v1~v_final). 참고용 보존
- `reports/_legacy/` — 단계별 구버전 보고서/진단 이력
- `src/collection.py` — 수집 재사용 모듈 (recover XML parser 등)

> 단계 세분화(00/01/02/03 분리) 방식은 통합 노트북으로 대체됨. 현재 메인 산출물은 `notebooks/integrated/v1/`.

## 공유 드라이브 sync 규칙
- 본 폴더 ↔ 공유 드라이브 `members/이동원/` 양방향 sync
- 매일 저녁 진행상황 commit (관리자가 GitHub push 일괄 처리)

## 참고
- 5일 로드맵: `docs/supplements/versions/v0.2/ROADMAP_5일_데드라인.html`
- 데이터 수집 가이드: `docs/supplements/versions/v0.2/COLLECTION_데이터수집가이드.html`
