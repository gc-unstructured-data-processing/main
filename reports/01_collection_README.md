# 01 · 데이터 수집 단계 — 결정 사항 기록 (Phase 1)

> **작성일**: 2026-05-15
> **단계**: Phase 1 파일럿 (005930 × 2024)
> **노트북**: `notebooks/01_collection.ipynb`
> **HTML 가이드**: `docs/supplements/versions/v0.2/COLLECTION_데이터수집가이드.html`

이 문서는 수집 단계에서 팀이 내린 결정과 그 이유를 기록합니다. **최종 보고서(.md)의 "데이터" 섹션 초안**으로도 사용됩니다.

---

## 1. 표본 정의

### 결정
- 분석 단위: `stock_code × fiscal_year`
- 범위: 127개 기업 × 3 fiscal_year (2022, 2023, 2024) = **최대 381 firm-years**
- KCGS 등급 매칭: `esg_year = fiscal_year + 1` (예: 2025 등급 ↔ 2024.12 사업보고서)

### 이유
- 가이드 02 md "분석 단위 주의"에 명시 — `company_name`은 사명변경·분할로 silent 오매칭 위험 (`company_name` 133개 ≠ `stock_code` 127개)
- timing: 가이드 02 md "이 과제의 시간 기준은 KCGS 평가연도 t와 직전 회계연도 t-1 사업보고서의 연결"

### 위반 금지 체크
- [x] 회사명 join 사용 안 함
- [x] esg_year = fiscal_year + 1 매핑 고정

---

## 2. 식별자 깔때기

### 결정
세 식별자를 다음 순서로 채움:

```
stock_code (CSV에 있음, 6자리)
   ↓ OpenDART corpCode.xml (전체 1회)
corp_code  (8자리)
   ↓ OpenDART list.json (firm-year별)
rcept_no   (14자리)
   ↓ OpenDART document.xml
원본 사업보고서 zip
```

### 이유
- 가이드 02 md "먼저 이해할 세 가지 식별자" 명시
- OpenDART API는 `corp_code`를 키로 받음. `stock_code` 직접 사용 불가
- `list.json`은 정정공시 포함되므로 `last_reprt_at=Y`로 최신만 선택

### 핵심 코드 결정
- `corpCode.xml`은 **1회만** 받고 `data/cache/corp_code_map.parquet`로 캐시 (재실행 시 즉시 로드)
- `list.json` 필터: `report_nm`에 `"사업보고서"` AND `f"({fiscal_year}.12)"` 동시 포함
- 매칭된 행이 여러 개면 첫 행 선택 (`last_reprt_at=Y`로 이미 최신 1건만)

---

## 3. 원문 다운로드 경로

### 결정
- **표준 경로**: `document.xml` (OpenDART API)
- **저장 위치**: `data/raw/{stock_code}_{fiscal_year}_disclosure.zip`
- **재실행 안전**: 이미 받은 zip (크기 > 1KB)은 재다운로드 ❌

### 이유
- 가이드 02 md "document.xml로 raw ZIP을 저장한다" 명시
- viewer URL을 Selenium으로 긁는 우회 경로는 ❌ — lineage 추적 어려움 + LLM passage 검증 원칙 위배
- 재실행 안전성은 실무 ETL 표준 (idempotent)

### 위반 금지 체크
- [x] document.xml이 표준 경로
- [x] viewer 페이지 우회 크롤링 안 함

---

## 4. 섹션 추출

### 결정
- 분석 대상 섹션: **II (사업의 내용)**, **IV (이사의 경영진단)**, **VI (이사회 등 회사의 기관)**
- 추출 방식: 헤딩 정규식으로 시작 위치 찾기 → 다음 헤딩까지 슬라이스
- 헤딩 정규식: `II.|Ⅱ.|2.` 형식 OR로 매칭 (회사별 변형 대응)

### 이유
- 가이드 01 md "II, IV, VI 섹션에서 ESG 관련 문장을 추출" 명시
- II: 환경(E) 신호가 많음 (사업 내용 설명에 탄소·재생에너지 언급)
- IV: 사회(S)·지배구조(G) 신호 (경영진 시각의 ESG 언급)
- VI: 지배구조(G) 신호 多 (사외이사·감사위·내부통제)

### 추출 실패 시 대응
- 정규식 매칭 실패 → 다른 패턴(`Ⅱ.`, `2.`) 시도
- 모두 실패 → `collection_log`에 `FAIL_SECTION` 기록 후 drop (가짜 0 ❌)

---

## 5. ESG passage 후보 추출

### 결정
- 입력: 추출된 섹션 텍스트 (II/IV/VI)
- 필터: seed 30개(E·S·G × 10) 중 하나라도 포함된 문장
- 문장 분리: 마침표·줄바꿈 기준 (단순 분리. 정교한 분리는 다음 단계)
- 출력: passage 후보 DataFrame (sentence, section, dimensions, matched_terms)

### 이유
- 가이드 02 md "ESG 관련 문장을 추출하고 출처 섹션을 기록"
- 이 단계는 **후보 추출**일 뿐. 최종 corpus는 다음 단계(전처리·feature)에서 결정
- 단순 키워드 매칭 — 향후 fastText 확장 후 재추출 가능

### 위반 금지 체크
- [x] MCP가 만든 passage 사용 안 함 (Python 코드로 재현)
- [x] 추출 결과를 viewer URL과 직접 대조 (sample 5개)

---

## 6. 실패 행 처리

### 결정
- `collection_log.csv` 컬럼: `stock_code, fiscal_year, esg_year, corp_code, rcept_no, status, reason, n_passages, timestamp`
- 상태 코드: `SUCCESS / FAIL_CORP / FAIL_RCEPT / FAIL_DOC / FAIL_SECTION`
- 실패 행은 **분석 corpus에서 drop** — 가짜 0 ❌

### 이유
- 가이드 04 md "실패 행을 가짜 0으로 채워 텍스트 분석 corpus에 억지로 넣지 않는다" 명시
- 최종 보고서에 누락 사유를 적는 것이 정직성

### 위반 금지 체크
- [x] 가짜 0 없음
- [x] 모든 실패 사유 기록
- [x] 최종 보고서에 누락 행 설명 (Phase 3에서 작성)

---

## 7. API key 보호

### 결정
- 코드 직접 입력 ❌
- `.env` 파일에 `OPENDART_API_KEY` 저장
- 노트북에서 `python-dotenv`로 로드
- 출력 셀에 API key 포함된 URL 노출 ❌

### 이유
- 가이드 04 md §5 "API key 제거 확인" 항목
- CONTRIBUTING.md "API key 다루기" 규칙

### 위반 금지 체크
- [x] `.env`만 사용
- [x] `print(api_key)`, `print(res.url)` 금지
- [x] `.gitignore`에 `.env` 등록 확인

---

## 8. Rate Limit · Backoff (Phase 2 진입 시 적용)

### 결정 (Phase 2 적용)
- Rate limit: 분당 300회 (OpenDART 권장 600회의 안전 마진)
- Exponential backoff: 503/429 응답 시 1초 → 2초 → 4초 → ... 최대 5회 재시도
- 동시 요청 수: 1 (순차 처리)

### 이유
- 가이드 02 md "rate limit 분당 600회 페이스로 안전 마진 확보"
- 공개 코드(dart-fss, opendart-py) 벤치마킹 결과

---

## 9. Phase 1 파일럿 결과 (작성 예정)

> 노트북 실행 후 결과를 여기에 채웁니다.

```
파일럿 대상: 삼성전자 005930 × 2024
실행 일자:   2026-05-{XX}
실행자:      {이니셜}

[결과]
- corp_code:  00126380
- rcept_no:   {확인 후 기입}
- zip 크기:   {KB}
- 섹션 II:    {길이}자
- 섹션 IV:    {길이}자
- 섹션 VI:    {길이}자
- passage 후보: {개수}개

[viewer URL 정합성 검증]
- 무작위 5개 중 {N}개 일치
- 불일치 케이스 분석: {있다면 사유}
```

---

## 10. Phase 2 진입 전 결정 사항 (회고 회의 어젠다)

회고 회의에서 합의해야 할 항목:

- [ ] **rate limit 값** — 분당 300회 / 500회 / 600회 중 선택
- [ ] **캐시 정책** — `data/cache/`에 어떤 파일 캐시할지 (corpCode, list.json, document.xml)
- [ ] **섹션 정규식 표준** — 4명이 만든 패턴 중 가장 견고한 것 채택
- [ ] **문장 분리 방식** — 단순 정규식 / KSS / kss-light 중 선택
- [ ] **collection_log 컬럼 확정** — 위 9개 컬럼 외 추가 필요 여부
- [ ] **Phase 2 실행 환경** — 누가 어떤 머신에서, 몇 회 분할 실행할지
- [ ] **모듈화 정도** — `src/collection.py`로 함수 추출 vs 노트북 그대로 사용

---

## 11. 다음 단계로 가는 인터페이스

이 단계의 출력 = 다음 단계(`02_preprocessing.ipynb`)의 입력:

| 출력물 | 위치 | 다음 단계 사용처 |
|---|---|---|
| 섹션 JSON | `data/interim/{stock}_{year}_sections.json` | 토큰화 입력 |
| passage 후보 | (노트북 내부 DataFrame) | TF-IDF corpus 후보 |
| collection_log | `logs/collection_log.csv` | 분석 N 결정 (성공 행만) |
| raw zip | `data/raw/{stock}_{year}_disclosure.zip` | 재추출 필요 시 fallback |

---

## 참고 자료

- 교수님 가이드: `docs/professor_md/01_assignment_overview.md`, `02_dart_data_collection.md`
- 수집 가이드 HTML: `docs/supplements/versions/v0.2/COLLECTION_데이터수집가이드.html`
- 협업 규칙: `CONTRIBUTING.md`
- 데이터 lineage: `data/README.md`
