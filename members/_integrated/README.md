# 통합 작업 폴더 (Integrated)

4명(이동원·김지우·김혜성·신지영)의 작업물을 최종 통합하는 폴더.

## 활성화 시점
- **1차 통합**: 2026-05-19 데이터 quality 게이트 12개 통과 직후
- **최종 통합**: 발표 자료 완성 시점 (5/25 이후)

## 통합 절차

1. 4명 각자 폴더의 `notebooks/` · `src/` · `reports/` 점검
2. 회의에서 각 단계별 베스트 코드/노트북 선정 (Phase별):
   - 수집 단계 베스트 → `_integrated/notebooks/01_collection.ipynb`
   - 전처리 단계 베스트 → `_integrated/notebooks/02_preprocessing.ipynb`
   - 마이닝 단계 베스트 → `_integrated/notebooks/03_mining.ipynb`
   - 회귀 단계 베스트 → `_integrated/notebooks/04_regression.ipynb` (5/20 이후)
3. 본 `_integrated/` 폴더에 정리:
   - `notebooks/` — 최종 파이프라인 노트북
   - `src/` — 4명 모듈 중 베스트 함수만 모음
   - `reports/` — 최종 분석 보고서 + 회의록 + decision log

## FREEZE 산출물 (5/19 데드라인)

- `analytical_dataset.parquet` — hash 기록 (md5/sha256)
- `esg_passages.parquet` / `esg_features.parquet`
- `collection_log.csv` 최종본
- 데이터 품질 게이트 12개 통과 보고서

## 5/20 이후 산출물

- 회귀·알파 분석 결과 노트북
- 시각화 (matplotlib/plotly)
- 최종 발표 슬라이드 (10분)
- 최종 보고서 (5-10 페이지)

## 통합 결정 기록 규칙

각 단계별로 누구의 코드를 채택했는지 `reports/integration_decisions.md`에 기록:
```
## 01_collection.ipynb
- 채택: 김지우 (가장 robust한 정규식 + retry 로직)
- 출처: members/김지우/notebooks/01_collection.ipynb (commit abc1234)

## 02_preprocessing.ipynb
- 채택: 신지영 (KoNLPy 사용자 사전 30개 추가, OOV 12% 달성)
- 출처: members/신지영/notebooks/02_preprocessing.ipynb (commit def5678)
```

## 참고
- 5일 로드맵 (5/15~5/19): `docs/supplements/versions/v0.2/ROADMAP_5일_데드라인.html`
- 게이트 12개 정의: 위 ROADMAP HTML 4번 탭 (데이터 품질 게이트)
- 데이터 수집 가이드: `docs/supplements/versions/v0.2/COLLECTION_데이터수집가이드.html`
