---
title: "ESG DART 발표와 제출 안내"
date: 2026-05-31
tags:
  - course/UD
  - project/esg-dart
  - data/OpenDART
aliases:
  - "ESG DART presentation and submission guide"
---

> 이 문서를 읽기 전에 `01_assignment_overview.md`에서 전체 흐름을 먼저 확인하세요.

> 이전 단계: `03_minimal_analysis_example.md`에서 분석 예시 확인 | 이 문서: 발표와 제출 안내

# ESG DART 발표와 제출 안내

분석이 끝났다면, 이제 결과를 정리하고 발표할 차례입니다. 이 문서는 제출물, 마감, 분량, sample/template 위치를 간단히 안내합니다. Short Research Paper를 어떻게 쓸지는 `05_mini_paper_guide.md`를 확인하세요.

## 1. 제출물

| 제출물 | 형식 | 내용 |
|---|---|---|
| 분석 노트북 | `.ipynb` | 데이터 수집, 전처리, feature 생성, 회귀분석 코드와 출력 |
| Short Research Paper (논문형 보고서) | `.docx` | 주요 연구질문과 contribution을 중심으로 데이터·방법·결과·논의·결론을 서술 |

노트북은 코드와 표가 실행 가능한 상태여야 합니다. Short Research Paper는 `.docx`로 제출합니다.

## 2. 제출 일정과 분량

- **제출 마감**: 2026-06-16 화요일 23:59
- **권장 분량**: 본문 6-8쪽
- **최대 분량**: 첫 페이지, 참고문헌, 부록 제외 본문 10쪽
- **샘플**: `sample_mini_paper_esg_dart.docx`
- **템플릿**: `mini_paper_template.docx`

첫 페이지는 제목, 저자명, 수업명·팀명, 초록이 들어가는 페이지입니다. 참고문헌과 부록도 본문 분량에 포함하지 않습니다. 본문은 Introduction부터 Conclusion까지를 뜻합니다.

## 3. 작성 방향

Short Research Paper는 분석 결과를 모두 모아두는 문서가 아닙니다. 주요 연구질문을 중심으로 가장 중요한 결과 1-2개를 고르고, 그 결과가 ESG DART 분석에서 어떤 의미를 갖는지 설명하는 글입니다.

글을 쓸 때는 아래 세 가지를 특히 신경 쓰세요.

- **선택과 집중**: 분석을 많이 보여주기보다, 주요 질문에 필요한 결과를 골라 설명합니다.
- **해석**: 표와 계수를 붙이는 데서 끝내지 말고, 독자가 무엇을 읽어야 하는지 문장으로 설명합니다.
- **조심스러운 주장**: DART 공시 언어와 실제 ESG 성과를 동일시하지 말고, 회귀 결과를 인과관계로 단정하지 않습니다.

Sample 문서는 구조를 참고하기 위한 예시입니다. 제목, 저자명, 팀명, 수치, 문장, 주제, 결론은 모두 예시이므로 그대로 가져다 쓰지 마세요.

## 4. 제출 전 확인

- 노트북을 위에서 아래로 실행했을 때 결과가 재현되는지 확인하세요.
- API key가 노트북, 보고서, 스크린샷에 포함되어 있지 않은지 확인하세요.
- Short Research Paper의 formatting과 섹션 구성은 `05_mini_paper_guide.md`를 따르세요.

## 5. 해석할 때 조심할 점

이 프로젝트는 DART 사업보고서의 **공시 언어**와 KCGS ESG 등급 사이의 관계를 살펴보는 분석입니다. 공시 문장은 실제 ESG 성과 그 자체가 아니며, 회귀 결과도 인과관계가 아니라 연관성으로 읽어야 합니다. 이런 해석상의 주의는 필요할 때 Data, Method, Discussion에서 자연스럽게 설명하고, Conclusion은 주요 결론과 contribution을 정리하는 데 집중하세요.
