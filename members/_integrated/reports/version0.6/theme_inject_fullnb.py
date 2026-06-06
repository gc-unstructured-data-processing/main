# 설명포함본.ipynb 전체 nbconvert HTML에 가독성 테마 + 헤더 배너 주입
# (내용은 그대로 두고 스타일만 덧입힘 — 모든 셀/출력/이미지 보존)
import io, sys

SRC = "members/_integrated/_tmp_full_nb.html"
OUT = "members/_integrated/research/ipynb_내용_전체_이동원.html"

html = io.open(SRC, encoding="utf-8").read()

THEME = r"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@300;400;500;700;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style id="readability-theme">
:root{
  --paper:#f4f1ea; --card:#fffdf8; --ink:#1a1c1f; --ink-soft:#42454b; --ink-faint:#76787f;
  --rule:#dcd8cd; --teal:#15605a; --navy:#1f3a5f; --crimson:#9a2b1f;
}
/* 전체 배경/본문 */
body, .jp-Notebook{ background:var(--paper) !important; }
body{ -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility; }
.jp-Notebook{
  max-width:1000px !important; margin:0 auto !important;
  padding:8px clamp(16px,4vw,40px) 120px !important;
}
/* 마크다운 가독성 */
.jp-RenderedMarkdown{
  font-family:"Noto Sans KR",sans-serif !important;
  font-size:16px !important; line-height:1.85 !important; color:var(--ink-soft) !important;
}
.jp-RenderedMarkdown p{ margin:12px 0 !important; }
.jp-RenderedMarkdown strong{ color:var(--ink); font-weight:700; }
.jp-RenderedMarkdown h1,.jp-RenderedMarkdown h2,.jp-RenderedMarkdown h3,.jp-RenderedMarkdown h4{
  font-family:"Gowun Batang",serif !important; color:var(--ink) !important; letter-spacing:-.01em;
  line-height:1.3 !important;
}
.jp-RenderedMarkdown h1{ font-size:1.9em !important; border-bottom:3px double var(--ink);
  padding-bottom:.25em; margin:1.6em 0 .6em !important; }
.jp-RenderedMarkdown h2{ font-size:1.45em !important; border-bottom:1px solid var(--rule);
  padding-bottom:.2em; margin:1.4em 0 .5em !important; color:var(--teal) !important; }
.jp-RenderedMarkdown h3{ font-size:1.2em !important; margin:1.2em 0 .4em !important; }
.jp-RenderedMarkdown h4{ font-size:1.05em !important; color:var(--navy) !important; }
.jp-RenderedMarkdown blockquote{
  border-left:4px solid var(--teal); background:#eef4f2; border-radius:0 8px 8px 0;
  padding:10px 18px !important; margin:16px 0 !important; color:var(--ink-soft) !important;
}
/* 표 */
.jp-RenderedMarkdown table{
  border-collapse:collapse !important; margin:16px 0 !important; background:var(--card);
  border:1px solid var(--rule); font-size:14px; box-shadow:0 10px 24px -26px rgba(0,0,0,.5);
}
.jp-RenderedMarkdown th{ background:var(--ink) !important; color:var(--paper) !important;
  padding:9px 13px !important; text-align:left; font-weight:600; }
.jp-RenderedMarkdown td{ padding:8px 13px !important; border-bottom:1px solid #ebe7dc !important;
  color:var(--ink-soft); }
.jp-RenderedMarkdown tr:nth-child(even) td{ background:rgba(236,231,220,.4); }
.jp-RenderedMarkdown code{ font-family:"JetBrains Mono",monospace !important; font-size:.86em;
  background:#ece7da; border-radius:4px; padding:1px 5px; color:var(--crimson); }
/* 코드 셀 */
.jp-CodeMirrorEditor, .jp-Editor, .highlight, .jp-InputArea-editor{
  font-family:"JetBrains Mono",monospace !important; font-size:13px !important;
}
.jp-Cell{ margin:6px 0 !important; }
.jp-InputArea-editor{ border-radius:8px !important; }
/* 출력(그림) 가운데 정렬·여백 */
.jp-OutputArea-output img{ border-radius:8px; box-shadow:0 8px 22px -20px rgba(0,0,0,.5); }
.jp-RenderedImage{ text-align:center; }
/* 헤더 배너 */
#nb-banner{
  max-width:1000px; margin:28px auto 8px; padding:0 clamp(16px,4vw,40px);
  font-family:"Noto Sans KR",sans-serif;
}
#nb-banner .tag{ font-family:"JetBrains Mono",monospace; font-size:11px; letter-spacing:.34em;
  text-transform:uppercase; color:var(--ink-faint); margin:0 0 12px; }
#nb-banner h1{ font-family:"Gowun Batang",serif; font-weight:700; color:var(--ink);
  font-size:clamp(26px,4.6vw,40px); line-height:1.18; margin:0; letter-spacing:-.015em; }
#nb-banner h1 .em{ color:var(--teal); }
#nb-banner .lead{ margin:16px 0 0; max-width:820px; font-size:16px; color:var(--ink-soft); line-height:1.75; }
#nb-banner .lead b{ color:var(--ink); }
#nb-banner .chips{ margin-top:16px; display:flex; flex-wrap:wrap; gap:8px; }
#nb-banner .chip{ font-family:"JetBrains Mono",monospace; font-size:12px; background:var(--card);
  border:1px solid var(--rule); border-radius:999px; padding:6px 13px; color:var(--ink-soft); }
#nb-banner .chip b{ color:var(--teal); font-weight:700; }
#nb-banner .rule{ margin-top:22px; border:0; border-top:3px double var(--ink); }
::selection{ background:var(--teal); color:var(--paper); }
</style>
"""

BANNER = r"""
<div id="nb-banner">
  <p class="tag">ESG DART · 3조 · 분석 노트북 전체 (설명포함본)</p>
  <h1>비정형 데이터 처리 Final Term Project<br><span class="em">설명포함본 노트북</span> — 전체 내용</h1>
  <p class="lead">이 문서는 분석 노트북 <b>설명포함본.ipynb</b>의 <b>모든 셀(마크다운·코드·출력·시각화)을 빠짐없이</b> 그대로 옮긴 읽기용 페이지다.
    데이터 수집(§1) → 전처리(§2) → Feature 생성(§3) → 타당성 검증(§4) → 회귀 3종(§5) → 알파 분석 Talk–Walk Gap(§6) → 종합 결론(§7)의
    전 과정을 코드와 결과까지 함께 확인할 수 있다. 보고서가 아니라 <b>노트북 자체의 이해</b>를 위한 자료다.</p>
  <div class="chips">
    <span class="chip">표본 <b>127사 × 3년 = 381 firm-year</b></span>
    <span class="chip">셀 <b>전체 102개</b></span>
    <span class="chip">시각화 <b>6종 포함</b></span>
    <span class="chip">성격 <b>연관·진단 (인과 아님)</b></span>
  </div>
  <hr class="rule">
</div>
"""

# 테마 주입 (</head> 직전)
if "</head>" in html:
    html = html.replace("</head>", THEME + "\n</head>", 1)
else:
    html = THEME + html

# 배너 주입 (<body ...> 직후)
import re
m = re.search(r"<body[^>]*>", html)
if m:
    idx = m.end()
    html = html[:idx] + "\n" + BANNER + html[idx:]
else:
    html = BANNER + html

io.open(OUT, "w", encoding="utf-8").write(html)
print("written:", OUT, "bytes:", len(html.encode("utf-8")))
