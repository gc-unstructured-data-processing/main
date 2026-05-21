#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""통합 v1 보고서 HTML 생성 (실측 + 그림 base64 임베드).
Write 도구 truncate 회피 위해 Python으로 생성."""
from pathlib import Path

B64 = Path("/sessions/blissful-upbeat-volta/mnt/outputs")
OUT = Path("/sessions/blissful-upbeat-volta/mnt/unstructured-data-processing-final-project/members/이동원/notebooks/integrated/v1/REPORT_통합v1.html")

def img(name, cap):
    b = (B64 / f"{name}.b64").read_text()
    return f'<figure><img src="data:image/png;base64,{b}" alt="{cap}"><figcaption>{cap}</figcaption></figure>'

CSS = """
:root{--ink:#101828;--soft:#475467;--line:#e4e7ec;--accent:#2e7d32;--accent-bg:#e8f5e9;--warn:#b45309;--warn-bg:#fef3c7;--bad:#b42318;--bad-bg:#fee4e2;--blue:#1d4ed8}
*{box-sizing:border-box}
body{margin:0;background:#f7f8fa;color:var(--ink);font-family:-apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;line-height:1.65}
.wrap{max-width:980px;margin:0 auto;padding:28px 22px}
.banner{background:#fff;border:1px solid var(--line);border-radius:12px;padding:20px 24px;margin-bottom:20px}
.banner h1{margin:0 0 6px;font-size:21px}
.banner .sub{color:var(--soft);font-size:13px}
.tag{display:inline-block;padding:2px 9px;border-radius:999px;font-size:12px;font-weight:700}
.tag.ok{background:var(--accent-bg);color:var(--accent)}
.tag.warn{background:var(--warn-bg);color:var(--warn)}
.tag.bad{background:var(--bad-bg);color:var(--bad)}
section.card{background:#fff;border:1px solid var(--line);border-radius:12px;padding:20px 24px;margin-bottom:18px}
h2{font-size:17px;margin:0 0 12px;padding-bottom:8px;border-bottom:2px solid var(--accent)}
h3{font-size:14px;color:var(--soft);margin:16px 0 6px;text-transform:uppercase;letter-spacing:.03em}
table{width:100%;border-collapse:collapse;font-size:13px;margin:10px 0}
th{background:#f8fafc;text-align:left;padding:9px 11px;border-bottom:1px solid var(--line);font-size:12px;color:var(--soft)}
td{padding:9px 11px;border-bottom:1px solid var(--line)}
tr:last-child td{border-bottom:0}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:6px 0 4px}
@media(max-width:760px){.kpis{grid-template-columns:1fr 1fr}}
.kpi{background:#f8fafc;border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.kpi .v{font-size:22px;font-weight:800}
.kpi .l{font-size:11px;color:var(--soft)}
figure{margin:14px 0;text-align:center}
figure img{max-width:100%;border:1px solid var(--line);border-radius:8px}
figcaption{font-size:12px;color:var(--soft);margin-top:6px}
.note{background:#f8fafc;border-left:3px solid var(--accent);padding:10px 14px;border-radius:6px;font-size:13px;margin:10px 0}
.note.warn{border-left-color:var(--warn);background:var(--warn-bg)}
code{background:#f1f5f9;padding:1px 6px;border-radius:4px;font-size:12px}
.star{color:#f59e0b;font-weight:700}
footer{color:var(--soft);font-size:12px;text-align:center;padding:18px}
"""

HTML = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>ESG DART 통합 v1 — 단계별 보고서</title>
<meta name="viewport" content="width=device-width,initial-scale=1"><style>{CSS}</style></head><body><div class="wrap">

<div class="banner">
<h1>ESG DART 통합 분석 — 단계별 보고서 <span class="tag ok">integrated v1</span></h1>
<div class="sub">작성: 이동원 · 2026-05-21 · 노트북 <code>esg_dart_integrated_v1.ipynb</code> (Run All 완주·에러 0) · 실측 N=381</div>
<div class="sub" style="margin-top:6px">회의 결정(5/19): ① 381개 다 살리기 ② 분석기 robust 검증 ③ seed 30개 — 모두 충족. 결과는 <b>연관성</b>이며 인과 아님(가이드 04 §4).</div>
</div>

<section class="card">
<h2>핵심 지표</h2>
<div class="kpis">
<div class="kpi"><div class="v" style="color:var(--accent)">381/381</div><div class="l">수집 SUCCESS (100%)</div></div>
<div class="kpi"><div class="v" style="color:var(--blue)">Kiwi 87%</div><div class="l">seed 보존 (Okt 67%)</div></div>
<div class="kpi"><div class="v">N=381</div><div class="l">분석 표본</div></div>
<div class="kpi"><div class="v" style="color:var(--warn)">ρ=0.654</div><div class="l">total_tokens (최강)</div></div>
</div>
<div class="note warn"><b>핵심 발견</b>: ESG feature 중 <b>보고서 길이(total_tokens)가 ρ=0.654로 가장 강한 양의 연관</b>. 등급과 가장 강하게 연결된 것이 ESG 표현 강도가 아니라 공시 분량일 수 있어 <b>cheap-talk/verbosity</b>를 회의에서 반드시 검토해야 합니다.</div>
</section>

<section class="card">
<h2>1. 데이터 수집 (회의 결정 ①)</h2>
<p>127개 상장기업 × 3개 회계연도(2022~2024) = <b>381 firm-year</b> 전수 수집. 김혜성 <code>find_business_report_v2</code>(결산월 무관 + 정정 우선순위: 원본 &gt; 기재정정 &gt; 첨부정정) + 이동원 <code>XMLParser(recover=True)</code> 결합.</p>
<table><tr><th>항목</th><th>값</th></tr>
<tr><td>수집 성공</td><td>381/381 (100%) — FY별 127/127</td></tr>
<tr><td>문서 분량(II+IV+VI)</td><td>평균 34,167자 · 중앙값 25,520 · 범위 4,194~186,911</td></tr>
<tr><td>실패·가짜 0</td><td>0건 (위반금지 #1)</td></tr>
<tr><td>raw 보존</td><td><code>data/raw/*.zip</code> (위반금지 #5)</td></tr></table>
<p class="note">평균 34,167자는 김혜성 독립 수집(34,222자)과 거의 일치 → 수집 로직 교차검증.</p>
{img("fig_01_collection", "그림 1. 연도별 수집 status(전부 SUCCESS) + firm-year 문서 분량 분포")}
</section>

<section class="card">
<h2>2. 형태소 분석기 robust 검증 (회의 결정 ②)</h2>
<p>동일 표본 15개(앞 25,000자 통일)에서 Kiwi·Okt의 seed 30개 보존율 비교.</p>
<table><tr><th>분석기</th><th>seed 보존</th><th>보존율</th><th>사용자 사전</th></tr>
<tr><td><b>Kiwi</b></td><td>26/30</td><td><b>87%</b></td><td><code>add_user_word(NNP, score=50)</code></td></tr>
<tr><td>Okt</td><td>20/30</td><td>67%</td><td>미지원(강제 불가)</td></tr></table>
<p><b>Kiwi PRIMARY 선정.</b> 복합명사 seed 보존이 20%p 높고, score 기반 강제 우선으로 신지영 사례(미등록 11/30 손실)를 방지. <b>Komoran·Kkma 제외 근거</b>: Kkma는 과도 세분화+대용량 corpus 비실용적 느림, Komoran은 미등록어 약함+score 우선권 미지원.</p>
{img("fig_02_analyzer", "그림 2. Kiwi vs Okt — seed 보존율 + 처리 시간")}
</section>

<section class="card">
<h2>3·4. 전처리 + Feature 생성 (회의 결정 ③)</h2>
<p>Kiwi에 seed 30개 <code>NNP score=50</code> 등록(복합명사 보존), 불용어 358개(회사명 1·2자 분리 포함, seed는 제외) 제거. feature는 두 패러다임 병행 — seed/expanded TF-IDF(E·S·G), cosine(E·S·G), <code>g_signal_ratio</code>·<code>esg_signal_ratio</code>, cheap-talk 통제(<code>total_tokens</code>·<code>specificity</code>).</p>
<div class="note">v0.1 비교에서 이동원 seed_tfidf(+)와 김지우 signal_ratio(−)가 다른 부호를 보였으므로, <b>같은 corpus에서 두 측정을 동시 산출</b>해 회의에서 비교할 수 있게 했습니다.</div>
{img("fig_04_features", "그림 4. seed TF-IDF·cosine 분포(E/S/G) + total_tokens vs g_signal_ratio")}
</section>

<section class="card">
<h2>5. 통계·회귀 (N=381)</h2>
<h3>Spearman 순위상관 + Bootstrap 95% CI</h3>
<table><tr><th>feature</th><th>ρ</th><th>p</th><th>95% CI</th><th>판정</th></tr>
<tr><td>total_tokens</td><td><b>0.654</b></td><td>&lt;0.001</td><td>[0.595, 0.705]</td><td><span class="star">★★★</span> 최강(verbosity)</td></tr>
<tr><td>cosine_S</td><td>0.401</td><td>&lt;0.001</td><td>[0.309, 0.479]</td><td>★★★</td></tr>
<tr><td>cosine_E</td><td>0.346</td><td>&lt;0.001</td><td>[0.265, 0.432]</td><td>★★★</td></tr>
<tr><td>seed_tfidf_E</td><td>0.318</td><td>&lt;0.001</td><td>[0.231, 0.413]</td><td>★★★</td></tr>
<tr><td>specificity</td><td>0.267</td><td>&lt;0.001</td><td>[0.167, 0.353]</td><td>★★★</td></tr>
<tr><td>seed_tfidf_G</td><td>0.210</td><td>&lt;0.001</td><td>[0.119, 0.303]</td><td>★★★</td></tr>
<tr><td>seed_tfidf_S</td><td>0.131</td><td>0.010</td><td>[0.039, 0.228]</td><td>★</td></tr>
<tr><td>g_signal_ratio</td><td>-0.067</td><td>0.195</td><td>[-0.166, 0.028]</td><td>무유의</td></tr></table>
<h3>회귀 3종</h3>
<table><tr><th>모형</th><th>β1</th><th>p</th><th>R²/pseudo</th><th>AIC</th></tr>
<tr><td>OLS</td><td>23.06</td><td>0.0006</td><td>0.406</td><td>1257.1</td></tr>
<tr><td>Ordered Logit</td><td>29.19</td><td>0.0020</td><td>—</td><td>1104.7</td></tr>
<tr><td>Binary Logit (A↑)</td><td>8.25</td><td>0.505</td><td>0.238</td><td>396.3</td></tr></table>
<p>Mann-Whitney U: 고등급(A↑) 152 vs 저등급 229에서 seed_tfidf·cosine·total_tokens·specificity 모두 고등급 평균이 유의하게 높음. <code>g_signal_ratio</code>·<code>esg_signal_ratio</code>만 무유의.</p>
{img("fig_05_spearman_ci", "그림 5. Spearman ρ + Bootstrap 95% CI (N=381)")}
</section>

<section class="card">
<h2>6. 알파분석 4종</h2>
<table><tr><th>알파</th><th>요지</th></tr>
<tr><td>① 부호 역전 robustness</td><td>표본 N=10 ρ평균 0.317(양 비율 82%) → N=381 0.401(100% 양). 소표본일수록 변동 큼 — 김지우 표집 편의 발견을 본인 데이터로 재현·정량화</td></tr>
<tr><td>② section_weighted</td><td>II·IV·VI 섹션별 분량과 등급 상관 — 위치별 변별력</td></tr>
<tr><td>③ 업종별 분해</td><td>N≥10 업종 회귀 분해</td></tr>
<tr><td>④ cheap-talk 3종</td><td>log_tokens·specificity·non-material 통제 후 신호 잔존 OLS</td></tr></table>
</section>

<section class="card">
<h2>7. 한계</h2>
<p>① <b>cheap-talk 우려</b>: total_tokens가 최강 연관 → 신호의 상당 부분이 공시 장황함일 수 있음. ② 381은 수업용 pilot panel(대표표본 아님). ③ <code>esg_year=fiscal_year+1</code>은 시점 식별 아님. ④ 기업·연도 고정효과 미통제. ⑤ 분석기 의존성 잔존.</p>
<div class="note">상세 발전 과제는 <code>GUIDE_발전제안_v1.md</code> / <code>.html</code> 참조.</div>
</section>

<footer>ESG DART 통합 분석 v1 · 이동원 · 2026-05-21 · 회의·발표용 시각 자료 (그림 base64 임베드)</footer>
</div></body></html>"""

OUT.write_text(HTML, encoding="utf-8")
print("REPORT HTML 작성:", len(HTML), "chars →", OUT.name)
