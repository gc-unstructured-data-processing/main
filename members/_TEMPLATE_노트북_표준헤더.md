# 노트북 표준 헤더 탬플릿

본 파일은 모든 .ipynb 파일의 **첫 셀**에 마크다운 셀로 붙여넣을 헤더 탬플릿입니다.
→ 노트북 6개 규칙 (`members/README.md`) 준수를 보장.

---

## 사용법

1. 빈 노트북 생성 (예: `members/이동원/notebooks/02_preprocessing.ipynb`)
2. 첫 셀을 **Markdown**으로 설정
3. 아래 "헤더 셀 내용" 부분을 복사해서 붙여넣기
4. `{...}` placeholder를 본인 정보로 교체

---

## 헤더 셀 내용 (복사해서 사용)

```markdown
# {01_collection} — {DART API를 이용한 사업보고서 수집}

> **작성자**: {이동원} | **노트북 버전**: v{1} | **작성일**: {2026-05-15} | **마지막 수정**: {2026-05-15}
>
> **결과 요약** (실행 후 채움): {예— 삼성전자 005930 × fiscal_year 2024 파일럿 성공 · sections.json 3개 추출}

## 이 노트북의 목적

{한 문단으로 설명 — 예: OpenDART API를 사용해 stock_code 기준으로 사업보고서 document.xml을 다운로드하고, II·IV·VI 섹션을 추출한 뒤 ESG passage 후보를 저장한다.}

## 교수님 가이드 위반금지 8항목 (접수경로 명시)

- [x] (1) 모든 크롤링 경로에 출처·lineage 기록
- [x] (2) document.xml이 표준 raw 텍스트 경로 (우회 금지)
- [x] (3) MCP는 발견·연습용, corpus 투입 전 Python 재현 검증
- [x] (4) API key 코드 노출 없음 (.env만) + 출력에도 노출 없음
- [x] (5) rate limit·backoff·캐시 적용
- [x] (6) 실패 행은 collection_log.csv에 기록, 가짜 0 금지
- [x] (7) stock_code 기준 join, esg_year = fiscal_year + 1
- [x] (8) 이 노트북 재실행 가능 (idempotent, 캠시 존재)

## 이전 버전·다른 접근

| 파일 | 설명 | 각주롭고 포기한 이유 |
|---|---|---|
| `archive/01_collection_2026-05-15_initial.ipynb` | 결과원본 파일럿 (삼성 1건) | 성공 교훈 일부 본 버전에 반영 — 50건 확장 실패 시 롤백 |
| (예) `archive/01_collection_2026-05-16_rate-limit-v2.ipynb` | rate limit 0.3s 의 v2 | 0.5s로 강화, 성공률 개선 |

## 참고·출처

- 교수님 가이드: `docs/professor_md/02_dart_data_collection.md` §N (구체 세션)
- 데이터 수집 가이드: `docs/supplements/versions/v0.2/COLLECTION_데이터수집가이드.html` → "Phase 1 파일럿" 탭
- 5일 로드맵: `docs/supplements/versions/v0.2/ROADMAP_5일_데드라인.html`
- 학술: Li et al. 2021 (Review of Financial Studies) — NER 기반 ESG passage 식별

## 새 버전 만든 이유 (v2 이상일 경우)

{예— v1은 rate limit 0.3s어서 429 에러 적집. v2는 0.5s + exponential backoff 추가.}
```

---

## 컬레이아웃 셀 (각 절 단계 앞에 삽입 권장)

각 코드 셀 바로 위에 다음 세 블록 마크다운 셀을 넣어 설명을 달아주세요 (규칙 6).

```markdown
## Step N — {함수 또는 단계 명}

**What** — {이 코드가 무엇을 하는지 한 줄·한 문단}

**Why** — {왜 필요한지 — 명확한 목적·문제·고쳐야 할 것}

**근거** — {교수님 가이드 §N 인용, 수업 Week X 슬라이드, 혹은 학술 인용. "이 결정의 근거"를 명시}
```

## 진행률 시각화 셀 예시 (규칙 3)

```python
# tqdm.notebook 사용 — Jupyter용 진행률 바
from tqdm.notebook import tqdm
import time

results = []
for stock_code in tqdm(stock_codes, desc="Collecting"):
    # 실제 수집 로직
    time.sleep(0.5)  # rate limit
    result = collect_one(stock_code)
    results.append(result)

# Phase 2 batch 처림 몇 천건 처리 시 마다 이렇게 감싸서 수행
```

## API key 안전 수칙 (규칙 2 주의사항)

출력을 보존하면 API key가 노출될 수 있으므로 몇 가지 규칙:

**❌ 절대 금지**
```python
# url에 key가 들어가는 경우 절대 출력 X
print(response.url)               # 429 에러 디버깅 시에도 금지
print(f"key: {api_key}")           # 이따고 그럴 일 없다… 가 아니라 실수로 잘 나옴
```

**✅ 권장**
```python
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("OPENDART_API_KEY")
assert API_KEY, ".env에 OPENDART_API_KEY 설정 필요"

# request 호출 시 params로 전달 (URL에 노출 X — 이때도 .url 출력 금지)
response = requests.get(BASE_URL, params={"crtfc_key": API_KEY, "corp_code": corp_code})

# 출력에서 key 제거 (mask 함수 추천)
def mask_key(text: str) -> str:
    return text.replace(API_KEY, "<MASKED>") if API_KEY else text

print(mask_key(response.text[:500]))
```

## 결과 시각화 셀 예시 (규칙 5)

```python
import matplotlib.pyplot as plt
import koreanize_matplotlib   # 한글 폰트 자동 설정
import seaborn as sns

# 수집 결과 시각화 — firm-year별 성공/실패 분포
fig, ax = plt.subplots(figsize=(10, 4))
log_df["status"].value_counts().plot(kind="barh", ax=ax)
ax.set_title("Phase 2 batch 수집 결과 — firm-year별 status 분포")
ax.set_xlabel("firm-year 수")
plt.tight_layout()
plt.show()
```
