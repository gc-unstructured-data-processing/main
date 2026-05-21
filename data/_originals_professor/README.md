# data/_originals_professor/ — 교수님 제공 원본 데이터 보존

> 📌 **원칙**: 이 폴더의 파일은 **읽기 전용**. 절대 수정·삭제 금지.
> 모든 분석은 상위 data/ 폴더의 파일을 사용하며, 본 폴더는 lineage 추적용 snapshot.

## 출처
- 가천대학교 비정형데이터분석 (2026 1학기) 기말 프로젝트
- 교수님 제공 시드 데이터 (2026-05-04 강의 자료)

## 버전 v0 (2026-05-04 받음)

| 파일 | 크기 | 용도 |
|---|---:|---|
| company_master.csv | 27 KB | 127 stock_code × 3 fiscal_year = 381 firm-year 식별자 + KCGS 등급 |
| seed_dictionary.csv | 5.6 KB | E·S·G 각 10단어 = 30 seed (가이드 01 line 130-138) |
| stopwords_ko_esg.txt | 0.3 KB | 한국어 ESG 불용어 초안 (가이드 03 line 56-58) |

## 향후 버전 정책

신규 시드 데이터를 교수님이 제공할 경우 `v1/`, `v2/` ... 폴더 신설.
파일명·구조 동일하게 유지.

## 사용 방법

```python
# 원본 직접 사용 (분석용 데이터는 ROOT/data/ 사용)
import pandas as pd
ROOT = Path(__file__).parent.parent.parent  # data/_originals_professor/
cm_original = pd.read_csv(ROOT / 'data' / '_originals_professor' / 'v0' / 'company_master.csv',
                          dtype={'stock_code': str})
```

## 변경 이력

- 2026-05-04: 교수님 강의 자료로 받음 (v0)
- 2026-05-18: members/이동원/notebooks 사이클 3 작업으로 본 보존 폴더 신설 (이동원)
