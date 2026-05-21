# integrated v1 — 이동원 통합 노트북

회의 결정(5/19) 반영 통합 노트북. 단계 세분화(00/01/02/03) 폐기 → 단일 노트북.

## 구성
- `esg_dart_integrated_v1.ipynb` — 메인 노트북 (Run All 완주·에러 0). 수집→형태소검증→전처리→feature→회귀→알파4종
- `REPORT_통합v1.md` — 단계별 보고서 (데이터·방법·결과·한계, 실측 N=381)
- `outputs/` — feature parquet/csv, 통계 csv, 그림 4종, 캐시(corpus meta·tokens·analyzer)
- `_build_scripts/` — 노트북 빌드 + 캐시 생성 스크립트 (재현용)

## 회의 결정 반영 (위반 불가 — 합의)
1. **381개 다 살리기**: 김혜성 `find_business_report_v2`(결산월 무관+정정 우선순위) + 이동원 `recover` XML parser → 381/381 SUCCESS (100%)
2. **분석기 robust 검증**: Kiwi(87%) vs Okt(67%) seed 보존율 비교 → Kiwi PRIMARY. Komoran/Kkma 제외 근거 문서화
3. **seed 30개 활용**: Kiwi `add_user_word(NNP, score=50)`로 복합명사 보존

## 재현 방법
노트북은 캐시 우선 구조입니다. `outputs/`의 캐시(`collection_meta_381.csv`, `tokens_primary.json`, `analyzer_cache.json`)가 있으면 Run All이 네트워크/토큰화 재계산 없이 빠르게 완주합니다. 캐시가 없는 새 환경(Colab 등)에서는 `.env`의 `API_KEY`로 수집부터 자동 수행합니다.

## 핵심 실측 (N=381)
- total_tokens ↔ KCGS: ρ=0.654*** (가장 강함 — cheap-talk/verbosity 우려)
- seed_tfidf_E: ρ=0.318*** · cosine_S: 0.401*** · cosine_E: 0.346***
- g_signal_ratio: ρ=-0.067 (무유의) — 김지우 N=210 -0.197과 방향 동일하나 약화
- OLS β=23.06 (p=0.0006, R²=0.406) · Ordered Logit β=29.19 (p=0.002)

## 5/23 회의 안건
측정 방식(seed TF-IDF vs signal_ratio) 최종 채택 + cheap-talk(total_tokens) 통제 방식 + 알파 확정 + 역할 분담.
