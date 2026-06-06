# ESG DART 4인 최신 비교 — 전문가 30단계 분석

생성일: 2026-05-23  
대상: 김지우 0523 업데이트, 신지영 0523 업데이트1 전체 진행본, 기존 김혜성·이동원 결과

## 통합 요약
- 신지영 업데이트1은 381/381 수집, seed 30 보존, FastText 확장, θ=.55~.75 sweep, Spearman/MWU/회귀/알파까지 정리했습니다.
- 새 업데이트에서 seed 희소성, G 단어의 법정공시성, E/S/G 빈도 466배 불균형, 일반 경영 용어 노이즈 해석이 추가되어 교수님 질문 대응력이 좋아졌습니다.
- 다만 업데이트1 노트북은 출력 74개와 오류 0개가 보존되어 있지만 code cell execution_count가 모두 비어 있어 제출 전 Run All 확인이 필요합니다.
- 김지우 업데이트는 KOSPI 기반 심층 robustness, sign reversal, verbosity confounding, governance cheap-talk 해석을 크게 보강했습니다.
- 최종 본선 산출물은 김혜성/신지영/이동원의 381 전수 재현성과 김지우의 cheap-talk 해석을 결합하는 구성이 가장 강합니다.
- HTML은 동적 innerHTML 표 생성을 쓰지 않고 정적 테이블로 구성해 <P>, <TABLE> 같은 태그 문자열이 레이아웃을 깨지 않도록 했습니다.

## 종합 점수
| 구성원 | 역할 | 표본 | 점수 | 주요 근거 |
|---|---|---|---:|---|
| 김지우 | cheap-talk · robustness · FE | N=243 수집 / N=209 회귀 | 51/60 | full sample g_signal_ratio ρ=-0.1952, p=0.0046; N=30 양의 ρ 발생률 13.5% |
| 김혜성 | 381 수집 코어 · fastText θ sweep | N=381 전수 | 58/60 | 381/381 수집 성공 핵심 로직; fastText θ=.55/.60/.65/.70 sweep |
| 이동원 | 통합 v1 · 재현성 · 381 분석 | N=381 전수 | 53/60 | total_tokens ρ=0.654***; seed_tfidf_E ρ=0.318***; cosine_S ρ=0.401*** |
| 신지영 | 381 전체 재실행 · fastText 확장 | N=381 전수 | 54/60 | θ=.55~.75 sweep과 seed 인사이트 보강; execution_count 공란은 제출 전 확인 필요 |

## 시각화 보강
| 차트 | 핵심 메시지 |
|---|---|
| 종합 점수 막대 | 김혜성 58/60, 신지영 54/60, 이동원 53/60, 김지우 51/60 |
| 표본 커버리지 | 김혜성·이동원·신지영은 381 전수, 김지우는 KOSPI 심층 robustness 축 |
| 신지영 Spearman | total_word_count ρ=.650, reference_cosine_mean ρ=.421, seed_tfidf_score ρ=.382 |
| 김지우 cheap-talk | raw G ρ=-.195, 직교화 후 ρ=.058, N=30 양의 ρ 발생률 13.5% |
| 30단계 준수 분포 | 충족 항목 수: 김지우 22, 김혜성 28, 이동원 25, 신지영 24 |
| 교수님 가이드 리스크 축 | 식별자·cheap-talk은 강하고, 분석기 제외근거와 사전확장 채택/기각 로그는 추가 보강 필요 |

## 신지영 업데이트1 추가 인사이트
| 인사이트 | 보고서 반영 의미 |
|---|---|
| 희소 seed 5개 | 넷제로 9회, 부패방지 8회, 교육훈련 17회 등 seed-only 한계를 보여 expanded dictionary 필요성의 직접 근거가 됨 |
| G seed 과다 등장 | 이사회 7,928회, 사외이사 7,460회, 주주 7,329회처럼 법정공시성 반복이 강해 G 점수 cheap-talk 해석 필요 |
| 차원 빈도 466배 불균형 | 이사회 7,928회 vs 교육훈련 17회로 E/S/G raw frequency 직접 비교 금지 근거가 됨 |
| 일반 경영 용어 노이즈 | 시장, 위험, 자산, 영업 같은 고빈도 단어가 cosine/embedding 분석에 노이즈가 될 수 있음을 명시 |
| θ sweep 보강 | θ=.55/.60/.65/.70/.75별 E/S/G 확장 크기를 비교하고 최종 θ=.65를 선택 |

## 교수님 가이드와 숨은 의도 9가지
| 코드 | 의도 | 이번 비교에서 본 포인트 |
|---|---|---|
| H1 | 정답 표현보다 선택의 정당성 | 왜 이 feature와 모형을 선택했는지, 버린 대안의 한계까지 설명 |
| H2 | cheap-talk 정면화 | 분량·verbosity 통제 없이는 ESG 언어 강도가 말의 양일 수 있음 |
| H3 | 분석기 선택/제외 근거 | Kiwi뿐 아니라 Okt/Komoran/Kkma를 왜 버렸는지 |
| H4 | expanded는 자동 정답 아님 | θ sweep, 후보 검토, 잡음 제거 로그가 가점의 본체 |
| H5 | validity 없이 회귀 금지 | Spearman·MWU·Bootstrap이 회귀 전 안전장치 |
| H6 | 작은 ρ 과장 금지 | 유의성과 효과크기는 별도 |
| H7 | pilot vs full sample | 소표본 부호는 쉽게 뒤집힘 |
| H8 | 거버넌스/boilerplate cheap-talk | G 어휘는 의례적 공시일 수 있음 |
| H9 | E/S/G 차원 매칭 주의 | 통합 ESG 등급과 차원별 언어를 무리하게 등치 금지 |

## 30단계 정밀 비교
| # | 항목 · 가이드 · 숨은 의도 | 김지우 | 김혜성 | 이동원 | 신지영 |
|---:|---|---|---|---|---|
| 1 | 표본 규모 — 최대 381 firm-year 시도필수📕 01 §127 / 02 §117·123 / 🧭 표본 편의가 ρ 부호까지 뒤집을 수 있음 | 🟡 부분KOSPI 81×3=243 수집, 회귀 N=209 | ✅ 충족381 전수 수집 기준 | ✅ 충족381 전수 통합 | ✅ 충족381/381 SUCCESS |
| 2 | 식별자 키 — stock_code×fiscal_year위반금지📕 02 §35 / 🧭 회사명 join은 silent mismatch 위험 | ✅ 충족5-key 원칙 | ✅ 충족stock_code/corp_code | ✅ 충족복합키 | ✅ 충족회사명 133 vs stock_code 127 직접 진단 |
| 3 | stock_code zfill(6) 정규화숨은의도📕 02 식별자 / 🧭 005930 손실 방지 | ✅ 충족zfill 명시 | ✅ 충족6자리 확인 | ✅ 충족준수 | ✅ 충족길이분포 {6:381} |
| 4 | 타이밍 — esg_year=fiscal_year+1필수📕 01 §70 / 02 §37 / 🧭 공시→평가 lag, 인과 아님 | ✅ 충족명시 | ✅ 충족정렬 | ✅ 충족준수 | ✅ 충족연도분포 127×3 |
| 5 | 실패 행 처리 — 가짜 0 금지위반금지📕 01 §98 / 02 §172 / 🧭 결측 0 대체 금지 | ✅ 충족salvage_log, KCGS_NA 제외 | ✅ 충족실패 13건 복구 | ✅ 충족status/reason | ✅ 충족FAIL=0, 원칙 명시 |
| 6 | raw 원문 보존 + lineage 로그필수📕 02 §145·176 / 🧭 원자료 보존과 감사 로그 | ✅ 충족lineage_audit/salvage | ✅ 충족raw/JSON 캐시 | ✅ 충족corpus_381 캐시 | ✅ 충족collection_meta + corpus 381 |
| 7 | II/IV/VI 섹션 선택필수📕 01 §99 / 02 §137 / 🧭 관련 섹션 한정 | ✅ 충족729 sections | ✅ 충족직접 추출 | ✅ 충족본문 추출 | ✅ 충족section_chars 기록 |
| 8 | XML 직접 파싱위반금지📕 02 §94 / 🧭 LLM passage 신뢰 금지 | ✅ 충족직접 처리 | ✅ 충족lxml 구조 진단 | ✅ 충족recover parser | ✅ 충족document.xml/SECTION 진단 |
| 9 | firm-year 1행 집계필수📕 01 §100 / 03 §32 / 🧭 firm-year document 표준 | ✅ 충족firm_year_documents_v2 | ✅ 충족II/IV/VI 통합 | ✅ 충족feature 1행 | ✅ 충족corpus JSON firm-year |
| 10 | 형태소 분석기 robust 비교회의결정📕 5·19 회의 / 🧭 선택 근거 필요 | 🟡 부분Kiwi+exp_B/E/F, Okt 직접표 약함 | ✅ 충족Kiwi/Okt 8지표 | ✅ 충족87% vs 67% | 🟡 부분Kiwi 사용, Okt 비교 없음 |
| 11 | Komoran·Kkma 제외 근거숨은의도📕 5·19 회의 / 🧭 왜 안 썼는가 | 🟡 부분제외근거 약함 | 🟡 부분보강 필요 | ✅ 충족정성+정량 근거 | 🟡 부분제외근거 부족 |
| 12 | seed 복합명사 보존필수📕 03 §90 / 🧭 seed 무결성 | ✅ 충족NNP score=50 | ✅ 충족score 방식 | ✅ 충족seed 30 등록 | ✅ 충족30개 전부 보존 |
| 13 | 불용어·boilerplate 제거필수📕 03 §56–58 / 🧭 공시 잡음 제거 | ✅ 충족STOPWORDS/G 보호 | ✅ 충족358개 | ✅ 충족회사명/boilerplate | ✅ 충족회사명/숫자/법률·회계 제거 |
| 14 | seed TF-IDF (E/S/G)필수📕 03 §124–130 / 🧭 직접 ESG 언어 강도 | ✅ 충족E/S/G + ratio | ✅ 충족seed_score | ✅ 충족E ρ=0.318*** | ✅ 충족seed_tfidf_score |
| 15 | expanded dictionary필수📕 01 §101 / 03 §90 / 🧭 자동확장+큐레이션 | 🟡 부분방법론/honest gap | ✅ 충족expanded 56 | 🟡 부분manual 7 | ✅ 충족expanded 394 |
| 16 | fastText 직접 학습가점📕 03 §90 / 🧭 산업특화 임베딩 | 🟡 부분절차 중심 | ✅ 충족직접 학습 | ⛔ 미흡미구현 | ✅ 충족gensim FastText 완료 |
| 17 | θ sweep필수📕 01 §102 / 03 §120 / 🧭 임계 calibration | 🟡 부분frame 제시 | ✅ 충족θ sweep | ⛔ 미흡미실행 | ✅ 충족θ=.55~.75 sweep, θ=0.65 선택 |
| 18 | 후보 직접 검토·잡음 제거필수📕 02 §76 / 03 §122 / 🧭 회사명/일반어 잡음 제거 | 🟡 부분기준 제시 | ✅ 충족후보 검토 | 🟡 부분manual 제한 | 🟡 부분채택/기각 로그 부족 |
| 19 | 기준 문장 cosine선택📕 01 §55–59 / 🧭 보조 측정 | ➖ 해당없음ratio 중심 | ✅ 충족E/S/G cosine | ✅ 충족cosine_S ρ=0.401*** | ✅ 충족reference_cosine_mean ρ=0.4213 |
| 20 | 다중공선성 회피필수📕 03 §132 / 🧭 VIF 폭증 방지 | ✅ 충족VIF/joint/orthogonalization | ✅ 충족상관 진단 후 분리 | ✅ 충족동시투입 회피 | 🟡 부분VIF 제한 |
| 21 | Spearman 검증필수📕 03 §166 / 🧭 회귀 전 validity | ✅ 충족Spearman+Bootstrap | ✅ 충족차원매칭 | ✅ 충족Spearman+CI | ✅ 충족ρ=0.6505 등 |
| 22 | Mann-Whitney/평균차필수📕 03 §190–192 / 🧭 분포 차이 증거 | ✅ 충족MWU | ✅ 충족t/MW | ✅ 충족A이상 vs 미만 | ✅ 충족A이상 vs B+이하 |
| 23 | 약한 연관 신중 해석숨은의도📕 03 §188 / 04 §89 / 🧭 유의성≠실질 의미 | ✅ 충족instability finding | ✅ 충족약한 연관 라벨 | ✅ 충족효과크기 주의 | ✅ 충족verbosity dominance 명시 |
| 24 | OLS/Ordered/Binary 모형필수📕 03 §221–274 / 🧭 서열변수 고려 | ✅ 충족3종+FE | ✅ 충족Ordered 중심 | ✅ 충족3종 비교 | ✅ 충족3종 모두 |
| 25 | cheap-talk 통제변수숨은핵심📕 03 §234 / 04 §46 / 🧭 분량 통제 필수 | ✅ 충족log_tokens/직교화 | ✅ 충족n_tokens | ✅ 충족total_tokens 핵심 | ✅ 충족total_word_count 통제 |
| 26 | industry/year FE선택·가점📕 03 §164 / 🧭 패널 보강 | ✅ 충족FE 투입 | 🟡 부분FE 제한 | 🟡 부분pooled 중심 | 🟡 부분FE 없음 |
| 27 | cheap-talk 정면 검토숨은핵심📕 04 §46 / 🧭 연구 질문 중심 | ✅ 충족Alpha 1~4 | ✅ 충족G 진단 | ✅ 충족specificity 등 | ✅ 충족분량/section alpha |
| 28 | 알파분석 이유·결과·한계필수📕 01 §105 / 04 §93 / 🧭 좋은 알파 조건 | ✅ 충족sign reversal/governance | ✅ 충족section mechanism | ✅ 충족4축 alpha | ✅ 충족section/cheap-talk |
| 29 | 인과 아닌 연관·한계위반금지급📕 04 §4 / 🧭 anchor 한계 인정 | ✅ 충족KOSPI/anchor 한계 | ✅ 충족구체 한계 | ✅ 충족timing/FE 한계 | ✅ 충족인과 아님 명시 |
| 30 | 제출 형식·재현성필수📕 04 §1·§5 / 🧭 실행·출력·비밀키 | ✅ 충족145셀, 출력105, 오류0 | ✅ 충족출력 보존 | ✅ 충족Run All 오류0 | 🟡 부분93셀, 출력74, 오류0; execution_count 공란 |

## 최종 채택 제안
| 영역 | 권장 베이스 | 이유 |
|---|---|---|
| 수집/lineage | 김혜성 + 신지영 + 이동원 | 381 전수, 수집 함수, 재현성 결합 |
| 전처리/seed | 신지영 + 이동원 + 김혜성 | score=50 seed 보존 + Kiwi/Okt 근거 |
| 사전확장 | 김혜성 + 신지영 | θ sweep 근거와 394개 expanded 실행 결합 |
| validity/회귀 | 신지영 + 이동원 | 381 Spearman/MWU/OLS/Ordered/Binary |
| cheap-talk/알파 | 김지우 + 이동원 + 신지영 | 부호역전, verbosity, section alpha 결합 |

## 남은 보강 포인트
- 신지영 업데이트1의 θ sweep은 강점이지만 expanded 후보에 고유명사·잡음 후보가 일부 남아 있어 채택/기각 예시 로그를 붙이면 더 안전합니다.
- Komoran·Kkma 제외 근거를 발표 Q&A용으로 3~5줄 명시하면 분석기 선택 방어가 좋아집니다.
- 업데이트1 노트북은 출력은 보존되어 있으나 execution_count가 모두 공란이므로 제출 직전 Run All 결과 확인 또는 실행 카운트 복원이 필요합니다.
- 신지영 381 분석의 강한 total_word_count 효과는 cheap-talk 통제 설명과 함께 제시해야 과장 해석을 피할 수 있습니다.
