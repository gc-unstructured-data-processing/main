# ESG DART 통합 v1 — 10단계 진단 · 발전 제안

> **작성**: 이동원 · **날짜**: 2026-05-21 · **대상**: `esg_dart_integrated_v1.ipynb` (Run All 완주, N=381)
> 전문가 10단계 진단 + 발전 우선순위. 회의 결정(5/19) 준수 여부 + 5/23 회의·최종 제출 대비.

---

## A. 실측 요약

| 항목 | 값 |
|---|---|
| 수집 | 381/381 SUCCESS (100%) |
| 분석기 PRIMARY | Kiwi (seed 보존 87% vs Okt 67%) |
| 분석 표본 N | 381 (KCGS 등급 매칭) |
| 최강 연관 | total_tokens ρ=0.654*** (cheap-talk 우려) |
| seed_tfidf_E | ρ=0.318*** (pilot 0.606 → 약화) |
| g_signal_ratio | ρ=-0.067 (무유의) |
| 회귀 | OLS β=23.06 p=0.0006 R²=0.406 · Ordered β=29.19 p=0.002 |

---

## B. 10단계 진단

### 1. 표본·식별자 — 정상 ✅
381 firm-year 전수, `stock_code.zfill(6)`, `stock_code × fiscal_year` 키. 회의 결정 "381 다 살리기" 충족. 위반금지 #2·#7 준수.

### 2. 수집 lineage — 정상 ✅
김혜성 `find_business_report_v2`(결산월 무관 + 정정 우선순위) + 이동원 `recover` parser로 381/381 SUCCESS. 비12월 결산도 포착. raw ZIP 보존(위반금지 #5). 가짜 0 없음(위반금지 #1).

### 3. XML 파싱 robustness — 정상 ✅
`XMLParser(recover=True)` + TITLE 로마숫자 + TABLE 제거 + P 추출. 깨진 XML도 복구. 평균 34,167자 추출(김혜성 34,222자와 일치 → 로직 교차검증).

### 4. 형태소 분석기 선정 — 정상 ✅ (근거 명확)
Kiwi 87% vs Okt 67% seed 보존 → Kiwi PRIMARY. Komoran·Kkma 제외 근거(속도·미등록어·score 미지원) 문서화. **단 주의**: 비교 표본이 15개(앞 25,000자)로 한정됨 → 발전 항목 ⑨.

### 5. seed 보존 — 정상 ✅
Kiwi `add_user_word(NNP, score=50)`로 복합명사 보존. 신지영 사례(미등록 11/30 손실) 회피.

### 6. total_tokens 최강 연관 — 주의 ⚠️ (핵심 발견)
`total_tokens` ρ=0.654로 ESG feature 중 가장 강함. **공시 분량 자체가 등급과 가장 강하게 연결** → cheap-talk/verbosity 우려. 발전 항목 ⑥에서 통제 강화 필요.

### 7. seed_tfidf_E 약화 — 주의 ⚠️
pilot(N=29) ρ=0.606 → 전체(N=381) ρ=0.318. 양의 유의는 유지하나 효과 약화. 김지우 발견(소표본 spurious +ve)과 정합 — 알파 ①에서 N별 ρ 변동 정량 확인.

### 8. signal_ratio 무유의 — 주의 ⚠️
`g_signal_ratio` ρ=-0.067(무유의). 김지우 N=210의 -0.197(유의 음)보다 약함. 측정 패러다임(TF-IDF 강도 vs 토큰 비율) + corpus 차이. 회의에서 measurement 합의 필요.

### 9. 분석기 비교 표본 한정 — 발전 🟡
현재 Kiwi/Okt 비교가 표본 15개(앞 25,000자)뿐. 발전: 381 전체 corpus에서 비교(시간 소요) 또는 표본 확대로 보존율 근거 강화.

### 10. 알파 base 마련 — 알파 🟣
부호 역전 robustness(N별 ρ)·section_weighted·업종 분해·cheap-talk 3종 모두 실행. 단 expanded dictionary fastText·고정효과·section 점수화는 미완 → 발전 항목.

---

## C. 발전 우선순위

| # | 발전 과제 | 우선도 | 근거 | 소요 |
|---|---|---|---|---|
| 1 | **cheap-talk 3종 정교화** (specificity·commitment·non-material) 통제 후 신호 잔존 검증 | 🔴 즉시 | total_tokens ρ=0.654 → verbosity 분리 필수 | 1시간 |
| 2 | **measurement 합의** (seed TF-IDF vs signal_ratio) + 동시 회귀 | 🔴 즉시 | 부호·유의가 측정에 따라 갈림 (5/23 안건) | 회의 |
| 3 | **expanded dictionary fastText 확장** (θ sweep + 상위 100단어 검토 + 회사명 제외) | 🟡 중기 | 가이드 03 line 90~122 미충족. 김혜성 5개 희소 seed + 김지우 G_SIGNAL 5종 부재 근거 | 1~2시간 |
| 4 | **기업·연도 고정효과 패널 회귀** | 🟡 중기 | 현재 pooled OLS — 기업 특성 교란 가능 (김지우 §6 한계) | 1시간 |
| 5 | **section_weighted 점수화** (II/IV/VI 가중) | 🟡 중기 | section_chars 로깅됨, 점수화 미실행. 가이드 04 §3-1 알파 1순위 | 1시간 |
| 6 | **분석기 전체 corpus 비교** | 🟢 보강 | 현재 표본 15 → 보존율 근거 강화 | 30분 |
| 7 | **OrderedLogit 해석 정교화** | 🟢 보강 | N=381에서 안정(p=0.002), 계수 해석 추가 | 30분 |

---

## D. 회의 결정 준수 체크 (위반 없음)

| 회의 결정 | 준수 | 증거 |
|---|---|---|
| ① 381개 다 살리기 | ✅ | 381/381 SUCCESS |
| ② 분석기 robust 검증 후 결정 | ✅ | Kiwi 87% vs Okt 67% + Komoran/Kkma 제외 근거 |
| ③ seed 30개 활용 | ✅ | Kiwi user dict score=50, 30개 등록 |
| 전처리까지 통합 + 알파분석 | ✅ | 단일 노트북, 알파 4종 실행 |

---

## E. 5/23 회의 준비 메모

가장 중요한 결정은 **cheap-talk(total_tokens) 통제 방식**과 **measurement 채택**입니다. total_tokens가 가장 강한 신호인 현 상태로는 "ESG 표현이 등급과 연관"이라는 주장이 "긴 보고서가 등급과 연관"으로 환원될 위험이 있습니다. 발전 항목 1(cheap-talk 3종)을 회의 전 또는 직후 우선 실행해, verbosity 통제 후에도 seed/cosine 신호가 살아남는지 확인하는 것을 권장합니다.
