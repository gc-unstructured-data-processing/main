# AGENTS.md — ESG DART 기말 프로젝트 작업 지침

> 이 파일은 **AI 코딩 에이전트(Codex / ChatGPT 등)** 가 이 저장소에서 작업할 때 반드시 먼저 읽고 따라야 하는 운영 매뉴얼입니다.
> 가천대 「비정형데이터분석」 2026‑1학기 기말 팀 프로젝트의 누적 작업·회의 결정·교수님 가이드를 한 곳에 정리했습니다.
> 사람이 보기 좋은 시각화 버전은 `프로젝트_인계_대시보드.html` 을 함께 참고하세요.

---

## 0. 프로젝트 한 줄 요약

- **연구 질문**: “ESG 관련 공시 표현(사업보고서 언어)은 KCGS 외부 평가 등급과 통계적으로 유의미하게 **연관**되어 있는가?”
- 이것은 ESG 성과를 **예측·분류**하는 문제가 아니라, 공시 언어와 외부 평가의 잠재적 괴리(**cheap‑talk**)를 탐색하는 **공시 연구**입니다. 결과는 **인과가 아니라 연관**으로만 해석합니다(가이드 04 §4).
- **데이터**: OpenDART 사업보고서, 127개 기업 × 3개 회계연도(2022~2024) = **최대 381 firm‑year**. 종속변수는 KCGS ESG 등급(D=0 … A+=5).
- **분석 단위**: 회사명이 아니라 `stock_code × fiscal_year`.

---

## 1. 황금률 (절대 어기지 말 것)

1. **git 작업은 사람(이동원)이 PC에서 전담한다.** 에이전트는 파일 생성·수정만 하고, `git` 명령(커밋·푸시·리셋은 물론 `git status`까지)을 **직접 실행하지 않는다.**
   - *이유*: 과거 Cowork 샌드박스와 PC가 같은 `.git/` 을 동시 접근해 `index.lock`·HEAD 손상·mount whiteout 충돌이 발생했음. 충돌 방지를 위해 git 소유자를 한 명으로 고정.
   - *Codex(PC 로컬)에서의 적용*: git 명령이 기술적으로 가능하더라도, **실제 커밋/푸시는 사용자 확인 후에만** 수행하고 자동 실행 금지. 변경 요약과 제안된 커밋 메시지를 먼저 보여줄 것.
2. **두 저장소를 항상 동일하게 동기화한다.** (아래 §2)
3. **버전 보존 — 기존 노트북·산출물을 절대 덮어쓰지 않는다.** 결과가 나빠질 때 되돌릴 수 있어야 한다(노트북 규칙 #1).
4. **회의 결정·교수님 가이드 위반금지 8항목은 합의 사항이므로 분석에서 위반 불가.** (아래 §6, §8)

---

## 2. 작업 사이클 — “작업이 끝날 때마다” 양쪽 레포 배포

작업 1건이 끝나면 **작업 단위로** 다음 흐름을 제안한다. 한 PR에 여러 작업을 몰아 넣지 말 것(리뷰·revert 단위를 논리적으로 분리).

```
pull → commit(1건) → push(origin + team) → PR 오픈(양쪽) → squash merge(양쪽)
```

| 단계 | 내용 |
|---|---|
| pull | 양쪽 remote 최신 `main` fetch + 작업 branch sync |
| commit | 같은 변경 내용으로 local commit 1건 (브랜치명·메시지 양쪽 동일) |
| push | `origin` 과 `team` 양쪽에 같은 branch push |
| PR | 양쪽 저장소에 동일 제목으로 PR 오픈 |
| merge | 양쪽 모두 **squash** 머지 |

- **두 저장소**
  - 개인(1차): `https://github.com/mygithub05253/unstructured-data-processing-final-project`
  - 팀(최종): `https://github.com/gc-unstructured-data-processing/main`
- **한 쪽만 처리하면 drift 발생** — 발표·평가 시 어디서든 같은 결과가 나오도록 반드시 양쪽 동기화. (origin만 PR하고 끝내지 말 것)
- `main` 직접 push 금지. 항상 feature branch → PR → merge.
- 머지 후 양쪽 PR 번호는 다를 수 있음(독립 카운터). 그래도 내용은 동일해야 함.
- **team 레포 `has no history in common` 오류 시**: origin/team 이 별도 root commit이라 발생. 사용자 확인 후 force‑sync 또는 cherry‑pick으로 한 번 정렬한 뒤 다시 PR(절대 team 건너뛰지 말 것).

---

## 3. 팀 헌법 — 식별자 규칙 (silent mismatch 방지)

1. **식별자는 `stock_code` 기준**으로만 join. 회사명 merge 금지(동명·표기 변형으로 조용한 오매칭 위험).
2. `stock_code` 는 항상 **6자리 문자열**로 정규화: `stock_code.zfill(6)` (CSV 로드 시 `005930 → 5930` 손실 방지).
3. **타이밍은 `esg_year = fiscal_year + 1` 고정.** KCGS 평가연도 t 등급과 직전 회계연도 t‑1 사업보고서 언어의 정렬을 **서술적으로** 본다(시점 식별·인과 아님).
4. **실패 행은 drop + `collection_log.csv`(status·reason) 기록.** 텍스트 점수를 가짜 0으로 강제 금지.

---

## 4. 폴더 구조

```
unstructured-data-processing-final-project/
├── AGENTS.md                      # ← 이 파일
├── 프로젝트_인계_대시보드.html      # 시각화 대시보드
├── docs/professor_md/             # 교수님 가이드 01~04 (정본, 수정 금지)
├── docs/supplements/              # 팀 보강자료 (GLOSSARY/QNA/SUPPLEMENT HTML 등)
├── data/
│   ├── raw/                       # 원문 ZIP (위반금지 #5 — 보존)
│   ├── interim/corpus_381/        # firm-year별 수집 JSON 캐시 (idempotent)
│   └── processed/                 # feature parquet/xlsx, 사전 csv
└── members/
    ├── 이동원/  김지우/  김혜성/  신지영/   # 각자 전체 파이프라인
    │   ├── notebooks/  (+ archive/, _legacy/)
    │   ├── reports/
    │   └── README.md
    └── _integrated/               # 5/19 이후 베스트 부분 통합
```

- **새 작업물은 적절한 `members/{이름}/` 하위**에 배치. 통합 결정은 `members/_integrated/reports/integration_decisions.md` 에 채택자·commit hash 기록.
- 현재 메인 산출물: `members/이동원/notebooks/integrated/v1/esg_dart_integrated_v1.ipynb` (34셀, Run All 에러 0).

---

## 5. 노트북 작성 6규칙

1. **버전 보존** — 새 버전을 만들어도 기존 노트북 덮어쓰기 금지. 활성 파일 + `notebooks/archive/{원본명}_{YYYY-MM-DD}_{설명}.ipynb` 스냅샷.
2. **GitHub에 출력 보존** — 커밋 시 모든 셀 출력 유지. `nbstripout` **사용 금지**(전처리 재실행은 비효율).
3. **진행률 시각화 필수** — 오래 걸리는 작업(수집·전처리)엔 `tqdm.notebook` 또는 % 표시.
4. **교수님 가이드 준수 + 모든 경우의 수 테스트** — 매 노트북 상단에 위반금지 8항목 헤더 셀. 각 단계마다 변형 실험(분석기 3종 비교, vocab sweep 등).
5. **결과 시각화 의무** — 각 단계 결과를 matplotlib/seaborn/plotly/wordcloud로 검증.
6. **마크다운·주석 상세** — 각 셀 위에 **What / Why / 근거(가이드 line·수업 Week·학술 인용)** 3블록 + 비전공자도 이해할 주석.

> **마크다운 규율(중요)**: v1부터 처음부터 세심하게 작성한다. “나중에 v_final에서 몰아 정리” 패턴 금지 — 잘 되면 v1이 그대로 최종 제출 버전이 되도록 채점 quality로 작성. 버전 v→v+1 전환은 알고리즘·라이브러리 변경 등 실질 변경 시에만.

> **비밀값 보호**: 출력이 보존되므로 API key 등은 출력에 절대 노출 금지. 코드엔 `<MASKED>` placeholder 사용.

---

## 6. 5/19 회의 결정 (위반 불가)

1. **데이터 381개 다 살리기** — 김혜성 `find_business_report_v2`(결산월 무관 + 정정 우선순위) 참고. *근거*: 김지우가 파일럿 n=30 → 전체 n=210에서 부호 역전(상위 대형주 표집 편의)을 발견 → 전수 수집으로 표집 편의 축소.
2. **형태소 분석기 robust 검증 후 결정** — Kiwi vs Okt 비교, 근거 기반 선정. Komoran·Kkma 제외 근거도 명확히(교수님 심층 질문 대비).
3. **seed 단어 30개 활용** — 김혜성 user dict `score` 방식(복합명사 보존).
- 전처리까지 통합 후 알파분석까지 진행. 다음 회의(5/23)에서 4명 결과 추합 + 최종 분석 파일·역할 분담.

---

## 7. 환경 / .env (주의!)

- Python 3.10+, `requirements.txt` / `pyproject.toml` 사용. PRIMARY 형태소 분석기 = **Kiwi**.
- **`.env` 의 OpenDART API key 이름은 `API_KEY`** 다. 가이드 02 예시(`OPENDART_API_KEY`)와 다름.
- 키 로드는 **반드시 후보 리스트로** 처리하고, 코드 작성 전 실제 키 이름을 확인할 것:

```python
import os
# 작성 전 확인:  awk -F= '{print $1}' .env
KEY_CANDIDATES = ['OPENDART_API_KEY', 'API_KEY', 'DART_API_KEY']
API_KEY = next((os.getenv(k) for k in KEY_CANDIDATES if os.getenv(k)), None)
assert API_KEY, f'❌ {KEY_CANDIDATES} 어느 것도 .env에 없음. cat .env로 키 이름 확인.'
```

---

## 8. 교수님 가이드 — 위반금지 8항목 (매 노트북 상단 명시)

| # | 위반금지 | 준수 방식 |
|---|---|---|
| 1 | 실패 행을 가짜 0으로 채우기 ❌ | 수집/추출 실패 행은 status·reason 기록, corpus에서 제외 |
| 2 | 회사명으로 merge ❌ | `stock_code × fiscal_year` 키로만 join |
| 3 | MCP/LLM 결과 그대로 신뢰 ❌ | Python으로 직접 파싱·재현, seed 직접 검토 |
| 4 | API key 코드 노출 ❌ | `.env` 의 `API_KEY` 환경변수만 사용 |
| 5 | raw 원문 미보존 ❌ | `data/raw/*.zip` 원문 ZIP 보존 |
| 6 | 진단·평가 부재 ❌ | 단계별 통계·시각화·robust 검증 |
| 7 | silent 오매칭 ❌ | `stock_code.zfill(6)` |
| 8 | timing 무시 ❌ | `esg_year = fiscal_year + 1` |

**평가에서 보는 7영역**: 데이터 이해 · DART lineage(stock_code/corp_code/rcept_no/fiscal_year 구분 + 추출 로그) · 텍스트 처리(II·IV·VI 발췌, 불용어, feature 선택 근거) · 측정 validity(Spearman·그룹 평균차로 feature 정당화) · 모형 선택(OLS/ordered/binary 중 질문에 맞게 + 버린 대안 한계) · 해석과 한계(효과 크기·cheap‑talk·표본 한계) · 알파(이유·결과·한계).

**제출물**: 분석 노트북 `.ipynb`(실행 가능 상태, 출력·표 포함) + 보고서 `.md`(데이터→방법→결과→한계, 각 선택의 이유 명시).

---

## 9. 방법론 — 전체 파이프라인 15단계

수집부터 알파까지를 15단계로 본다(상세·실측 수치는 대시보드 참조).

1. KCGS 등급 적재 (D~A+ → 0~5)
2. 식별자 매핑 (`corpCode.xml` 전체 다운로드로 `stock_code↔corp_code`, 개별 검색 회피)
3. 사업보고서 탐색 (`rcept_no`, `find_business_report_v2`: 결산월 무관 + 정정 우선순위)
4. 원문 수집 (`document.xml` ZIP, OpenDART API, `data/raw/` 보존)
5. 섹션 추출 (II·IV·VI, lxml `<SECTION-1>` 14개 순회 + `section_code`, `XMLParser(recover=True)`)
6. 형태소 분석기 벤치마킹 (Kiwi 87% vs Okt 67% seed 보존 → **Kiwi PRIMARY**)
7. 전처리·토큰화 (seed 30 `NNP score=50` + 불용어 358, seed는 불용어 제외)
8. seed/expanded TF‑IDF (E·S·G)
9. 기준 문장 cosine similarity (E·S·G)
10. signal ratio (`g_signal_ratio`, `esg_signal_ratio`) + cheap‑talk 통제(`total_tokens`, `specificity`)
11. Spearman 순위상관 (vs KCGS 등급)
12. Bootstrap 95% CI
13. Mann‑Whitney U (고등급 A↑ vs 저등급)
14. 회귀 3종 (OLS / Ordered Logit / Binary Logit)
15. 알파분석 4종 (부호역전 robustness · section_weighted · 업종 분해 · cheap‑talk 3종 통제)

**핵심 실측(통합 v1, N=381)**: 수집 381/381 SUCCESS · `total_tokens` ρ=0.654\*\*\*(최강, cheap‑talk 우려) · `seed_tfidf_E` ρ=0.318\*\*\* · `cosine_S` ρ=0.401\*\*\* · `g_signal_ratio` ρ=−0.067(무유의) · OLS β=23.06, p=0.0006, R²=0.406.

---

## 10. 새 대화/세션 시작 시 체크리스트

- [ ] 이 `AGENTS.md` 와 `프로젝트_인계_대시보드.html` 를 먼저 읽는다.
- [ ] git 은 사람이 전담 — 에이전트는 파일만, 커밋/푸시는 사용자 확인 후.
- [ ] 작업 끝나면 작업 단위로 양쪽 레포 동기화 제안.
- [ ] 노트북 6규칙 + 위반금지 8항목 self‑check.
- [ ] `.env` 키 이름은 `awk -F= '{print $1}' .env` 로 먼저 확인.
- [ ] 5/19 회의 결정(381 전수·분석기 robust·seed 30) 위반 여부 확인.
