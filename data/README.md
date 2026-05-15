# 데이터 폴더

## 공유 데이터 (커밋됨)

이 세 파일은 교수님이 제공한 마스터 자료로 모든 팀원이 동일하게 사용합니다.

| 파일 | 행 수 | 설명 |
|---|---:|---|
| `company_master.csv` | 381 | 127기업 × 3 fiscal_year. 컬럼: company_name, corp_code, stock_code, industry, fiscal_year, report_code, rcept_no, esg_source, esg_grade, e_grade, s_grade, g_grade, esg_year |
| `seed_dictionary.csv` | 30 | E·S·G 각 10개 seed 단어. 컬럼: dimension, seed_term, pattern, source_basis, source_titles, notes |
| `stopwords_ko_esg.txt` | 33 | 한국어 불용어 초안 (조사·부사). 도메인 불용어는 팀이 추가 |

## 비공유 폴더 (gitignore)

각자 수집/생성하는 데이터. 대용량이거나 재현 가능하므로 git에 안 올림.

| 폴더 | 용도 | 예상 크기 |
|---|---|---|
| `raw/` | OpenDART에서 받은 사업보고서 zip 원본 | ~수 GB |
| `interim/` | 전처리 중간 결과 (XML→텍스트, 섹션 추출 등) | ~수백 MB |
| `feature/` | TF-IDF 행렬, firm-year 점수 등 | ~수십 MB |
| `cache/` | API 응답 캐시 등 | 가변 |

## 파일 명명 규칙

```
{stock_code}_{fiscal_year}_{kind}.{ext}
```

예시:
- `005930_2024_disclosure.zip` (raw zip)
- `005930_2024_sections.json` (섹션 추출 결과)
- `005930_2024_tokens.parquet` (토큰화 결과)
- `feature/seed_tfidf_scores.parquet` (전체 firm-year × seed 점수)

## 데이터 출처 lineage

| 컬럼 | 소스 | 비고 |
|---|---|---|
| `company_master.csv` | 교수님 제공 | KCGS 공식 등급 + 분석 단위 정의 |
| `seed_dictionary.csv` | 교수님 제공 | Bloomberg ESG framework, Refinitiv, MSCI KLD, Li 2021 등 문헌 기반 |
| `stopwords_ko_esg.txt` | 교수님 제공 | 일반 조사·부사. 회사명·도메인 불용어는 팀이 보강 |
| `raw/*.zip` | OpenDART API document.xml | rcept_no로 받음 |

## 사용 시 주의

- `corp_code`, `rcept_no` 컬럼은 `company_master.csv`에 비어 있음 — 팀이 채워야 함
- `industry`도 일부 비어 있음 — 팀이 KRX 산업분류 등으로 보강 가능
- `esg_grade` 등급 → 숫자 매핑: S=6, A+=5, A=4, B+=3, B=2, C=1, D=0
- `esg_year = fiscal_year + 1` 고정

## 가짜 0 금지

fastText 학습/회귀 corpus는 **수집·추출 성공행만** 사용. 실패행은 `collection_log.csv`에 사유 기록 후 분석에서 제외. 자세히는 `docs/professor_md/04_submission_and_evaluation.md` 참고.
