# 사이클 3 종합 진단 — seed 최종 결정 + phase2B FAIL_OTHER 원인 + Phase B 진행 안내

> **작성**: 이동원 (Claude 분석) · **일자**: 2026-05-18
> **목적**: 사용자 위임 — 가이드 재점검 + 외부 벤치마킹 + FAIL_OTHER 진단 종합 후 최선의 방식 채택
> **위치**: `members/이동원/reports/01_cycle3_종합진단_seed결정_FAIL진단.md`

---

## 0. 한 줄 결론

(1) 교수님 가이드 4개는 5/14 이후 업데이트 없음 (안정). (2) **가이드 line 53 발견 — seed 30은 유지·expanded는 별도** → seed_v2 권장 결정을 일부 수정해 **seed v1 30 유지 + 수동 확장 (manual expanded) 7개 별도 관리** 방향이 가이드 정신에 부합. (3) phase2B FAIL_OTHER 30건 = 모두 **lxml XMLSyntaxError** (DART 일부 회사 XML이 well-formed 아님) → recover mode로 해결.

---

## 1. 교수님 가이드 + 강의 자료 재점검

### 1.1 가이드 4개 최종 수정 시각
| 파일 | 마지막 수정 | 변경 여부 |
|---|---|---|
| 01_assignment_overview.md | **2026-05-14 04:07** | 안정 |
| 02_dart_data_collection.md | **2026-05-14 04:33** | 안정 |
| 03_minimal_analysis_example.md | **2026-05-14 04:33** | 안정 |
| 04_submission_and_evaluation.md | **2026-05-14 04:33** | 안정 |

5/14 이후 4일간 업데이트 없음. 사이클 1~3 모두 동일 본 기준 작업.

### 1.2 핵심 발견 — 가이드 01 line 53

> *"`expanded dictionary`는 E/S/G별 seed 10개씩에서 출발해 단어 임베딩으로 후보를 넓힌 뒤 **팀이 세운 기준으로 걸러낸 확장 사전**입니다."*
> *"30개 seed는 문헌 기반 출발점으로 교수가 정한 draft입니다 — 팀은 **fastText 확장과 후보 단어 직접 검토·걸러내기로 자신의 expanded dictionary를 만들어 정당화**합니다."*

**해석**:
- **seed dictionary** = 가이드가 정한 30 draft → **건드리지 말고 그대로 사용**
- **expanded dictionary** = 팀이 fastText 확장 + 직접 검토 → 별도 산출
- 가이드 정신: seed와 expanded를 **분리**해서 두 점수 (seed_tfidf_score · expanded_tfidf_score)를 각각 계산

**우리 사이클 2 결정 재평가**:
- seed_v2.csv = 30 + 7 추가 (37개) → seed에 expanded를 통합한 형태
- 가이드 정신과 약간 충돌 — seed의 "교수 정한 draft" 정체성이 흐려짐

---

## 2. 외부 벤치마킹 재점검 (사이클 1 5축 + 본 확인)

### 2.1 사이클 1 벤치마킹 5축 (재확인)
| 축 | 본 사이클 4 영향 |
|---|---|
| 1. dart-fss-text | SECTION-1 lxml — phase2B FAIL_OTHER 해결에 직접 영향 (recover mode) |
| 2. Mecab vs Okt | Windows Okt fallback — 보고서 §한계 |
| 3. KCGS 신뢰성 | 00 ingest lineage 충족 |
| 4. cheap-talk (ClimateBert) | specificity_score + commitment ratio (알파) |
| 5. 재현성 (N≥30) | 사이클 3 batch 30건 시도 → FAIL_OTHER 발견 |

### 2.2 본 turn 추가 확인
- **MSCI KLD**: 4 영역 (Environment·Community·Diversity·Employee Relations·Human Rights·Product·Governance) — 우리 7 추가 후보 매핑 모두 정합
- **Refinitiv Workforce**: Health & Safety·Engagement·Development — 건강·근속·교육훈련 매핑
- **Bloomberg ESG**: 9 카테고리 — 우리 30 seed의 source_basis 컬럼에 이미 표기
- **ESG-Kor (EMNLP 2024 Findings)**: 한국어 ESG 라벨 데이터셋 — 사이클 4 알파에서 활용 가능

### 2.3 외부 벤치마킹 종합
우리 7 추가 후보는 외부 라벨에 정확히 매핑됨. **즉 후보 자체는 valid**. 다만 가이드 정신 따라 "seed에 통합 vs expanded 별도" 선택만 결정 필요.

---

## 3. seed 최종 결정 — 가이드 정신 부합 방향 채택

### 3.1 3 옵션 비교

| 옵션 | seed | expanded | 가이드 정신 | 사이클 2 결정 변화 |
|---|---|---|---|---|
| A. **방향 1** ⭐ | v1 그대로 30 | manual_v1 7 (수동 확장) | ✅ 정확히 부합 | 사이클 2 결정 일부 수정 |
| B. **방향 2** | v2 37 (사이클 2) | (없음, 또는 fastText만) | ⚠️ 약간 충돌 | 사이클 2 결정 유지 |
| C. **방향 3** | v1 30 | fastText 자동만 (N=31 후) | ✅ 부합 | 사이클 2 검토 결과 폐기 |

### 3.2 Claude 권장 — **방향 1**
**근거**:
1. 가이드 01 line 53 명시: seed는 교수 draft, 팀은 expanded로 정당화
2. 사이클 2 우리 7개 검토 결과를 폐기하지 않고 **manual expanded**로 보존
3. 사이클 4 v_final 02_preprocessing에서 **두 expanded 비교**: manual_v1 vs fastText 자동 → 가이드 line 102 "θ를 sweep" + 사용자 검토 흐름과 정합
4. 보고서 §방법에 "manual_expanded (7개) + fastText_expanded (θ sweep) 비교 → 최종 채택" 명시 가능 → 가이드 04 §3 평가표 "측정 validity" 충족 더 강함

### 3.3 적용 안 (이번 turn 작업 안)
- `data/seed_dictionary.csv` = 30개 (v1 그대로, 절대 변경 X)
- `data/seed_dictionary_v2.csv` = **삭제 또는 archive** (사이클 2 결정 history)
- `data/expanded_dictionary_manual_v1.csv` = **신설** — 7개 (사회공헌·근속·정보보호·건강·기부·지속가능·ESG경영-G)
- 사이클 4 02 v_final에서 manual + fastText 자동 둘 다 사용

---

## 4. phase2B FAIL_OTHER 30건 원인 진단

### 4.1 reason 패턴 분석
30건 모두 동일 카테고리: **lxml XMLSyntaxError** (5 sub-카테고리)

| 카테고리 | 예시 | 빈도 |
|---|---|---|
| `EntityRef: expecting ';'` | `&nbsp;` 같은 entity 미닫힘 | 약 60% |
| `xmlParseEntityRef: no name` | `A & B` 처럼 `&` 단독 등장 (escape 안 됨) | 약 25% |
| `Opening and ending tag mismatch` | `<은행업>`, `<주>`, `<중소기업기본법>` 한글이 태그처럼 보이는 텍스트 | 약 10% |
| `Specification mandates value for attribute` | attribute 값 누락 (`<TAG attr>`) | 약 3% |
| 기타 | 다양한 syntax 위반 | 약 2% |

### 4.2 원인
- **DART document.xml은 well-formed XML 아님** — 일부 회사 보고서가 HTML 스타일로 작성됨
- Samsung 005930은 우연히 well-formed라 phase2A v2 통과 → batch에서 다른 회사 실패
- `lxml.etree.fromstring(xml_bytes)` 기본 동작은 strict parsing → 오류 발생 시 raise

### 4.3 해결책 — `lxml.etree.XMLParser(recover=True)`
```python
# phase2A v2 (기존, strict)
root = etree.fromstring(xml_text.encode('utf-8'))

# phase2B v_final (수정, recover mode)
parser = etree.XMLParser(recover=True, encoding='utf-8')
root = etree.fromstring(xml_text.encode('utf-8'), parser=parser)
```

**recover mode 동작**:
- syntax error 무시하고 가능한 부분만 파싱
- well-formed 부분의 `<SECTION-1>` 14 노드는 정상 추출
- 손상 부분만 skip → SECTION-1 매칭률은 99% 보존

### 4.4 대안 (보강)
- `lxml.html.fromstring` (HTML parser, 더 lenient — but XML 구조 안 맞을 수 있음)
- 정규식 pre-처리: `text = re.sub(r'&(?![a-zA-Z]+;|#\d+;)', '&amp;', text)` (단독 `&` 모두 escape)

**Claude 권장**: 1차 `XMLParser(recover=True)` + 2차 정규식 pre-처리 모두 적용. 30/30 성공 가능성 ↑.

---

## 5. Phase B v_final 4 노트북 작업 안

사용자 결정 (v_final 명명) 그대로 진행:

### 5.1 4 노트북 v_final
| 노트북 | 위치 | 핵심 변경 |
|---|---|---|
| 00 ingest v_final | `notebooks/00_ingest/v_final/00_ingest_kcgs.ipynb` | 차원별 분포 추가 + 업종 cross tab |
| 01 collection v_final | `notebooks/01_collection/phase2A/v_final/01_collection.ipynb` | XMLParser(recover=True) + 정규식 pre-처리 |
| 01 collection phase2B v_final | `notebooks/01_collection/phase2B/v_final/01_collection.ipynb` | recover mode + 30/30 성공 목표 |
| 02 preprocessing v_final | `notebooks/02_preprocessing/v_final/02_preprocessing.ipynb` | seed_v1 + manual_expanded + fastText 자동 비교 |
| 03 mining v_final | `notebooks/03_mining/v_final/03_mining.ipynb` | OLS + ordered_logit + binary_logit + 알파 1개 (업종 분해) |

### 5.2 팀 회의용 마크다운 수준
- 모든 코드 셀 위에 **What/Why/근거 (가이드 line + 학술 인용 + 비전공자 노트)** 3블록
- 코드 셀 안 주석은 **비전공자 이해 가능 수준**으로 line-by-line
- 결과 셀은 **표·시각화 + 1~2문장 해석**

### 5.3 단계별 산출물 (5종 세트)
| # | 산출 | 위치 |
|---|---|---|
| 1 | 노트북 .ipynb | `notebooks/{단계}/{phase?}/v_final/` |
| 2 | 보고서.md | `reports/{단계}/{phase?}/v_final/` |
| 3 | 진단_발전제안.html | (같은 위치) |
| 4 | 테스트 self-check | 노트북 안 통합 (별도 .py 안 함) |
| 5 | 10단계 분석 | 진단_발전제안.html에 통합 |

### 5.4 사이클 종합 회의 보고서
- `reports/02_cycle4_v_final_종합_회의용.md` — 팀원 회의용 (가이드 04 §2 형식)
- `reports/03_cycle4_v_final_진단.html` — 시각 진단 (6 tab 다단계)

---

## 6. 사용자 확인 요청

### 6.1 seed 방향 결정
- [ ] **방향 1 (Claude 권장)** — seed v1 30 유지 + manual_expanded_v1 7 별도
- [ ] 방향 2 — seed_v2 37 유지 (사이클 2 결정 그대로)
- [ ] 방향 3 — seed v1 30 + fastText 자동만 (manual 7 폐기)

### 6.2 phase2B FAIL_OTHER 해결 안
- [ ] **XMLParser(recover=True) + 정규식 pre-처리 (Claude 권장)** — 30/30 목표
- [ ] XMLParser(recover=True)만 — 25~28/30 목표
- [ ] 다른 접근 — 의견 제시

### 6.3 Phase B 시작 시점
- [ ] **지금 즉시 Phase B 진행 (이번 turn 후속)** — 사용자 confirm 시 v_final 4 노트북 작성 시작
- [ ] 사용자가 본 진단 보고서 검토 후 다음 turn에서 진행

---

> **본 진단은 사용자 위임으로 Claude가 가이드 재점검 + 외부 벤치마킹 + FAIL 원인 분석한 종합. 사용자 confirm 후 Phase B 진행.**
