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
| `_TEMPLATE_노트북_표준헤더.md` | 노트북 표준 헤더 | 새 .ipynb 만들 때 이 마크다운을 첨 셀로 붙여넣기 |

## 워크플로우

1. 각 팀원은 본인 폴더에서 **전체 파이프라인**을 작업 (수집 → 전처리 → 마이닝 → 분석)
2. 작업물을 **공유 드라이브**에 업로드
3. 관리자(이동원)가 GitHub 레포에 일괄 push (mygithub05253 + gc-unstructured-data-processing 양쪽)
4. 5/19 데이터 quality 게이트 통과 후 → 5/20 이후 `_integrated/`에서 베스트 부분 통합

## 각 개인 폴더 표준 구조

```
{이름}/
├── notebooks/
│   ├── 01_collection.ipynb       # 활성 버전 (최신)
│   ├── 02_preprocessing.ipynb
│   ├── 03_mining.ipynb
│   └── archive/                   # 과거 스냅샷 (규칙 1: 버전 보존)
│       ├── 01_collection_2026-05-15_initial.ipynb
│       └── 01_collection_2026-05-16_v2.ipynb
├── src/                           # Python 재사용 함수
├── reports/                       # 결정 로그·회의록
└── README.md                      # 본인 5일 진행 체크리스트
```

## 노트북 6개 규칙 (2026-05-15 합의)

모든 .ipynb 파일 작성·발전 시 반드시 지킬 규칙:

| # | 규칙 | 적용 방식 |
|---|---|---|
| 1 | **버전 보존** | 새 버전은 새 파일명으로 — 기존 파일 덮어쓰기 ❌. 중요 버전은 `notebooks/archive/{원본명}_{YYYY-MM-DD}_{descriptor}.ipynb` 스냅샷 |
| 2 | **출력 보존** | GitHub commit 시 모든 셀 출력 유지. `nbstripout` 사용 금지. API key는 코드 측에서 마스킹 |
| 3 | **진행률 시각화** | 오래 걸리는 작업에 `from tqdm.notebook import tqdm` 필수. ipywidgets 의존 |
| 4 | **교수님 가이드 준수 + 모든 경우의 수 테스트** | 노트북 최상단에 위반금지 8항목 헤더 셀. 각 단계마다 alt 셀로 변형 실험 |
| 5 | **결과 시각화 의무** | 단계별 결과를 matplotlib·seaborn·plotly·wordcloud 등으로 검증 |
| 6 | **상세 마크다운·주석** | 각 셀 위에 What/Why/근거 3블록 마크다운. 교수님 자료·수업 자료 인용 |

구체 규칙 적용 탬플릿: [`_TEMPLATE_노트북_표준헤더.md`](_TEMPLATE_노트북_표준헤더.md)

## 왜 이렇게 나누었나

- **버전 관리** — 각 팀원의 작업 history 보존 (누가 어떤 결정을 언제 했는지)
- **파일 보존** — 개인이 만든 중간 결과물 손실 방지
- **통합 시점 명확화** — `_integrated/`로 옮기는 순간이 곧 합의된 산출물
- **실패 격리** — 한 사람의 코드 깨짐이 다른 사람 폴더에 영향 없음
- **상호 학습** — 4명이 같은 문제를 다르게 풀어보고 베스트 비교

## 데이터 파일 정책

- 각 폴더의 `notebooks/` · `src/` · `reports/`는 코드/문서만 커밋 (**노트북 출력 포함**)
- 원본 데이터(zip · json · parquet · csv)는 모두 `.gitignore` (각 팀원 로컬·공유 드라이브 보관)
- `analytical_dataset.parquet` 등 FREEZE 산출물은 `_integrated/`에 hash만 기록

## archive/ 컬벤션 (규칙 1 상세)

새 버전 만들 때 (예: 전처리 로직 큰 변경, 형태소 사전 교체):

1. 현재 노트북을 `notebooks/archive/{원본명}_{YYYY-MM-DD}_{결정적descriptor}.ipynb`로 이동·복사 (출력 보존)
2. 동일 파일명으로 활성 완성 (예: `notebooks/01_collection.ipynb` 유지, 안의 코드를 발전)
3. PR로 push — archive 파일과 활성 파일 모두 commit
4. 결과 나쁜으면 archive의 이전 버전으로 rollback

**명명 예시**
```
notebooks/archive/01_collection_2026-05-15_initial-pilot.ipynb
notebooks/archive/02_preprocessing_2026-05-17_okt-only.ipynb
notebooks/archive/02_preprocessing_2026-05-18_okt+mecab-test.ipynb
notebooks/archive/03_mining_2026-05-18_tfidf-vocab5k.ipynb
notebooks/archive/03_mining_2026-05-18_tfidf-vocab10k.ipynb
```

## 참고 가이드

- 데이터 수집 가이드: `docs/supplements/versions/v0.2/COLLECTION_데이터수집가이드.html` (v0.3에서 nbstripout 관련 안내 제거 예정)
- 5/15~5/19 5일 로드맵: `docs/supplements/versions/v0.2/ROADMAP_5일_데드라인.html`
- 식별자 규칙·PR 정책: `CONTRIBUTING.md`
