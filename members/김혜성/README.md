# 김혜성 작업 폴더

## 작업 방식
전체 파이프라인 개별 진행 (수집 → 전처리 → 마이닝 → 분석).

## 진행 상황 (5/15~5/19)

### Day 1 — 5/15 (금)
- [ ] 환경 셋업 (uv venv + .env, OpenDART API key)
- [ ] company_master.csv 확인, Phase 1 파일럿 (삼성 005930 × 2024) 노트북 실행

### Day 2 — 5/16 (토)
- [ ] Phase 2 1차 batch 50건 시범 (수집)
- [ ] 02_preprocessing.ipynb 작성 시작

### Day 3 — 5/17 (일)
- [ ] Phase 2 잔여 batch (~330건)
- [ ] 전처리 본격 가동 (정제 → 형태소 → ESG passage 필터)

### Day 4 — 5/18 (월)
- [ ] TF-IDF · 임베딩 · cosine similarity 산출
- [ ] analytical_dataset 1차 생성

### Day 5 — 5/19 (화, D-Day)
- [ ] 데이터 품질 게이트 12개 self-check
- [ ] 통합 회의 참석

## 폴더 구조
- `notebooks/` — 본인의 Jupyter 노트북
- `src/` — 본인의 Python 모듈
- `reports/` — 본인의 결정 로그·메모

## 공유 드라이브 sync 규칙
- 본 폴더 ↔ 공유 드라이브 `members/김혜성/` 양방향 sync
- 매일 저녁 진행상황 업로드 (관리자가 GitHub push 일괄 처리)

## 참고
- 5일 로드맵: `docs/supplements/versions/v0.2/ROADMAP_5일_데드라인.html`
- 데이터 수집 가이드: `docs/supplements/versions/v0.2/COLLECTION_데이터수집가이드.html`
