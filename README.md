# ESG DART 기말 프로젝트

비정형데이터분석 (2026 1학기, 가천대) 기말 팀 프로젝트.
DART 사업보고서의 ESG 언어와 KCGS 등급의 연관성 분석.

## 팀
- A · 코디네이션 · GitHub master
- B · 데이터 수집
- C · 전처리 · Feature
- D · 회귀 · 알파 분석

## 폴더 구조

```
.
├── README.md                    # 이 파일
├── CONTRIBUTING.md              # 팀 협업 규칙 (브랜치·커밋·PR)
├── requirements.txt             # Python 의존성
├── pyproject.toml               # uv 호환 (Colab pip와 병행)
├── .gitignore
├── data/
│   ├── README.md                # 데이터 소스·구조 명시
│   ├── company_master.csv       # 381 firm-year master (교수 제공)
│   ├── seed_dictionary.csv      # 30 seed × E·S·G (교수 제공)
│   ├── stopwords_ko_esg.txt     # 한국어 불용어 초안 (교수 제공)
│   ├── raw/                     # 사업보고서 zip (.gitignore — 각자 수집)
│   ├── interim/                 # 전처리 결과 (.gitignore)
│   └── feature/                 # TF-IDF·점수 (.gitignore)
├── docs/
│   ├── professor_md/            # 교수님 4개 .md 가이드
│   ├── guides/                  # 기존 HTML 가이드 (심층/시각화/협업 등)
│   └── supplements/             # 팀 보강 자료 (용어사전·8단계·QnA + versions/v0.1·v0.2)
├── notebooks/                   # 분석 노트북 (번호-이니셜-내용)
├── src/                         # 재사용 함수
└── reports/                     # .md 보고서
```

## 환경
1. Python 3.10+
2. `.env` 파일에 `OPENDART_API_KEY` 등록 (본인 인증키)
3. **로컬**: `uv venv && uv pip install -e .` / **Colab**: `!pip install -r requirements.txt`
4. `nbstripout --install` (노트북 conflict 방지)

## 팀 헌법 3개
1. **식별자**: `stock_code` 기준 (회사명 X — silent mismatch 위험)
2. **타이밍**: `esg_year = fiscal_year + 1` 고정
3. **실패 행**: drop + `collection_log.csv`에 이유 기록 (가짜 0 X)

## 마일스톤
- M1 수집 완료: [날짜]
- M2 Feature freeze: [날짜]
- M3 회귀·알파 완료: [날짜]
- M4 발표: [날짜]

## 시작하기
```bash
git clone https://github.com/gc-unstructured-data-processing/main.git
cd main
uv venv && uv pip install -e .       # 로컬
# 또는: pip install -r requirements.txt
cp .env.example .env                   # .env에 OPENDART_API_KEY 입력
```

## 문서 읽는 순서 (비전공자 권장)
1. `docs/professor_md/01_assignment_overview.md` — 전체 흐름
2. `docs/supplements/GLOSSARY_비전공자용어사전.html` — 용어 25개 풀이
3. `docs/supplements/versions/v0.1/ANALYSIS_프로젝트분석.html` — 프로젝트 종합 분석
4. `docs/supplements/versions/v0.1/ROLES_역할분담재설계.html` — 4명 협업 모델 (3-Phase)
5. `docs/professor_md/02_dart_data_collection.md` — 데이터 수집
6. `docs/supplements/versions/v0.2/COLLECTION_데이터수집가이드.html` — 수집 단계 풀이
7. `docs/supplements/SUPPLEMENT_8단계보강가이드.html` — 단계별 위반금지/권고/발전
8. `docs/professor_md/03_minimal_analysis_example.md` — 분석 예시
9. `docs/professor_md/04_submission_and_evaluation.md` — 제출 기준
10. `docs/supplements/QNA_발표대비.html` — 발표 직전 정독

## 참고
- 본 저장소는 ESG DART 기말 프로젝트 Organization 협업 레포입니다.
- 개인 레포 미러: https://github.com/mygithub05253/unstructured-data-processing-final-project
