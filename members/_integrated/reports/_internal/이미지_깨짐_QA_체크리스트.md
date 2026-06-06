# 이미지 깨짐 QA 체크리스트

> 제출용 보고서·HTML에 들어가는 그림은 반드시 이 기준으로 확인한다. 특히 matplotlib/wordcloud는 기본 폰트가 한글 glyph를 지원하지 않으면 `□□□` 네모 글자로 깨진다.

## 진단 결과

| 그림 | 기존 문제 | 원인 판단 | 처리 |
|---|---|---|---|
| `fig_step10_cosine_grade.png` | `rho=nan, p=nan`, 한 점짜리 산점도 | 특정 예시 1건만 그려 상관계수가 정의되지 않음. 글자 깨짐보다 데이터 진단 그림이 보고서용으로 부적절한 문제 | 전체 표본 Spearman rho 막대그래프로 교체 |
| `fig_step10_tokenizer_vocab.png` | 제목 일부 `□□□` | matplotlib 기본 폰트가 한글/특수문자를 지원하지 않음 | `Noto Sans KR` 지정 후 재생성 |
| `fig_step10_theta_sweep.png` | 제목·축 한글 깨짐 가능성 | 동일한 폰트 문제 | `Noto Sans KR` 지정 후 재생성 |
| `fig_step10_section_dim.png` | 제목 일부 `□□□` | 동일한 폰트 문제 | `Noto Sans KR` 지정 후 재생성 |
| `fig_step10_wordcloud.png` | 제목 `seed □□□`, 일부 글자 깨짐 | wordcloud와 matplotlib 제목이 서로 다른 폰트 경로를 사용 | wordcloud `font_path`와 matplotlib `font.family`를 모두 `Noto Sans KR`로 지정 |

## 재생성 방법

```powershell
python members/_integrated/reports/_scripts/refresh_report_v2_assets.py
```

스크립트는 다음 순서로 한국어 폰트를 찾는다.

1. `C:\Windows\Fonts\NotoSansKR-Regular.ttf`
2. `C:\Windows\Fonts\malgun.ttf`
3. `C:\Windows\Fonts\NanumGothic.ttf`

## 최종 확인 기준

- 제목, 축, 범례, 캡션 역할 문구에 `□□□`, `�`, `rho=nan`, `p=nan`이 없어야 한다.
- 이미지가 보고서 본문 수치와 같은 의미를 가져야 한다. 예시 한 건만 그린 진단용 그림은 제출용 본문 그림으로 쓰지 않는다.
- HTML에서 이미지 5개가 모두 정상 로딩되어야 한다.
- 새 그림을 추가할 때는 먼저 이 체크리스트에 한 줄을 추가하고 직접 눈으로 확인한다.
