// ESG DART v0.8 제출본 빌드 스크립트
// 중심: Talk–Walk Gap(말–실행 격차) 알파 + 축 간 선택적 공시
// 형식: 가이드(05_mini_paper_guide) 준수 — 맑은 고딕 10.5pt, 줄간격 160%, A4 여백 25mm, 왼쪽정렬, 페이지번호
// v0.7 형식 피드백 반영: 제목 캐치프레이즈 제거·학번 병기·단어 인용 작은따옴표·
//   단락 첫머리 한 칸 들여쓰기(공백)·초록만 가운데/본문 왼쪽·본문 강조 기울임·표/그림 설명 회색
// v0.8 발표 후 피드백 반영: ①선행연구 검색기준·빈틈+47% 예고(서론) ②Kruskal–Wallis 도구 근거·강건성 2단계(방법3.3/결과4.3)
//   ③gap 수식 명시 ④제출 노트북에 없는 섹션 국소화(구 그림5) 제거→그림 6개로 노트북과 1:1 정합 ⑤직관 비유 소량 보강
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
  Footer, AlignmentType, BorderStyle, WidthType, ShadingType, PageNumber, PageBreak
} = require('docx');
const fs = require('fs');
const path = require('path');

const FONT = '맑은 고딕';
const CONTENT_WIDTH = 9072;
const SZ_BODY = 21; const SZ_ABSTRACT = 20; const SZ_TITLE = 32;   // 제목 16pt
const SZ_H1 = 26; const SZ_H2 = 22; const SZ_CAPTION = 19;          // 1단계 13pt · 2단계 11pt · 표/그림 9.5pt
const SZ_REF = 20; const SZ_AUTHOR = 21; const SZ_COURSE = 19;
const LS_BODY = 384; const LS_ABSTRACT = 360;
const SP_AFTER = 120;
const ASSETS = path.join(__dirname, 'assets');
const INDENT = '　';        // 단락 첫머리 한 칸 들여쓰기(전각 공백) — 프로그램 indent 대신 띄어쓰기
const GRAY = '808080';      // 표/그림 설명 글자색(회색)

function body(text, opts = {}) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 0, after: SP_AFTER, line: LS_BODY, lineRule: 'auto' },
    ...opts,
    children: [new TextRun({ text: INDENT + text, font: FONT, size: SZ_BODY })]
  });
}
// 인라인 강조가 필요한 본문 (parts: [텍스트, 강조?] 배열 — 강조는 기울임)
function rich(parts, opts = {}) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 0, after: SP_AFTER, line: LS_BODY, lineRule: 'auto' },
    ...opts,
    children: parts.map((p, i) => new TextRun({
      text: (i === 0 ? INDENT + p[0] : p[0]), font: FONT, size: SZ_BODY, italics: !!p[1]
    }))
  });
}
function bullet(text) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 0, after: 60, line: LS_BODY, lineRule: 'auto' },
    indent: { left: 360, hanging: 200 },
    children: [new TextRun({ text: '· ' + text, font: FONT, size: SZ_BODY })]
  });
}
function h1(text) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 240, after: 100, line: LS_BODY, lineRule: 'auto' },
    children: [new TextRun({ text, font: FONT, size: SZ_H1, bold: true })]
  });
}
function h2(text) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 160, after: 70, line: LS_BODY, lineRule: 'auto' },
    children: [new TextRun({ text, font: FONT, size: SZ_H2, bold: true })]
  });
}
function cap(text) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 50, after: 70, line: 280, lineRule: 'auto' },
    children: [new TextRun({ text, font: FONT, size: SZ_CAPTION, color: GRAY })]
  });
}
function fig(filename, w, h, alt) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 80, after: 0 },
    children: [new ImageRun({
      type: 'png',
      data: fs.readFileSync(path.join(ASSETS, filename)),
      transformation: { width: w, height: h },
      altText: { title: alt, description: alt, name: alt }
    })]
  });
}
function sp(n = 80) {
  return new Paragraph({ spacing: { before: 0, after: n }, children: [new TextRun('')] });
}
function absPara(text) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 0, after: 80, line: LS_ABSTRACT, lineRule: 'auto' },
    indent: { left: 280, right: 280 },
    children: [new TextRun({ text, font: FONT, size: SZ_ABSTRACT })]
  });
}
const TB = { style: BorderStyle.SINGLE, size: 4, color: 'AAAAAA' };
const BORD = { top: TB, bottom: TB, left: TB, right: TB };
function tc(text, { hdr = false, w, shade } = {}) {
  return new TableCell({
    borders: BORD,
    width: w ? { size: w, type: WidthType.DXA } : undefined,
    shading: shade ? { fill: shade, type: ShadingType.CLEAR } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({
      alignment: AlignmentType.LEFT,
      children: [new TextRun({ text, font: FONT, size: 18, bold: hdr })]
    })]
  });
}
function tbl(headers, rows, colW) {
  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: colW,
    rows: [
      new TableRow({
        tableHeader: true,
        children: headers.map((h, i) => tc(h, { hdr: true, w: colW[i], shade: 'D5E3F5' }))
      }),
      ...rows.map((row, ri) => new TableRow({
        children: row.map((cell, ci) => tc(cell, {
          w: colW[ci], shade: ri % 2 === 1 ? 'F3F6FB' : 'FFFFFF'
        }))
      }))
    ]
  });
}
function note(text) {
  return new Paragraph({
    spacing: { before: 30, after: 90 },
    children: [new TextRun({ text, font: FONT, size: 16, color: GRAY })]
  });
}
function center(text, sz, opts = {}) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 80, line: 320, lineRule: 'auto', ...opts.spacing },
    children: [new TextRun({ text, font: FONT, size: sz, bold: !!opts.bold })]
  });
}

const C = [];

// ===================== TITLE PAGE =====================
C.push(center('사업보고서 ESG 공시 언어와 KCGS 등급의 정합성 진단:', SZ_TITLE, { bold: true, spacing: { before: 760, after: 60, line: 360 } }));
C.push(center('분량 통제 후 거버넌스 신호와 축 간 선택적 공시', SZ_TITLE, { bold: true, spacing: { before: 0, after: 300, line: 360 } }));
C.push(center('김혜성(202231193) · 이동원(202136006) · 김지우(202431626) · 신지영(202431928)', SZ_AUTHOR, { spacing: { before: 0, after: 60 } }));
C.push(center('비정형 데이터 처리 Final Term Project | 3조', SZ_COURSE, { spacing: { before: 0, after: 320 } }));
C.push(center('초록', SZ_H2, { bold: true, spacing: { before: 0, after: 100 } }));
C.push(absPara(
  '본 연구는 상장기업이 사업보고서에 쓴 ESG 관련 표현(말)과 한국ESG기준원(KCGS)이 부여한 외부 ESG 등급(실행)이 ' +
  '기업 단위에서 얼마나 정합적인지를 진단한다. 127개 상장기업의 2022–2024 회계연도 사업보고서 381 firm-year에서 ' +
  '환경(E)·사회(S)·지배구조(G) 어휘 강도를 측정하고, 공시 분량을 통제한 회귀로 등급과의 연관을 확인한 뒤, ' +
  '기업별 말–실행 격차(Talk–Walk Gap)로 공시 정합성을 유형화하였다. 등급과 가장 강하게 연관된 것은 ESG 어휘가 아니라 ' +
  '보고서 분량이었고(Spearman ρ=0.663), 분량·규모를 통제하면 거버넌스 어휘만 독립 신호로 남았다(β=1.955, p<0.001). ' +
  '분량 착시를 제거한 격차로 보면 전체의 44%가 말과 실행이 어긋났고(과잉공시 19%·과소공시 25%), 그중 60%는 3년 내내 ' +
  '같은 유형으로 고착되어 있었다. 유형을 가르는 축은 수익성이 아니라 기업 규모였으며, 격차는 규모를 통제해도 유지되었다(ρ=0.993). ' +
  '나아가 firm-year의 47%가 한 축을 부풀리고 다른 축에는 침묵하는 선택적 공시였는데, 부풀린 축이 사회(S)인 기업은 실제 S등급이 ' +
  '가장 낮아(2.08 대 전체 3.03) 약점을 언어로 가리는 패턴인 반면, 지배구조(G)를 부풀린 기업은 실제 G등급이 평균 이상이어서 ' +
  '강점을 알리는 정당한 신호에 가까웠다. 이 결과는 공시 ESG 어휘량을 성과 대리지표로 그대로 쓰면 안 되며, 평가·투자·공시 의사결정이 ' +
  '분량과 규모를 보정하고 축별로 말–실행 정합성을 따로 점검해야 함을 시사한다. 모든 결과는 연관 관찰이며 인과로 해석하지 않는다.'
));
C.push(new Paragraph({ children: [new PageBreak()] }));

// ===================== 1. Introduction =====================
C.push(h1('1. 서론'));
C.push(rich([
  ['ESG 공시는 외부 평가기관이 등급을 매기는 주요 근거다. 그렇다면 사업보고서에 ESG 표현을 더 많이, 더 구체적으로 적는 기업일수록 등급도 높을 것이라 기대할 수 있는데, 이 기대에는 두 해석이 얽혀 있다. 하나는 실제 ESG 활동이 활발한 기업이 보고서에도 관련 내용을 충실히 담는다는 해석이고, 다른 하나는 규모가 크고 공시 역량이 높은 기업이 어떤 주제든 길고 정교하게 써서 어휘량과 등급이 함께 높아진다는 해석이다. 본 연구는 후자를 ', false],
  ['cheap-talk', true],
  ['이라 부른다. 이는 허위 공시라는 단정이 아니라, 공시 언어의 양과 외부 평가가 강하게 연동되어 실제 성과와 표현 사이에 괴리가 생길 수 있다는 측정상의 경계 개념이다. 공시 텍스트로 ESG를 측정하려는 시도가 이 분량 효과와 실질 신호를 구분하지 못하면 "보고서가 긴 기업이 등급도 높다"는 동어반복에 빠진다.', false]
]));
C.push(body(
  '선행연구는 ‘ESG 등급의 신뢰성’, ‘공시 언어의 greenwashing 측정’, ‘한국어 ESG 텍스트마이닝’ 세 갈래로 좁혀 검토하였다. ' +
  '먼저 등급의 신뢰성은 국내외에서 거듭 지적되어 왔다. 유지선(2025)은 KCGS와 글로벌 평가사 등급의 격차가 정보환경에 따라 ' +
  '달라지고 그 격차가 기업가치와 연결됨을 한국 표본으로 보였고, Kim과 Kim(2023)은 평가사 간 등급 불일치가 클수록 정보비대칭이 ' +
  '커져 기업가치와 연기금 투자에 부정적임을 확인하였다. 평가기관 간 등급 상관이 0.38–0.71에 그친다는 Berg, Kölbel, and ' +
  'Rigobon(2022)의 결과와 함께, 이는 KCGS 단일 등급을 정답처럼 다루기 어렵다는 점을 보여준다. 본 연구가 KCGS 등급과의 관계를 ' +
  '인과가 아닌 연관으로만 해석하는 이유다. 한편 한국어 ESG 보고서를 텍스트마이닝한 Yoon, Han, Lee, and Hwang(2023)은 ' +
  '국내 공시 언어 분석의 가능성을 보였으나 등급과의 연결이나 분량 교란 통제까지는 다루지 않았다.'
));
C.push(rich([
  ['선행연구의 공백은 두 가지다. 첫째, 대부분의 연구가 "공시를 잘하면 등급이 높다"는 ', false],
  ['평균효과', true],
  ['에서 멈추고, 개별 기업이 자신의 등급 대비 얼마나 과(過)·소(少) 공시하는지를 측정해 유형화·처방하는 firm-level 진단 도구는 드물다. 둘째, greenwashing을 다룬 연구들은 ESG를 ', false],
  ['하나의 점수', true],
  ['로 합쳐 보기 때문에, 한 기업이 어떤 축은 부풀리고 다른 축에는 침묵하는 축 간(cross-pillar) 선택을 구조적으로 잡아내지 못한다. 기후 공시의 선택적 공개를 다룬 Bingler 외(2022)도 환경(E) 내부의 선택일 뿐 E·S·G 세 축을 각 축의 등급에 견준 것은 아니다. 실제로 본 연구가 E·S·G를 각 축의 KCGS 등급에 견줘 따로 보면 firm-year의 ', false],
  ['47%가 한 축만 부풀리고 다른 축에는 침묵하는 선택적 공시', true],
  ['였는데(4.4절), 이는 ESG를 하나의 합산 점수로 보던 선행연구의 한 축에서는 드러나지 않는다.', false]
]));
C.push(rich([
  ['본 연구는 이 공백을 겨냥한다. 분석 단위는 회사명이 아니라 stock_code × fiscal_year의 firm-year이며, 세 질문에 답한다. ' +
   '(1) ESG 어휘 강도는 등급과 연관되며 그 연관은 분량 통제 후에도 유지되는가. (2) 분량 착시를 제거하면 개별 기업의 ' +
   '말–실행 정합성은 어떻게 갈리는가. (3) 기업은 ESG를 고르게 말하는가, 아니면 축을 골라 부풀리는가. 기여는 세 가지다. ', false],
  ['분량 교란을 직접 제거한 격차 구성, 그 격차가 수익성이 아니라 규모·구조적 특성과 연결된다는 통념 반증, 그리고 단일 점수가 ' +
   '못 보는 E·S·G 축 간 선택적 공시를 KCGS 축별 등급에 견줘 측정한 점', true],
  ['이다. 이를 통해 현상 확인을 넘어 기업·투자자·평가기관·규제당국 각각에 대한 구체적 제언으로 연결한다.', false]
]));

// ===================== 2. Data =====================
C.push(h1('2. 데이터'));
C.push(body(
  '표본은 KCGS ESG 등급을 보유한 상장기업 127개를 2022·2023·2024 세 회계연도로 확장한 381 firm-year다. ' +
  '한 기업을 한 관측치로 두면 연도별 공시 변화가 사라지므로 firm-year를 단위로 삼되, 한 기업이 세 해 반복 관측되어 ' +
  '완전 독립은 아니라는 점은 한계로 남는다. 결합 키로 회사명 대신 종목코드를 쓴 것은 사명 변경·표기 차이로 인한 오매칭을 막기 위해서다. ' +
  '고유 회사명은 133개였으나 고유 종목코드는 127개였고, 종목코드는 항상 6자리 문자열로 처리해 005930이 5930으로 읽혀 매핑이 ' +
  '실패하는 일을 막았다. 등급은 D=0부터 A+=5까지 순서형으로 부호화하되 간격이 같다는 가정을 두지 않아 순위 기반 통계를 먼저 보았고, ' +
  '공시와 평가 시점은 esg_year = fiscal_year + 1로 정렬해 평가연도 t의 등급을 직전 회계연도 사업보고서와 맞추었다.'
));
C.push(body(
  '수집은 재현성을 위해 회사명 검색 대신 stock_code → corp_code → rcept_no → document.xml 경로를 남겼다. ' +
  '같은 회계연도에 정정공시가 여럿이면 최신 확정본을 택하고 결산월에 의존하지 않는 방식으로 검색해 비12월 결산 기업의 누락을 막았으며, ' +
  '수집 실패 행은 텍스트 부재와 의미가 다르므로 0점으로 채우지 않았다(최종 381건 전부 수집 성공). ' +
  '재무제표 주석·표·안내문이 ESG 어휘 측정을 흐릴 수 있어, ESG 서술이 실제 문장으로 나타나는 II(사업의 내용)·IV(이사의 경영진단)·' +
  'VI(이사회 등 기관) 세 섹션만 추출하였다. 기업별 세부 항목명은 달라도 대분류 구조는 안정적이므로 로마숫자 대분류 제목만 경계로 삼아, ' +
  'TF-IDF를 왜곡하는 표 블록과 파싱 실패 조각(너무 짧은 텍스트)을 제거하기 위해 그 범위로 한정하였다. 그 결과 세 섹션 모두 0자인 firm-year는 없었다.'
));
C.push(rich([
  ['추출 텍스트의 글자 수는 평균 34,773자였으나 최소 4,513자에서 최대 189,606자까지 약 42배의 편차를 보였다. ' +
   '보고서가 길면 어떤 단어든 더 많이 등장하므로, ESG 어휘가 많다는 사실만으로 성과가 좋다고 해석하면 분량 효과를 신호로 착각한다. ' +
   '따라서 이후 모든 분석에서 분량을 로그 변환한 log_n_tokens를 통제하였다. 이 변수는 단순 보조 통제가 아니라 ', false],
  ['cheap-talk 가능성을 정면으로 점검하는 핵심 변수이자, 뒤이을 말–실행 격차의 출발점', true],
  ['이다.', false]
]));
C.push(cap('표 1. 사업보고서 추출 텍스트 글자 수 분포 (381 firm-year)'));
C.push(tbl(
  ['항목', '평균', '중앙값', '최소', '최대', '편차비'],
  [['글자 수', '34,773', '25,872', '4,513', '189,606', '42.0배']],
  [1512, 1512, 1512, 1512, 1512, 1512]
));
C.push(sp(100));

// ===================== 3. Method =====================
C.push(h1('3. 방법'));
C.push(h2('3.1 형태소 분석기와 ESG 어휘 보존'));
C.push(body(
  '한국어는 조사·어미가 결합하고 복합명사가 많아, ‘재생에너지’·‘감사위원회’가 ‘재생+에너지’처럼 쪼개지면 feature가 본래 개념을 잃는다. ' +
  '따라서 분석기 선택 기준은 속도가 아니라 ESG 핵심 어휘 보존율로 두었다. Kiwi는 기본 상태에서 seed 30개 중 18개(60%)를 보존했으나 ' +
  '사용자 사전을 적용하자 28개(93%)로 올랐고, Okt는 20개(67%), BERT subword는 합성어를 잘게 나누어 16개(53%)에 머물렀다. ' +
  '사전 기반 점수에는 합성어 보존이 필수이므로 Kiwi 사용자 사전을 채택하였고, 회사명에서 분해된 ‘에너지’ 같은 ESG 관련어가 ' +
  '불용어 제거 과정에서 사라지지 않도록 seed 30개는 강제로 보호하였다.'
));
C.push(fig('fig1_analyzer_compare.png', 460, 167, '형태소 분석기 seed 보존율 비교'));
C.push(cap('그림 1. 형태소 분석기 seed 보존율 비교. Kiwi 사용자 사전(짙은 막대)이 전 차원에서 ESG seed를 가장 많이 보존한다.'));
C.push(h2('3.2 어휘 강도 측정 — TF-IDF seed·FastText 확장·cosine'));
C.push(body(
  'TF-IDF는 특정 문서에서 자주 나오면서 전체 corpus에서는 흔하지 않은 단어에 높은 값을 준다. 보일러플레이트 제거를 위해 max_df=0.80을 ' +
  '두었는데, 이는 ‘이사회’·‘주주’ 같은 G seed 7개를 어휘에서 제외한다. 이것이 G 신호를 인위적으로 죽인 선택인지 확인하려고 max_df를 ' +
  '1.00까지 높이며 추적한 결과(그림 2), seed_G와 g_grade 상관은 0.80–0.95에서 0.27–0.30으로 안정적이다가 0.99에서 0.108로 급락하고 ' +
  '1.00에서 −0.162로 반전되었다. 모든 문서에 등장하는 의무공시 보편어를 넣을수록 신호가 무너지는 것은, 그 어휘가 변별력이 없을 뿐 아니라 ' +
  '많이 쓰는 것이 높은 등급의 지표가 아니라는 진단이다.'
));
C.push(fig('fig2_maxdf_sweep.png', 410, 228, 'max_df sweep'));
C.push(cap('그림 2. max_df 값에 따른 seed_G ↔ g_grade Spearman ρ 변화. 보편적 의무공시어를 포함할수록 G 신호가 붕괴·반전된다.'));
C.push(body(
  'seed 30개만으로는 기업이 실제 쓰는 다양한 표현을 포착하기 어려워, 외부 사전 대신 분석 corpus에서 FastText를 학습해 확장 사전을 ' +
  '구축하였다. seed와의 cosine 유사도 임계값 θ를 0.55–0.75로 훑어 θ=0.65를 택했는데, 약 493개로 사람이 전수 검토할 수 있으면서 ' +
  '잡음 비율이 1.0% 수준이었기 때문이다. 임베딩이 인명·지명·시사어를 가까운 후보로 끌어오므로 자동 필터 후 사람이 직접 기각하여 ' +
  '최종 433개를 확정하였고, 기각률은 S에서 40.7%로 가장 높아 사회 차원 어휘의 희소성을 다시 확인하였다. 확장 점수는 seed 대비 ' +
  'G에서 보완 효과가 가장 컸다(+2185%). 사전 기반 측정의 타당도는 한국어 문장 임베딩(dense cosine)과 비교해 점검하였다(그림 3).'
));
C.push(fig('fig3_dense_vs_tfidf.png', 410, 214, 'Dense vs TF-IDF 비교'));
C.push(cap('그림 3. 의미 임베딩(dense)과 단어 기반(TF-IDF) cosine의 등급 상관. 세 차원 모두 TF-IDF가 높아(E 0.367 대 0.229 등) 이 설정에서는 단어 기반 측정이 타당함을 확인한다.'));
C.push(h2('3.3 회귀 설계와 말–실행 격차(Talk–Walk Gap)'));
C.push(body(
  '서열형 등급의 성격을 고려해 OLS·Ordered Logit·Binary Logit 세 모형을 병행하였다. 모든 모형에 분량(log_n_tokens)을 넣어 ' +
  '분량 효과를 제거했고(M1), 기업 규모가 분량과 등급을 동시에 끌어올리는 교란일 수 있어 규모·수익성·재무위험을 추가 통제한 모형(M2, n=344)도 ' +
  '추정하였다. 이 회귀는 "분량을 빼도 남는 신호가 있는가"라는 진단까지를 담당한다.'
));
C.push(rich([
  ['알파 분석은 여기서 한 걸음 더 나아가, 한 기업이 자기 등급에 비해 사업보고서에서 ESG를 과하게 말하는지(과잉) 아니면 실력보다 ' +
   '조용한지(과소)를 점수로 만든다. 핵심은 ', false],
  ['격차 = 말 − 실행', true],
  ['이다. 네 가지 결정으로 격차를 구성한다. (1) 분량 착시 제거 — 어휘 강도를 log_n_tokens에 회귀한 잔차(talk_resid)만 사용해 길이로 ' +
   '설명되는 몫을 걷어낸다. (2) 단위 통일 — 말(잔차)과 등급을 각각 z-점수로 표준화한다. (3) 격차 정의 — 아래 수식처럼 표준화한 말에서 ' +
   '표준화한 등급을 빼며, 양수는 과잉(말이 앞섬), 음수는 과소(등급이 앞섬)다. (4) 차원 — E·S·G 각각과 종합을 따로 본다. 이 격차 구성은 ' +
   'greenwashing 연구가 쓰는 ‘공시 − 성과’ 발상과 같되, 본 표본의 최대 교란인 분량을 talk 항에서 직접 제거한다는 점이 다르다.', false]
]));
C.push(center('gap_d = z(talk_resid_d) − z(grade_d),   d ∈ {E, S, G, 종합}', SZ_BODY, { spacing: { before: 40, after: 80 } }));
C.push(note('주: 잔차화 검증에서 talk_resid와 log_n_tokens의 상관은 E·S·G 모두 r≈0.000으로, 길이 효과가 제거되었음을 확인하였다. 이는 설계상 당연한 검증 표시이며 발견이 아니다.'));
C.push(body(
  '유형 간 비교(4.3)에는 평균 기반 분산분석(ANOVA) 대신 순위 기반 비모수 검정인 Kruskal–Wallis 검정을 쓴다. ' +
  '비교 대상인 등급·격차 유형이 순서형이고 네 유형의 분포가 정규성을 가정하기 어려워, 평균보다 순위 합을 비교하는 쪽이 이상치와 ' +
  '비대칭에 견고하기 때문이다. 검정통계량 H가 크고 p가 작을수록 네 유형의 분포 차이가 뚜렷하다는 뜻이다.'
));

// ===================== 4. Results =====================
C.push(h1('4. 결과'));
C.push(body(
  '결과는 네 단계로 압축한다. (1) 분량이 어휘보다 강하게 연관되고, (2) 통제 후 거버넌스만 남으며, (3) 분량을 걷어낸 격차로 보면 ' +
  '기업의 말–실행 정합성이 구조적으로 갈리고, (4) 기업은 ESG를 축을 골라 부풀린다.'
));
C.push(h2('4.1 가장 강한 연관은 ESG 어휘가 아니라 분량이다'));
C.push(body(
  '등급 4종과 feature 10개를 교차한 40개 검정은 FDR 보정 후 모두 유의했으나, 등급과 가장 강하게 연관된 것은 단순 토큰 수였다(ρ=0.663). ' +
  'A 이상 기업의 평균 토큰 수는 7,523으로 B+ 이하의 3,547보다 약 2.1배 많았다. ESG feature는 모두 효과가 약함~중간(최대 ρ=0.451)에 ' +
  '머물러, 공시 언어에서 가장 강한 신호는 내용이 아니라 분량이라는 cheap-talk 경고를 준다.'
));
C.push(cap('표 2. 주요 feature와 ESG 통합등급 간 Spearman ρ (FDR 보정 후 40/40 유의)'));
C.push(tbl(
  ['feature', 'ρ', 'feature', 'ρ'],
  [
    ['n_tokens (분량)', '0.663', 'seed_score_E', '0.306'],
    ['expanded_score_G', '0.425', 'seed_score_G', '0.248'],
    ['expanded_score_E', '0.373', 'expanded_score_S', '0.212'],
  ],
  [2900, 1636, 2900, 1636]
));
C.push(h2('4.2 분량·규모를 통제하면 거버넌스(G)만 독립 신호로 남는다'));
C.push(body(
  '분량을 통제한 회귀(M1)에서 ESG feature 중 expanded_G만 강하게 유의했고(β=3.174), 재무(규모·수익성·재무위험)를 추가 통제한 ' +
  'M2에서도 견고했다(β=1.955, p<0.001). 반면 expanded_E는 재무 통제 후 유의성이 사라져 환경 신호 상당 부분이 기업 규모 교란이었음이 ' +
  '드러났고, expanded_S는 모든 모형에서 비유의였다. 세 모형(OLS·Ordered·Binary)에서 방향이 일치해 결론이 모형 선택에 좌우되지 않았다. ' +
  '분량 자체는 재무 통제 후 절반으로 줄었지만 여전히 강해, cheap-talk이 단순 규모 효과로 환원되지 않음을 보강한다.'
));
C.push(fig('fig4_m1m2_dumbbell.png', 390, 197, 'M1→M2 계수 변화'));
C.push(cap('그림 4. 분량 통제(M1)→재무 통제 추가(M2) 계수 변화. expanded_G(파랑)는 통제 후에도 유의, expanded_E(빨강)는 소멸.'));
C.push(cap('표 3. OLS 회귀(확장 사전) — M2는 분량+재무 통제(n=344). 주: log_assets β=+0.262(p<0.001), R² 0.476→0.551.'));
C.push(tbl(
  ['feature', 'M1 β', 'M2 β', 'M2 p', '판정'],
  [
    ['expanded_G', '+3.174', '+1.955', '<0.001', '★ 견고'],
    ['expanded_E', '+0.432', '+0.172', '0.396', '유의성 소멸(규모 교란)'],
    ['expanded_S', '−0.695', '−0.070', '0.918', '비유의'],
    ['log_n_tokens', '+1.297', '+0.718', '<0.001', '절반↓이나 견고'],
  ],
  [2300, 1450, 1450, 1300, 2572]
));
C.push(body(
  '주목할 점은 살아남은 G 신호가 의무공시 보편어에서 나온 것이 아니라는 사실이다. ‘이사회·주주’처럼 모든 보고서에 등장하는 ' +
  'G seed 7개는 max_df=0.80 단계에서 이미 어휘에서 빠졌고(3.2절), 그 보편어를 도로 넣자 G 상관이 오히려 붕괴·반전했다. ' +
  '즉 거버넌스는 더 많이 쓰는 것이 아니라 변별력 있는 어휘를 쓰는 것이 등급과 맞물리며, 이것이 분량·규모를 통제한 뒤에도 G만 ' +
  '독립 신호로 남은 까닭이다.'
));
C.push(h2('4.3 말–실행 격차로 보면 44%가 어긋나고, 60%는 구조적이다'));
C.push(rich([
  ['분량 착시를 제거한 격차로 기업-연도를 어휘강도(말)×등급(실행) 2×2로 나누면, 정합형 31.2%·과소공시 25.2%·일관저조 24.7%·' +
   '과잉공시 18.9%로 분포한다. ', false],
  ['전체의 44%(168/381), 곧 열 곳 중 네 곳 남짓이 말과 실행이 어긋난다.', true],
  [' 더 중요한 것은 이 격차가 그해의 전술이 아니라는 점이다 — 127개사 중 76개사(59.8%)가 3년 내내 같은 칸에 머물러, ' +
   '말–실행 정합성은 기업에 굳어진 특성에 가깝다. 양극단도 직관과 맞는다. 과잉공시 1위는 3년 연속 D등급인데 ESG 어휘는 ' +
   '최상위인 백광산업이고, 과소공시 쪽은 A+이면서 어휘가 평균 이하인 KB·신한·하나·우리·BNK 등 대형 금융지주였다.', false]
]));
C.push(fig('fig5_talkwalk_map.png', 500, 229, 'Talk-Walk Gap 2x2 유형 지도'));
C.push(cap('그림 5. 말–실행 격차 2×2 유형 지도. 가로축=분량을 걷어낸 어휘강도(말), 세로축=KCGS 등급(실행). 우하 빨강=과잉공시, 좌상 청록=과소공시.'));
C.push(rich([
  ['유형을 가르는 진짜 축은 수익성이 아니라 규모였다. 수익성(roa)은 네 유형 간 차이가 없었으나(H=4.59, p=0.205), ' +
   '규모(log_assets)는 가장 강하게 갈렸다(H=172.0, p<0.001). 즉 ', false],
  ['과잉공시는 ‘부실기업의 변명’이 아니라 ‘소형주의 상징적 공시’, 과소공시는 ‘대형주의 소통 격차(IR gap)’', true],
  ['에 가깝다. 격차가 규모를 단순히 베낀 것은 아닌지 두 단계로 점검하였다. 길이만 잔차화로 걷어낸 1차 격차에, 규모(log_assets)까지 ' +
   '동시에 제거한 2차 격차를 견주자 두 격차의 순위상관은 ρ=0.993, 네 유형 재분류 일치율은 90.9%로 거의 동일했다. 즉 격차는 단순한 ' +
   '규모 대리가 아니라 규모로 환원되지 않는 독립적 정합성 신호다.', false]
]));
C.push(cap('표 4. 유형 간 비교 — 중앙값과 Kruskal-Wallis 검정'));
C.push(tbl(
  ['변수', '과잉', '과소', '정합', '일관저조', '검정'],
  [
    ['수익성 roa', '0.014', '0.019', '0.023', '0.021', 'H=4.59, p=0.205 (차이 없음)'],
    ['규모 log_assets', '27.56', '29.28', '30.12', '26.78', 'H=172.0, p<0.001 (최강)'],
    ['분량 n_tokens', '2,356', '5,721', '4,781', '2,269', 'H=149.4, p<0.001'],
  ],
  [1650, 1150, 1150, 1150, 1300, 2672]
));
C.push(h2('4.4 기업은 ESG를 전체가 아니라 ‘축을 골라’ 부풀린다'));
C.push(rich([
  ['E·S·G 격차를 따로 보면, firm-year의 ', false],
  ['47.2%(180/381)가 한 축은 부풀리고 다른 축에는 침묵하는 선택적 공시', true],
  ['였다(균형 과잉 26.2%·균형 과소 26.5%). 특정 축으로의 일방향 쏠림은 약했으나 거버넌스(G)가 가장 양극화된 축으로, ' +
   '회사마다 가장 적극적으로 내세우거나 가장 크게 침묵하였다. 결정적인 것은 부풀리는 축이 약점이냐 강점이냐가 갈린다는 점이다(표 5).', false]
]));
C.push(fig('fig6_crosspillar.png', 500, 190, '축 간 선택적 공시'));
C.push(cap('그림 6. 축 간 선택적 공시. (왼쪽) 선택적 47% 대 균형 53%. (오른쪽) 각 축이 ‘가장 부풀린 축’·‘가장 침묵한 축’으로 뽑힌 빈도 — G가 양쪽 모두 1위.'));
C.push(cap('표 5. 부풀린 축의 실제 KCGS 등급 (전체 평균과 비교)'));
C.push(tbl(
  ['부풀린 축', '그 축 실제 평균등급', '전체 평균', '해석'],
  [
    ['S (사회)', '2.08', '3.03', '가장 약한 곳을 가장 크게 부풀림 → 약점 은폐(cherry-pick)'],
    ['E (환경)', '2.34', '2.51', '약한 곳을 부풀림(약하게)'],
    ['G (지배구조)', '2.43', '2.31', '실제 강점을 부각 → 정당한 시그널링'],
  ],
  [1600, 2200, 1300, 3972]
));
C.push(rich([
  ['즉 ', false],
  ['‘선택적 공시 = greenwashing’이 아니다.', true],
  [' S·E는 약점을 언어로 가리는 패턴, G는 강점을 알리는 패턴이 공존한다. 단일 ESG 점수로는 결코 보이지 않는 구분이며, ' +
   '축 선택도 구조적이어서 매년 같은 축을 부풀린 기업이 59.1%(75/127)였다.', false]
]));

// ===================== 5. Discussion =====================
C.push(h1('5. 논의 — 시사점과 제언'));
C.push(h2('5.1 ‘양(量) 중심 공시’라는 통념을 데이터로 반박한다'));
C.push(rich([
  ['이 분석에서 가장 분명한 사실은 공시 언어에서 가장 강한 신호가 내용이 아니라 분량이라는 점이다. 그러나 "분량이 지배한다"에서 멈추면 ' +
   'ESG 공시를 보는 눈이 오히려 단순해진다. 분량·규모를 모두 걷어낸 뒤에도 거버넌스 어휘는 등급과 함께 갔고, 기업마다 ' +
   '말–실행 정합성과 축 편향이 구조적으로 달랐기 때문이다. ', false],
  ['핵심 메시지는 "ESG 단어를 많이 쓰면 성과가 좋다"는 통념이 데이터로 지지되지 않는다는 것', true],
  ['이다. 등급과 가장 강하게 연관된 것이 보고서 길이였고, 분량을 통제하면 어휘량의 설명력은 크게 줄었다. 따라서 공시 텍스트를 ' +
   'ESG 의사결정에 쓸 때는 분량과 규모를 보정한 뒤, 무엇이 남는지를 보아야 한다. 이는 평가사 간 등급 불일치의 절반 이상이 측정 방식에서 ' +
   '비롯된다는 Berg 외(2022)의 지적, 그리고 정보환경이 등급 격차를 만든다는 유지선(2025)의 결과와 같은 맥락에 있다.', false]
]));
C.push(h2('5.2 기업에 대한 제언 — 유형별로 처방이 다르다'));
C.push(body(
  '말–실행 격차는 기업을 두 진단군으로 나눈다. 두 군은 문제의 성격이 다르므로 처방도 달라야 한다. 수익성이 유형 간에 차이가 없었다는 ' +
  '점은 두 군 모두 ‘돈을 못 버는 부실기업’의 문제가 아님을 뜻한다.'
));
C.push(rich([
  ['과잉 공시형(소형·저등급, 구조적 11개사): ', true],
  ['등급 대비 말이 앞서면 평가기관·규제당국의 신뢰 할인과 greenwashing 점검 리스크에 노출된다. 수익성은 정상이므로 문제는 역량이 아니라 ' +
   '검증 근거의 부재다. 따라서 서술을 배출량·안전교육 이수율·사외이사 비율 같은 검증 가능한 수치로 뒷받침해야 한다. ' +
   '3년 내내 과잉으로 고착된 11개사가 우선 점검 대상이다.', false]
]));
C.push(rich([
  ['과소 공시형(대형·고등급, 구조적 21개사): ', true],
  ['실력 대비 ESG 언어가 약하다 — 알릴 것을 못 알린 손해이자 저평가 위험이다. 특히 금융지주·CJ·현대건설처럼 보고서가 길어 ESG 어휘가 ' +
   '비율상 묻히는 대형 기업이 여기 많다. 실질 성과를 별도 ESG 섹션이나 요약으로 II·IV·VI에 응집해, 시장과 평가기관이 읽을 수 있는 ' +
   '위치·형식으로 드러내야 한다. 등급 불일치가 정보비대칭과 기업가치 하락으로 이어진다는 Kim·Kim(2023)을 고려하면, 소통 격차의 해소는 ' +
   '단순 홍보가 아니라 자본비용과 직결되는 과제다.', false]
]));
C.push(rich([
  ['축 편향 관점의 제언: ', true],
  ['특히 사회(S)축을 부풀리는 기업은 실제 S등급이 가장 낮았다(2.08 대 전체 3.03). 이 약점은 언어가 아니라 실질 개선으로 메워야 하며, ' +
   '말로 가릴수록 검증 시 역풍이 크다. 반대로 거버넌스(G) 부각은 대체로 실제 강점에 근거하므로 정당하나, 과장은 경계해야 한다.', false]
]));
C.push(h2('5.3 투자자·평가기관·규제당국에 대한 제언'));
C.push(rich([
  ['투자자: ', true],
  ['공시의 ESG 어휘량을 액면 그대로 믿으면 분량·규모 착시에 노출된다. 합산 점수만 보면 축 편향을 놓치므로, 비슷한 규모끼리 비교하고 ' +
   '축별(E/S/G)로 말–실행 정합성을 따로 점검해야 한다. 분량·규모를 통제해도 살아남은 거버넌스 어휘는 외부 평가를 보완하는 독립 정보가 될 수 있다.', false]
]));
C.push(rich([
  ['평가기관: ', true],
  ['합산 등급은 차원 간 차이를 감춘다. 분량·규모를 통제한 차원별 신뢰도를 공개하고, 평가 인풋에서 ‘더 많이 쓴 공시’가 자동으로 ' +
   '보상되지 않도록 검증 가능성에 가중하는 것이 바람직하다. KCGS가 사업보고서를 평가에 참고한다는 점은, 공시 언어와 등급의 연관이 ' +
   '동어반복일 수 있다는 경고이자 공시 품질 개선이 등급 신뢰도와 직결된다는 뜻이기도 하다.', false]
]));
C.push(rich([
  ['규제당국: ', true],
  ['‘더 많은 공시’를 요구하면 길이와 불일치가 함께 늘 수 있다. 분량이 아니라 검증 가능성·정합성에 기반한 공시, 그리고 거버넌스처럼 ' +
   '기계가독·외부대조가 가능한 정보의 섹션 표준화가 더 유효하다. 다만 본 표본은 수업용 pilot이므로, 이 제언은 단정이 아니라 ' +
   '검토 권고 수준으로 읽어야 한다.', false]
]));
C.push(h2('5.4 학술적 기여'));
C.push(body(
  '본 연구의 기여는 greenwashing 개념의 최초성이 아니라 세 가지의 결합에 있다. 첫째, 표본의 최대 교란인 분량을 talk 항에서 직접 제거해 ' +
  '격차를 구성함으로써, ‘보고서가 길어 생긴 연관’과 ‘정합성의 격차’를 분리하였다. 둘째, 그 격차가 수익성이 아니라 규모·구조적 특성과 ' +
  '연결되며 규모를 통제해도 유지된다는 통념 반증을 한국 표본에서 제시하였다. 셋째, ESG를 단일 점수로 합치는 기존 측정이 못 보는 ' +
  'E·S·G 축 간 선택적 공시를 각 축의 KCGS 등급에 견줘 측정하여, 약점 은폐(S)와 정당한 시그널링(G)을 구분하였다. ' +
  '이는 평균효과에 머문 선행연구와 firm-level 진단의 공백을 겨냥한 것이다.'
));
C.push(h2('5.5 한계'));
C.push(body(
  '해석에는 분명한 제약이 있다. 첫째, 표본 381 firm-year는 수업용 pilot으로 무작위 추출이 아니어서 한국 상장기업 전반으로 일반화할 수 없다. ' +
  '둘째, 측정한 것은 ESG 성과가 아니라 언어이며, 명사 위주 bag-of-words 방식이라 ‘배출 증가’와 ‘배출 감축’을 구분하지 못한다. ' +
  '셋째, 모든 결과는 연관이며 인과가 아니다. KCGS가 사업보고서를 평가에 참고하므로 동어반복·역인과 위험이 있어, 격차와 축 편향은 ' +
  'greenwashing의 증명이 아니라 더 들여다볼 진단 신호로만 읽어야 한다. 넷째, KCGS 단일 등급에 의존했고 등급 자체가 평가사 간 ' +
  '분산이 크며(Berg 외, 2022; 유지선, 2025), 3개 연도뿐이라 지속성 판단의 검정력이 약하고, 같은 기업 반복 관측을 pooled로 추정해 ' +
  'p-value가 낙관적일 수 있다. seed·θ·max_df 등 연구자 재량도 결과를 조건부로 만든다. 후속 과제로 더 큰 무작위 표본, 기업 고정효과·' +
  '군집 표준오차, 실제 성과(배출량·사고·제재) 연결, 복수 평가사 결합, 지속가능경영보고서 확대를 남긴다.'
));

// ===================== 6. Conclusion =====================
C.push(h1('6. 결론'));
C.push(rich([
  ['사업보고서 ESG 어휘 강도와 KCGS 등급 사이에는 통계적 연관이 있으나, 가장 강한 요인은 ESG 어휘가 아니라 공시 분량이었다. ' +
   '분량과 규모를 통제하면 거버넌스(G) 어휘만 독립 신호로 남았고, 분량 착시를 제거한 말–실행 격차로 보면 전체의 44%가 어긋났으며 ' +
   '그 60%가 구조적이었다. 격차를 가르는 축은 수익성이 아니라 규모였고, 규모를 통제해도 격차는 유지되었다. 나아가 기업들은 ESG를 ' +
   '고르게가 아니라 축을 골라 말했는데, 약한 사회(S)는 언어로 가리고 강한 거버넌스(G)는 정당하게 부각하였다. ', false],
  ['요컨대 ESG 공시 어휘는 등급과 연관되지만 상당 부분이 ‘분량’ 착시이며, 이를 걷어내면 거버넌스 어휘만이 견고한 신호로 남고, ' +
   '기업마다 규모로 환원되지 않는 구조적 정합성·편향이 존재한다.', true],
  [' 따라서 보고서가 길고 그럴듯하다는 이유로 ESG 성과가 높다고 단정해서는 안 되며, 평가·투자·공시 의사결정은 분량과 규모를 보정하고 ' +
   '축별로 말과 실행의 정합성을 따로 점검해야 한다.', false]
]));

// ===================== References =====================
C.push(h1('참고문헌'));
[
  '유지선. (2025). ESG 평가등급 격차의 결정요인과 기업가치와의 관계. 국제회계연구, 119, 1–19.',
  'Kim, J., & Kim, H. (2023). The impact of ESG rating disagreement on corporate value. Journal of Derivatives and Quantitative Studies(선물연구), 31(3), 219–241. https://doi.org/10.1108/JDQS-01-2023-0001',
  'Yoon, B., Han, S., Lee, J., & Hwang, S. (2023). Text mining analysis of ESG management reports in South Korea: Comparison with SDGs. SAGE Open, 13(4), 1–18. https://doi.org/10.1177/21582440231202896',
  'Berg, F., Kölbel, J. F., & Rigobon, R. (2022). Aggregate confusion: The divergence of ESG ratings. Review of Finance, 26(6), 1315–1344. https://doi.org/10.1093/rof/rfac033',
  'Bingler, J. A., Kraus, M., Leippold, M., & Webersinke, N. (2022). Cheap talk and cherry-picking: What ClimateBERT has to say on corporate climate risk disclosures. Finance Research Letters, 47, 102776. https://doi.org/10.1016/j.frl.2022.102776',
  'Khan, M., Serafeim, G., & Yoon, A. (2016). Corporate sustainability: First evidence on materiality. The Accounting Review, 91(6), 1697–1724. https://doi.org/10.2308/accr-51383',
  'Li, K., Mai, F., Shen, R., & Yan, X. (2021). Measuring corporate culture using machine learning. The Review of Financial Studies, 34(7), 3265–3315. https://doi.org/10.1093/rfs/hhaa079',
  'Loughran, T., & McDonald, B. (2011). When is a liability not a liability? Textual analysis, dictionaries, and 10-Ks. The Journal of Finance, 66(1), 35–65. https://doi.org/10.1111/j.1540-6261.2010.01625.x',
  'Schimanski, T., Reding, A., Reding, N., Bingler, J., Kraus, M., & Leippold, M. (2024). Bridging the gap in ESG measurement: Using NLP to quantify environmental, social and governance communication. Finance Research Letters, 61, 104979. https://doi.org/10.1016/j.frl.2024.104979',
  '금융감독원. (n.d.). OpenDART API 개발가이드. 전자공시시스템. https://opendart.fss.or.kr',
  '한국ESG기준원. (n.d.). ESG 평가 등급 안내. https://www.cgs.or.kr',
  'Park, B. (2024). Kiwipiepy: A morphological analyzer for Korean. https://github.com/bab2min/Kiwi',
  'Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825–2830.',
  'Řehůřek, R., & Sojka, P. (2010). Software framework for topic modelling with large corpora. In Proceedings of the LREC 2010 Workshop on New Challenges for NLP Frameworks (pp. 45–50).',
].forEach(ref => C.push(new Paragraph({
  alignment: AlignmentType.LEFT,
  indent: { left: 360, hanging: 360 },
  spacing: { before: 0, after: 90, line: LS_BODY, lineRule: 'auto' },
  children: [new TextRun({ text: ref, font: FONT, size: SZ_REF })]
})));

// ===================== BUILD =====================
const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1417, right: 1417, bottom: 1417, left: 1417 },
      }
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18 })]
        })]
      })
    },
    children: C,
  }]
});

Packer.toBuffer(doc).then(buf => {
  const out = path.join(__dirname, '보고서_v8_제출본.docx');
  fs.writeFileSync(out, buf);
  console.log('완료:', out, '(' + buf.length + ' bytes)');
}).catch(e => console.error('오류:', e));
