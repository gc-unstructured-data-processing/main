# 팀 작업 폴더 (Team Workspaces)

본 ESG DART 프로젝트는 **4명이 각자 전체 파이프라인을 개별 진행한 뒤 통합하는 방식**으로 운영됩니다.

## 폴더 구조

| 폴더 | 역할 | 비고 |
|---|---|---|
| `이동원/` | 개인 작업물 | 본인 파이프라인 + GitHub 관리 |
| `김지우/` | 개인 작업물 | 본인 파이프라인 |
| `김혜성/` | 개인 작업물 | 본인 파이프라인 |
| `신지영/` | 개인 작업물 | 본인 파이프라인 |
| `_integrated/` | 4명 통합 결과 | 최종 분석·발표 자료 (5/19 이후) |

## 워크플로우

1. 각 팀원은 본인 폴더에서 **전체 파이프라인**을 작업 (수집 → 전처리 → 마이닝 → 분석)
2. 작업물을 **공유 드라이브**에 업로드
3. 관리자(이동원)가 본 GitHub 레포에 일괄 push
4. 5/19 데이터 quality 게이트 통과 후 → 5/20 이후 `_integrated/`에서 베스트 부분 통합

## 각 개인 폴더 표준 구조

```
{이름}/
├── notebooks/   # Jupyter 노트북 (01_collection, 02_preprocessing, 03_mining 등)
├── src/         # Python 모듈 (재사용 함수)
├── reports/     # 분석 노트, 의사결정 기록, 회의록 등
└── README.md    # 본인의 작업 진행 상황·로그
```

## 왜 이렇게 나누었나

- **버전 관리** — 각 팀원의 작업 history 보존 (누가 어떤 결정을 언제 했는지)
- **파일 보존** — 개인이 만든 중간 결과물 손실 방지
- **통합 시점 명확화** — `_integrated/`로 옮기는 순간이 곧 합의된 산출물
- **실패 격리** — 한 사람의 코드 깨짐이 다른 사람 폴더에 영향 없음
- **상호 학습** — 4명이 같은 문제를 다르게 풀어보고 베스트 비교

## 데이터 파일 정책

- 각 폴더의 `notebooks/` · `src/` · `reports/`는 코드/문서만 커밋
- 원본 데이터(zip · json · parquet · csv)는 모두 `.gitignore` (각 팀원 로컬·공유 드라이브 보관)
- `analytical_dataset.parquet` 등 FREEZE 산출물은 `_integrated/`에 hash만 기록

## 참고 가이드

- 데이터 수집 가이드: `docs/supplements/versions/v0.2/COLLECTION_데이터수집가이드.html`
- 5/15~5/19 5일 로드맵: `docs/supplements/versions/v0.2/ROADMAP_5일_데드라인.html`
- 식별자 규칙·PR 정책: `CONTRIBUTING.md`
