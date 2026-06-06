const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
  Footer, AlignmentType, BorderStyle, WidthType, ShadingType, PageNumber, PageBreak
} = require('docx');
const fs = require('fs');
const path = require('path');

const FONT = '맑은 고딕';
const CONTENT_WIDTH = 9072;
const SZ_BODY = 21; const SZ_ABSTRACT = 20; const SZ_TITLE = 30;
const SZ_H1 = 26; const SZ_H2 = 22; const SZ_CAPTION = 19;
const SZ_REF = 20; const SZ_AUTHOR = 21; const SZ_COURSE = 19;
const LS_BODY = 384; const LS_ABSTRACT = 360;
const SP_AFTER = 120;
const ASSETS = path.join(__dirname, 'assets');

function body(text, opts = {}) {
  return new Paragraph({
    alignment: AlignmentType.BOTH,
    spacing: { before: 0, after: SP_AFTER, line: LS_BODY, lineRule: 'auto' },
    ...opts,
    children: [new TextRun({ text, font: FONT, size: SZ_BODY })]
  });
}
function h1(text) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 300, after: SP_AFTER, line: LS_BODY, lineRule: 'auto' },
    children: [new TextRun({ text, font: FONT, size: SZ_H1, bold: true })]
  });
}
function h2(text) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 200, after: SP_AFTER, line: LS_BODY, lineRule: 'auto' },
    children: [new TextRun({ text, font: FONT, size: SZ_H2, bold: true })]
  });
}
function cap(text) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 60, after: 80, line: 300, lineRule: 'auto' },
    children: [new TextRun({ text, font: FONT, size: SZ_CAPTION, italics: true })]
  });
}
function fig(filename, w, h, alt) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 100, after: 0 },
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
    alignment: AlignmentType.BOTH,
    spacing: { before: 0, after: 80, line: LS_ABSTRACT, lineRule: 'auto' },
    indent: { left: 280, right: 280 },
    children: [new TextRun({ text, font: FONT, size: SZ_ABSTRACT })]
  });
}

const TB = { style: BorderStyle.SINGLE, size: 4, color: 'AAAAAA' };
const BORD = { top: TB, bottom: TB, left: TB, right: TB };
function tc(text, { bold = false, hdr = false, w, shade } = {}) {
  return new TableCell({
    borders: BORD,
    width: w ? { size: w, type: WidthType.DXA } : undefined,
    shading: shade ? { fill: shade, type: ShadingType.CLEAR } : undefined,
    margins: { top: 70, bottom: 70, left: 110, right: 110 },
    children: [new Paragraph({
      alignment: AlignmentType.LEFT,
      children: [new TextRun({ text, font: FONT, size: 18, bold: bold || hdr })]
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
          w: colW[ci],
          shade: ri % 2 === 1 ? 'F3F6FB' : 'FFFFFF'
        }))
      }))
    ]
  });
}
function note(text) {
  return new Paragraph({
    spacing: { before: 40, after: 100 },
    children: [new TextRun({ text, font: FONT, size: 16, italics: true })]
  });
}
function center(text, sz, opts = {}) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 80, line: 320, lineRule: 'auto', ...opts.spacing },
    children: [new TextRun({ text, font: FONT, size: sz, bold: !!opts.bold })]
  });
}

// ===================== CONTENT =====================
const C = [];

// --- TITLE PAGE ---
C.push(center('한국 상장기업 사업보고서의 ESG 어휘 강도는', SZ_TITLE, { bold: true, spacing: { before: 560, after: 0, line: 380 } }));
C.push(center('KCGS 등급을 설명하는가:', SZ_TITLE, { bold: true, spacing: { before: 0, after: 60, line: 380 } }));
C.push(center('공시 장황성 통제와 지배구조 신호의 섹션 국소화', SZ_TITLE, { bold: true, spacing: { before: 0, after: 300, line: 380 } }));
C.push(center('김혜성, 이동원, 김지우, 신지영', SZ_AUTHOR, { spacing: { before: 0, after: 60 } }));
C.push(center('비정형 데이터 처리 Final Term Project | 3조', SZ_COURSE, { spacing: { before: 0, after: 320 } }));
C.push(center('초록', SZ_H2, { bold: true, spacing: { before: 0, after: 100 } }));
C.push(absPara(
  '상장기업이 사업보고서에 적는 ESG 관련 표현과 한국ESG기준원(KCGS)의 외부 ESG 등급 사이에 어떤 통계적 연관이 있는지 분석하였다. ' +
  '127개 상장기업의 2022–2024 회계연도 사업보고서 381 firm-year에서 환경(E)·사회(S)·지배구조(G) 어휘 강도를 ' +
  'TF-IDF seed 사전, FastText 확장 사전, 기준 문장 cosine으로 측정하고, OLS·Ordered Logit·Binary Logit 세 모형으로 ' +
  '공시 분량을 통제한 뒤 등급과의 관계를 확인하였다. 가장 강한 연관은 ESG 어휘가 아니라 단순 토큰 수에서 나타났다(Spearman ρ=0.663). ' +
  'A 이상 등급 기업의 사업보고서는 B+ 이하 기업보다 평균 2.1배 길었으며, 이는 공시 분량이 외부 평가와 함께 움직이는 cheap-talk 가능성을 시사한다. ' +
  '다만 분량과 기업 규모를 함께 통제한 뒤에도 G 확장 어휘는 독립적인 신호를 유지하였고(β=1.955, p<0.001), ' +
  'E는 규모를 통제하면 사라졌으며 S는 모든 모형에서 유의하지 않았다. ' +
  '분량을 통제하고 남은 G 신호는 이사회 등 기관을 다루는 VI 섹션에 모여 있었으며, ' +
  '그 섹션에서 측정할 때 등급과의 상관이 전체 문서 기준 0.426에서 0.526으로 더 선명해졌다. ' +
  '이 패턴은 사전에 의존하지 않는 의미 임베딩 분류에서도 동일하게 재현되었다(VI 문장의 97.9%가 G로 분류). ' +
  '모든 결과는 연관 관찰이며 인과로 해석하지 않는다.'
));
C.push(new Paragraph({ children: [new PageBreak()] }));

// --- 1. Introduction ---
C.push(h1('1. Introduction'));
C.push(h2('1.1 연구 배경과 문제의식'));
C.push(body(
  '기업의 ESG 공시는 외부 평가기관이 등급을 매기는 주요 근거 자료다. 그렇다면 사업보고서에 ESG 관련 표현을 더 많이, ' +
  '더 구체적으로 적는 기업일수록 외부 등급도 높을 것이라는 기대가 자연스럽게 생긴다. 그러나 이 기대에는 두 가지 상반된 해석이 얽혀 있다. ' +
  '하나는 실제 ESG 활동이 활발한 기업이 보고서에도 관련 내용을 충실히 담는다는 해석이고, 다른 하나는 규모가 크고 공시 역량이 높은 기업이 ' +
  '어떤 주제든 길고 정교하게 서술하기 때문에 ESG 어휘량과 등급이 동시에 높게 나타난다는 해석이다.'
));
C.push(body(
  '본 연구는 후자의 가능성을 cheap-talk이라 부른다. 여기서 cheap-talk은 허위 공시라는 도덕적 단정이 아니라, ' +
  '공시 언어의 양과 외부 평가가 강하게 연동되어 실제 성과와 표현 사이에 괴리가 생길 수 있다는 측정상의 경계 개념이다. ' +
  '사업보고서 텍스트로 ESG를 측정하려는 모든 시도는 이 cheap-talk과 실질 신호를 구분하지 못하면 ' +
  '"보고서가 긴 기업이 등급도 높다"는 동어반복에 빠질 위험이 있다. ' +
  '따라서 본 연구의 일관된 문제의식은 단순하다. 공시 언어와 등급의 연관에서 분량 효과를 걷어낸 뒤에도 남는 ESG 신호가 있는가, ' +
  '있다면 그것은 어떤 차원의, 보고서 어느 부분의 신호인가.'
));
C.push(h2('1.2 선행연구'));
C.push(body(
  'ESG 등급 자체의 신뢰성 문제는 이미 폭넓게 지적되어 왔다. Berg, Koelbel, and Rigobon(2022)은 주요 6개 평가기관의 ESG 등급 사이 상관이 ' +
  '0.38–0.71에 그쳐 신용등급의 0.99와 크게 대비된다는 점을 보이고, 이 불일치의 절반 이상이 측정 방법의 차이에서 비롯된다고 분석하였다. ' +
  '이는 단일 평가기관 등급을 정답처럼 다루기 어렵다는 점, 그리고 텍스트 기반 측정치가 기존 등급을 그대로 재현하기보다 ' +
  '부분적으로만 겹치는 독립 정보일 수 있다는 점을 시사한다. 본 연구가 KCGS 단일 등급과의 관계를 인과가 아닌 연관으로만 해석하고, ' +
  '결과를 다른 평가기관으로 일반화하지 않는 이유가 여기에 있다.'
));
C.push(body(
  '금융 공시 텍스트의 어휘 측정에 관해서는 Loughran and McDonald(2011)의 연구가 직접적인 출발점이 된다. ' +
  '이들은 범용 감성 사전을 10-K 공시에 적용하면 상당수 단어가 도메인 맥락과 어긋나게 분류된다는 점을 보이고, ' +
  '금융 공시에 특화된 사전을 별도로 구축해야 한다고 주장하였다. 이 통찰은 범용 임베딩이나 외부 사전을 그대로 쓰지 않고, ' +
  '분석 대상 corpus 자체에서 학습한 단어 임베딩으로 ESG 확장 사전을 만든 본 연구의 방법론적 선택과 맞닿아 있다.'
));
C.push(h2('1.3 연구 질문과 기여'));
C.push(body(
  '분석 단위는 회사명이 아니라 stock_code × fiscal_year firm-year이며, 두 가지 질문에 답한다. ' +
  '첫째, 사업보고서의 ESG 어휘 강도는 KCGS 등급과 통계적으로 연관되는가, 그리고 그 연관은 공시 분량을 통제한 뒤에도 유지되는가. ' +
  '둘째, 분량을 통제하고 남은 ESG 신호는 보고서의 어느 섹션에 집중되어 있는가.'
));
C.push(body(
  '본 연구의 기여는 두 가지다. 먼저 공시 분량 효과를 명시적으로 분리하여, ESG 세 차원의 신호가 분량·규모 통제에 대해 ' +
  '서로 다르게 반응한다는 점(G는 견고, E는 규모 교란, S는 비유의)을 보였다. 다음으로 섹션 수준 분석을 통해, ' +
  '지배구조 신호가 이사회 공시 섹션에 국소화되며 그곳에서 측정할 때 등급과의 연관이 더 선명해진다는 점을 정량화하고, ' +
  '이를 사전 기반 측정과 의미 임베딩 분류 양쪽에서 교차검증하였다.'
));

// --- 2. Data ---
C.push(h1('2. Data'));
C.push(h2('2.1 표본과 분석 단위'));
C.push(body(
  '표본은 KCGS ESG 등급을 보유한 상장기업 127개를 2022·2023·2024 세 회계연도로 확장한 381 firm-year다. ' +
  '한 기업을 하나의 관측치로 두면 연도별 공시 변화가 사라지므로, 같은 기업이라도 연도마다 다른 보고서와 등급을 갖도록 firm-year를 기본 단위로 삼았다. ' +
  '다만 한 기업이 세 해 반복 관측되는 구조이므로 381개 관측치가 완전히 독립이라고 보기는 어렵고, ' +
  '더 긴 기간으로 확장한다면 기업 고정효과나 군집 강건표준오차를 더하는 것이 자연스럽다.'
));
C.push(body(
  '결합 키로 회사명을 쓰지 않은 이유는 사명 변경·지주회사 전환·표기 차이 때문에 회사명 기준 병합에서 드러나지 않는 오매칭이 발생할 수 있기 때문이다. ' +
  '실제로 고유 회사명은 133개였으나 고유 종목코드는 127개로, 이름만으로 합치면 서로 다른 기업이 섞일 여지가 있었다. ' +
  '종목코드는 항상 6자리 문자열로 처리하였는데, 005930이 수치형으로 읽혀 5930이 되면 앞자리 0이 사라져 OpenDART 매핑이 실패하기 때문이다. ' +
  '작은 전처리처럼 보이지만 이 단계를 건너뛰면 조용한 매핑 실패가 누적되므로, 결합 직전에 모든 종목코드가 6자리인지 강제로 점검하였다.'
));
C.push(body(
  '등급은 D=0, C=1, B=2, B+=3, A=4, A+=5의 순서형 변수로 변환하였다. 표본의 최고 등급이 A+였으므로 6단계로 부호화하였다. ' +
  '이 변환은 등급 간 간격이 같다는 뜻이 아니라 순서 정보를 모형에 넣기 위한 실용적 부호화이며, ' +
  '그래서 분석에서는 Pearson보다 순위 기반 통계를 먼저 보고 회귀도 등간성을 가정하는 모형 하나에만 의존하지 않았다. ' +
  '공시 시점과 평가 시점의 정렬은 esg_year = fiscal_year + 1 규칙을 따랐다. ' +
  '평가연도 t의 등급을 직전 회계연도 t−1의 사업보고서 언어와 맞추기 위한 것으로, 미래 정보를 끌어다 예측하는 설계가 아니라 직전 공시와 다음 평가의 서술적 정렬이다.'
));
C.push(h2('2.2 수집 절차와 출처 추적'));
C.push(body(
  '사업보고서 수집에서 가장 중요한 요건은 분석에 쓴 문서를 나중에 동일하게 다시 찾을 수 있어야 한다는 점이다. ' +
  '이를 위해 회사명 검색 대신 stock_code → corp_code → rcept_no → document.xml 경로를 남겼다. ' +
  '세 식별자의 역할은 서로 다르다. stock_code는 등급·분석 패널과 결합하는 종목 식별자, corp_code는 공시 목록을 조회하는 내부 회사 코드, ' +
  'rcept_no는 특정 보고서를 가리키는 접수번호다. 전체 상장기업의 종목코드–회사코드 매핑(corpCode.xml)을 한 번 내려받아 연결하면, ' +
  '회사명 표기 차이에 흔들리지 않고 API 호출도 줄일 수 있다.'
));
C.push(body(
  '보고서 탐색에는 몇 가지 규칙을 두었다. 보고서명에 "사업보고서"를 포함하되 "반기"·"분기"·"연장"·"신고서"는 제외하였는데, ' +
  '분석 질문이 회계연도 단위 사업보고서와 다음 평가연도 등급의 관계이기 때문이다. 문서 종류가 섞이면 ESG 표현 차이인지 ' +
  '문서 길이·성격 차이인지 구분할 수 없게 된다. 같은 회계연도에 정정공시가 여러 건이면 원본보다 기재정정·첨부정정을 우선하고 ' +
  '동순위에서는 접수일이 늦은 것을 택해, 가장 확정본에 가까운 문서를 사용하였다. 또한 결산월을 12월로 고정해 탐색하면 ' +
  '비12월 결산 기업이 누락되어 표본이 줄기 때문에, 결산월에 의존하지 않는 방식으로 검색하였다.'
));
C.push(body(
  '원문 ZIP 안에는 본 보고서 외에 첨부 XML이 함께 들어갈 수 있어, 접수번호와 같은 이름의 XML을 1순위로, 언더스코어가 없는 XML을 2순위로, ' +
  '그래도 모호하면 가장 큰 XML을 선택하였다. 아무 XML이나 읽으면 첨부자료를 본문으로 오인할 수 있기 때문이다. ' +
  '수집에 실패한 행은 0점으로 채우지 않았다. 텍스트가 없는 것과 수집에 실패한 것은 의미가 전혀 다르며, ' +
  '실패를 0으로 넣으면 낮은 점수가 기술적 실패 때문인지 실제 공시 부재 때문인지 구분할 수 없게 되기 때문이다. ' +
  '다만 최종 실행에서는 381건 전부 수집에 성공하여(381/381), 실제로 가짜 0을 넣거나 행을 버리는 상황은 발생하지 않았다.'
));
C.push(h2('2.3 섹션 추출'));
C.push(body(
  '사업보고서 전체가 아니라 II(사업의 내용)·IV(이사의 경영진단 및 분석의견)·VI(이사회 등 회사의 기관에 관한 사항) 세 섹션을 추출하였다. ' +
  '재무제표 주석이나 반복 안내문, 표 중심 영역이 ESG 언어 측정을 흐릴 수 있어 ESG 서술이 실제 문장으로 나타나는 구간만 남기려는 선택이었다. ' +
  '세 섹션의 역할은 분명히 다르다. II는 사업 현황과 함께 환경 대응·안전·공급망을 서술해 E와 S 표현이 가장 많이 나타나는 본문이고, ' +
  'IV는 경영진이 성과·위험·방향성을 자발적으로 설명하는 구간이라 의무공시 밖의 ESG 서술이 드러날 수 있으며, ' +
  'VI는 이사회·감사위원회·내부통제를 다루어 G 관련 공시의 핵심이다.'
));
C.push(body(
  '추출 과정에서는 신뢰할 수 있는 텍스트만 남기기 위해 세 가지 처리를 하였다. 첫째, 기업별 세부 항목명은 달라도 대분류 구조는 비교적 안정적이기 때문에 ' +
  '대분류 로마숫자 제목만 섹션 경계로 삼았다. 둘째, 숫자와 항목명이 반복되어 형태소 분석과 TF-IDF 점수를 왜곡할 수 있으므로 표 블록을 제거하였다. ' +
  '셋째, 파싱이 실패했거나 제목만 남은 조각을 본문으로 오인하지 않기 위해 너무 짧은 텍스트는 제외하였다. ' +
  '이 처리를 거친 뒤 II·IV·VI 전 섹션에서 0자인 firm-year는 한 건도 없어, 모든 관측치가 최소한의 분석 가능한 텍스트 기반을 확보하였음을 확인하였다.'
));
C.push(h2('2.4 공시 분량 분포와 cheap-talk 문제'));
C.push(body(
  '추출된 텍스트의 글자 수는 평균 34,773자, 중앙값 25,872자였으나 최소 4,513자에서 최대 189,606자까지 약 42배의 편차를 보였다. ' +
  '이 큰 편차가 본 연구의 핵심 문제를 미리 드러낸다. 보고서가 길면 어떤 단어든 더 많이 등장할 가능성이 높으므로, ' +
  'ESG 어휘가 많다는 사실만으로 ESG 성과가 좋다고 해석하면 분량 효과를 ESG 신호로 착각하게 된다. ' +
  '따라서 이후의 모든 주요 회귀에는 분량을 로그로 변환한 log_n_tokens를 통제변수로 포함하였다. ' +
  '이 변수는 단순한 보조 통제가 아니라 cheap-talk 가능성을 정면으로 점검하는 핵심 변수다.'
));
C.push(cap('표 1. 사업보고서 추출 텍스트 글자 수 분포 (381 firm-year)'));
C.push(tbl(['항목', '값'], [['평균', '34,773자'],['중앙값', '25,872자'],['최소', '4,513자'],['최대', '189,606자'],['편차비', '42.0배']], [4536, 4536]));
C.push(sp(120));

// --- 3. Method ---
C.push(h1('3. Method'));
C.push(h2('3.1 형태소 분석기 선택'));
C.push(body(
  '한국어 사업보고서는 조사·어미가 결합하고 복합명사가 많아 공백 기준 토큰화만으로는 ESG 개념을 안정적으로 세기 어렵다. ' +
  '가령 "감사위원회는"을 그대로 두면 "감사위원회" 기준어와 매칭되지 않고, "재생에너지"·"탄소중립"·"중대재해" 같은 복합명사가 ' +
  '"재생+에너지"처럼 쪼개지면 TF-IDF feature가 본래 의도한 개념을 잃는다. ' +
  '따라서 분석기 선택 기준은 처리 속도가 아니라 ESG 핵심 어휘의 보존율과 복합명사 처리 능력이었다.'
));
C.push(body(
  '이 기준으로 Kiwi와 Okt를 동일한 corpus 샘플에서 비교하였다. Kiwi는 기본 상태에서 seed 30개 중 18개(60%)를 보존했으나, ' +
  'seed를 고유명사로 등록하고 인식 우선순위를 높인 사용자 사전(score=50)을 적용하자 28개(93%)로 올라갔다. ' +
  'Okt는 20개(67%)에 그쳤고, 특히 "감사위원회"·"중대재해"를 분리하는 문제가 컸다. ' +
  '추가로 BERT 계열 subword 토크나이저(klue/bert-base)와도 비교했는데, subword는 "넷제로"를 "넷+##제+##로"처럼 의미 조각으로 잘게 나누어 ' +
  'ESG 합성어 보존율이 16/30(53%)에 머물렀다. 사전 기반 점수 계산에서는 합성어가 한 단어로 유지되어야 하므로 Kiwi 사용자 사전을 최종 채택하였다.'
));
C.push(fig('fig1_analyzer_compare.png', 545, 199, '형태소 분석기 seed 보존율 비교'));
C.push(cap('그림 1. 형태소 분석기 seed 보존율 비교. Kiwi 사용자 사전(짙은 막대)이 Kiwi 기본·HF subword보다 전 차원에서 ESG seed를 더 많이 보존하며, 특히 S·G 차원에서 격차가 크다.'));
C.push(body(
  'Komoran과 Kkma는 본선 비교에서 제외하였다. 이는 두 분석기가 이론적으로 부적절해서가 아니라, 381건을 반복 처리하는 본 작업에서 ' +
  'Kkma는 처리 시간이 지나치게 길고 Komoran은 파일 기반 사용자 사전 관리가 반복 실험 흐름에 맞지 않아 효율이 떨어졌기 때문이다. ' +
  '토큰화 단위는 일반명사·고유명사 2자 이상으로 제한하였는데, ESG seed가 모두 명사이고 1글자 명사는 "이"·"수"·"등" 같은 노이즈가 많기 때문이다.'
));
C.push(body(
  '불용어는 조사·일반 경영어·회사명 분해 토큰·공시 정형어를 줄이기 위해 구축하되, seed 30개는 불용어에서 강제로 제외해 보호하였다. ' +
  '예컨대 "에너지"는 한화에너지·SK에너지 같은 회사명이 분해되며 불용어 후보로 들어올 수 있는데, 이를 무조건 제거하면 E 차원의 핵심 신호가 사라진다. ' +
  '일반 잡음은 줄이되 ESG 신호는 지키는 방향으로 전처리를 설계한 것이다. 검증 결과 seed와 ESG 관련어가 불용어에 잘못 섞인 사례는 없었다.'
));
C.push(h2('3.2 TF-IDF와 seed score'));
C.push(body(
  'TF-IDF는 어떤 단어가 특정 문서에서 자주 나오면서도 전체 corpus에서는 너무 흔하지 않을 때 높은 값을 주는 방식이다. ' +
  '모든 보고서에 등장하는 "이사회" 같은 단어는 중요해 보여도 기업을 구분하지 못하지만, ' +
  '특정 firm-year에서 "온실가스 감축"이 유독 두드러지면 그 기업의 E 신호로 읽을 수 있다. ' +
  '파라미터는 세 가지를 두었고 각각 이유가 다르다. min_df=5는 1–4회만 등장하는 희귀어 노이즈를 제거하면서 희소 seed 일부는 보존하기 위함이고, ' +
  'max_df=0.80은 거의 모든 보고서에 나오는 보일러플레이트를 걷어내기 위함이며, sublinear_tf=True는 ' +
  '한 단어가 반복 등장할 때 점수가 과대 반응하지 않도록 빈도에 로그를 적용한다.'
));
C.push(body(
  'max_df=0.80은 "이사회"·"사외이사"·"주주" 같은 G seed 7개를 어휘에서 제외시킨다. ' +
  '이것이 G 신호를 인위적으로 죽인 자의적 선택이라는 의심이 가능하므로, max_df를 0.80에서 1.00까지 높이며 ' +
  'seed_G와 g_grade의 상관이 어떻게 변하는지 직접 추적하였다.'
));
C.push(fig('fig2_maxdf_sweep.png', 520, 289, 'max_df sweep'));
C.push(cap('그림 2. max_df 값에 따른 seed_G ↔ g_grade Spearman ρ 변화. max_df=0.80–0.95에서 ρ는 0.271–0.304로 안정적이지만, 0.99에서 0.108로 급락하고 1.00에서는 −0.162로 부호가 반전된다.'));
C.push(body(
  '결과는 자의성 의심을 반증한다. 보편적 의무공시 어휘를 포함시킬수록 신호가 무너지고, 1.00에서는 오히려 음의 상관으로 뒤집힌다. ' +
  '"이사회"·"주주" 같은 단어는 변별력이 없을 뿐 아니라 반복적으로 많이 쓰는 것이 높은 등급의 지표가 아니라는 뜻이다. ' +
  '즉 max_df=0.80은 G 신호 보존에 필요한 견고한 선택이며, seed_G가 약하게 측정되는 것은 파라미터의 부작용이 아니라 ' +
  '의무공시 어휘 자체의 한계를 드러낸 진단이다. 차원별 seed score를 보면 E는 10/10, S는 10/10이 어휘에 포함되었으나 ' +
  'G는 3/10에 그쳤고, 이 결과가 확장 사전을 도입한 직접적인 이유가 되었다.'
));
C.push(h2('3.3 FastText 기반 확장 사전'));
C.push(body(
  'seed 30개만으로는 기업이 실제 쓰는 다양한 ESG 표현을 포착하기 어렵다. 기업은 "온실가스" 대신 "배출량"·"감축"을, ' +
  '"감사위원회" 대신 "감사위원"·"내부통제"·"준법"을 쓸 수 있다. 이를 보완하기 위해 외부 사전이나 범용 임베딩을 가져오지 않고 ' +
  '분석 corpus 자체에서 FastText를 학습하였다. 파라미터 선택에도 각각 근거가 있다. skip-gram(sg=1)은 문서 수가 적을 때(381건) ' +
  '희소 단어 학습에 유리해 희소한 G·S seed 보강이라는 목적에 맞고, min_count=3은 "넷제로"(9회)·"부패방지"(8회)처럼 ' +
  '빈도가 낮은 핵심어가 더 높은 기준에서 제외되는 위험을 피하기 위함이며, vector_size=100·window=5는 corpus 규모에 맞춘 표준값이다. ' +
  'corpus로 직접 학습한 임베딩은 뉴스 기반 범용 사전보다 공시 맥락의 ESG 표현을 더 잘 반영한다.'
));
C.push(body(
  '확장 후보는 seed와의 cosine 유사도가 임계값 θ를 넘는 단어로 정했다. θ는 단어가 seed와 얼마나 비슷해야 후보로 받을지를 정하는 문턱으로, ' +
  '낮추면 후보가 늘지만 잡음도 늘고 높이면 좋은 단어를 놓친다. 0.55–0.75를 훑어 각 θ에서 후보 수·잡음 비율·수동 검토 가능성을 비교한 결과 θ=0.65를 택하였다. ' +
  'θ=0.60은 후보 770개로 직접 검토가 비현실적이었고, θ=0.70은 286개로 줄지만 이미 희소한 S 후보가 추가로 사라졌다. ' +
  'θ=0.65는 약 493개로 사람이 전수 검토할 수 있는 규모이면서 잡음 비율도 1.0% 수준을 유지하는 절충점이었다. ' +
  '이는 모형 성능을 본 뒤 사후 조정한 값이 아니라, 후보 규모와 검토 가능성의 균형으로 사전에 정한 값이다.'
));
C.push(body(
  'FastText가 제시한 후보를 그대로 사전으로 확정하지는 않았다. 임베딩은 문맥이 비슷한 단어를 잘 찾지만 고유명사나 시사 노이즈도 ' +
  '가까운 후보로 가져오기 때문이다. 자동 필터로 2자 미만·숫자·영문 전용·불용어·차원 중복을 제거한 뒤, 사람이 후보를 직접 읽고 ' +
  '인명·기관명·지명·형태소 오분리·의미 무관 후보를 기각하였다. θ=0.65의 초기 후보 660개(중복 포함)는 자동 필터를 거쳐 475개로, ' +
  '수동 검토에서 42개가 기각되어 최종 433개로 확정되었다.'
));
C.push(cap('표 2. 확장 사전 큐레이션 채택·기각 예시'));
C.push(tbl(
  ['후보', 'seed', 'cosine', '결정', '사유'],
  [
    ['배출량', '온실가스', '0.909', '채택', 'E 측정 단위, 의미 직접 연결'],
    ['재사용', '재활용', '0.751', '채택', 'E 동의어 계열'],
    ['보건', '안전', '0.768', '채택', 'S 안전보건 묶음 어휘'],
    ['감사위원', '감사위원회', '0.973', '채택', 'G 직접 관련'],
    ['블룸버그', '온실가스', '–', '기각', '금융정보기관 고유명사'],
    ['디자', '인권', '0.750', '기각', '형태소 오분리'],
    ['침공', '공급망', '0.676', '기각', '시사 노이즈'],
    ['콩기름', '재생에너지', '–', '기각', '의미 무관'],
  ],
  [1500, 1500, 1100, 1000, 3972]
));
C.push(body(
  '기각률은 E 9.8%, G 5.8%, S 40.7%로 차원마다 크게 달랐다. G는 후보가 많아도 실제 거버넌스 어휘가 대부분이라 기각이 적었던 반면, ' +
  'S는 시사·형태소 노이즈 비중이 커 기각률이 가장 높았다. 이는 앞서 seed 단계에서 확인한 S 신호의 희소성을 다시 보여준다. ' +
  '확장 사전으로 측정한 차원별 점수는 seed 대비 E +195%, S +63%, G +2185%로, 특히 G에서 확장 사전의 보완 효과가 가장 컸다. ' +
  '의무공시 어휘는 변별력이 낮았지만 "감사위원"·"내부통제"·"준법"·"독립성"처럼 기업마다 다르게 쓰는 실천 어휘가 G 신호를 더 잘 포착한 것이다.'
));
C.push(h2('3.4 기준 문장 cosine'));
C.push(body(
  '보조 측정으로 E·S·G 대표 문장 각 1개와 firm-year 문서의 TF-IDF cosine 유사도를 계산하였다. ' +
  '기준 문장이 짧아 벡터가 희소한 탓에 평균 cosine은 0.016–0.024로 매우 낮으므로, 이 값은 의미 유사도나 성과 점수로 과해석하지 않고 ' +
  'firm-year 간 상대 순위를 보는 보조 지표로만 사용하였다. 또한 회귀에서 cosine 계열의 큰 계수는 값 자체가 작아 단위당 계수가 ' +
  '커 보이는 것이지 효과 크기가 큰 것이 아니므로 방향 확인용으로만 읽었다.'
));
C.push(h2('3.5 측정 타당도 교차검증'));
C.push(body(
  '사전 기반 TF-IDF가 ESG 의미를 제대로 포착하는지 점검하기 위해, 한국어 문장 임베딩 모델(ko-sroberta-multitask)로 ' +
  '기준 문장과 firm-year 문장 간 의미 유사도(dense cosine)를 계산하여 TF-IDF cosine과 나란히 비교하였다. ' +
  '최신 의미 임베딩이 단어 겹침 기반보다 항상 낫다는 통념이 이 과제에도 적용되는지 확인하려는 것이다.'
));
C.push(fig('fig3_dense_vs_tfidf.png', 540, 282, 'Dense vs TF-IDF 비교'));
C.push(cap('그림 3. 의미 임베딩(dense)과 단어 기반(TF-IDF) cosine의 등급 상관 비교. 세 차원 모두 TF-IDF의 Spearman ρ가 dense보다 높다(E 0.367 vs 0.229, S 0.276 vs −0.144, G 0.290 vs −0.031). dense는 S·G에서 등급과 역방향이거나 무의미하다.'));
C.push(body(
  '결과는 통념과 반대였다. 짧은 기준 문장 하나와 긴 문서를 비교하는 이 설정에서는 의미 임베딩이 다양한 서술을 한 점으로 압축해 변별력이 떨어지고, ' +
  '일반 도메인 모델이라 공시체 특유의 미세한 표현 차이를 포착하지 못했다. 이 정직한 반증은 본 분석이 TF-IDF 계열 측정을 ' +
  '주력 feature로 삼는 선택이 적어도 이 과제에서는 타당함을 역으로 뒷받침한다. dense는 본선 측정을 대체하지 않고 ' +
  '수렴 타당도를 점검하는 보조 지표로 위치시켰다.'
));
C.push(h2('3.6 회귀 설계'));
C.push(body(
  '종속변수인 ESG 등급이 서열형이라는 점을 고려해 단일 모형에 의존하지 않고 세 모형을 병행하였다. ' +
  'OLS는 등급을 연속값으로 보는 가장 단순한 baseline으로 계수 해석이 직관적이고, Ordered Logit은 등급 간 등간성을 가정하지 않고 ' +
  '순서 정보만 사용하며, Binary Logit은 A 이상 여부로 압축해 해석이 쉽고 강건성을 확인해 준다. ' +
  '세 모형의 역할은 각각 직관, 이론 정합성, 강건성 확인이다.'
));
C.push(body(
  '모든 모형에는 분량(log_n_tokens)을 함께 넣어 분량 효과를 제거한 뒤 ESG 신호를 보았다(M1). ' +
  '추가로 기업 규모가 보고서 분량과 등급을 동시에 끌어올리는 교란일 수 있으므로, 규모(log_assets)·수익성(roa)·재무위험(leverage)을 ' +
  '더 통제한 모형도 추정하였다(M2). 재무 세 변수가 모두 확보된 344 firm-year에 적용하였고, 결측은 가짜 0 대신 목록별 제외로 처리하였다. ' +
  'seed·expanded·cosine은 한 회귀식에 같이 넣지 않았는데, E와 S에서 seed와 expanded의 상관이 각각 0.937, 0.817로 높아 ' +
  '다중공선성 위험이 크기 때문이다. 대신 세 feature set을 나누어 같은 결론이 반복되는지 확인하였다.'
));

// --- 4. Results ---
C.push(h1('4. Results'));
C.push(h2('4.1 공시 분량이 ESG 어휘보다 강하게 연관된다'));
C.push(body(
  '회귀로 들어가기 전, 각 feature가 등급과 기본적으로 연관되는지 순위 기반으로 먼저 확인하였다. ' +
  '등급 4종(esg·e·s·g)과 feature 10개를 교차한 40개 검정을 수행하고 다중비교를 BH-FDR로 보정한 결과, ' +
  '모든 feature가 보정 후에도 p<0.01로 유의하였다. 그러나 가장 중요한 사실은 ESG 어휘 feature가 아니라 ' +
  '단순 토큰 수가 등급과 가장 강하게 연관되었다는 점이다.'
));
C.push(cap('표 3. 주요 feature와 ESG 통합등급 간 Spearman ρ (FDR 보정 후 40/40 유의)'));
C.push(tbl(
  ['Feature', 'ESG 통합등급 ρ', '해석'],
  [
    ['n_tokens', '0.663', '전체 1위 — cheap-talk 핵심 증거'],
    ['expanded_score_G', '0.425', '중간, g_grade에 가장 강함'],
    ['expanded_score_E', '0.373', '중간'],
    ['ref_cosine_E', '0.321', '약한~중간'],
    ['seed_score_E', '0.306', '약한~중간'],
    ['seed_score_G', '0.248', '약함'],
    ['expanded_score_S', '0.212', '약함'],
  ],
  [3300, 1900, 3872]
));
C.push(body(
  '토큰 수의 ρ=0.663은 어떤 개별 ESG feature(최대 0.451)보다 높다. 집단 비교에서도 같은 방향이 확인되었다. ' +
  'A 이상 등급 기업(138건)의 평균 토큰 수는 7,523으로 B+ 이하(243건)의 3,547보다 약 2.1배 많았고, ' +
  'Mann-Whitney U 검정의 효과크기는 r=0.649로 "강함" 수준이었다. Binary Logit에서 log_n_tokens의 승산비는 약 7.9였는데, ' +
  '이는 토큰 수가 e배(약 2.7배) 늘 때 A 이상 등급일 odds가 약 8배 높아진다는 의미다. ' +
  '여기서 odds는 확률 자체가 아니라 p/(1−p)이므로 "확률이 8배"로 읽지 않도록 주의한다. ' +
  '모든 ESG feature가 통계적으로 유의했지만 효과크기는 약함~중간에 머물렀고, 가장 큰 연관은 분량이 차지했다. ' +
  '이것이 이후 모든 회귀에서 분량을 반드시 통제해야 하는 이유다.'
));
C.push(h2('4.2 회귀: 분량·규모를 통제하면 G만 독립 신호로 남는다'));
C.push(body(
  '분량을 통제한 OLS(M1)에서 확장 사전 모형의 설명력은 R²=0.476이었고, log_n_tokens의 계수가 1.297(p<0.001)로 가장 컸다. ' +
  'ESG feature 중에서는 expanded_G만 분량 통제 후에도 강하게 유의했고(β=3.174, p<0.001), expanded_E는 약하게 유의했으며(β=0.432, p=0.025), ' +
  'expanded_S는 유의하지 않은 음수였다(β=−0.695, p=0.302). Ordered Logit과 Binary Logit에서도 expanded_G는 같은 방향으로 유의해' +
  '(각각 β=4.944, OR=27.1) 결론이 모형 선택에 좌우되지 않음을 확인하였다. 다음으로 기업 규모 교란을 분리하기 위해 재무변수를 추가하였다(M2).'
));
C.push(fig('fig4_m1m2_dumbbell.png', 540, 273, 'M1→M2 계수 변화'));
C.push(cap('그림 4. 분량 통제(M1)와 재무통제 추가(M2)에 따른 ESG feature 계수 변화. expanded_G(파란 점)는 M2에서도 유의하게 유지되고, expanded_E(빨간 점)는 유의성이 사라진다.'));
C.push(cap('표 4. OLS 회귀 결과 — 확장 사전 feature set, M1(분량 통제)·M2(분량+재무 통제, n=344)'));
C.push(tbl(
  ['Feature', 'M1 β', 'M1 p', 'M2 β', 'M2 p', '판정'],
  [
    ['expanded_G', '+3.174', '<0.001', '+1.955', '<0.001', '★ 견고'],
    ['expanded_E', '+0.432', '0.025', '+0.172', '0.396', '유의성 소멸'],
    ['expanded_S', '−0.695', '0.302', '−0.070', '0.918', '비유의'],
    ['log_n_tokens', '+1.297', '<0.001', '+0.718', '<0.001', '절반↓이나 견고'],
  ],
  [2500, 1100, 1000, 1100, 1000, 2372]
));
C.push(note('주: M2에 log_assets β=+0.262(p<0.001), roa β=+2.503(p=0.005) 포함. R² 0.476 → 0.551.'));
C.push(body(
  'G는 규모·수익성·재무위험을 통제한 뒤에도 독립 신호를 유지하였다. 계수 β=1.955를 실제 분포(평균 0.197, SD 0.133)로 환산하면 ' +
  '1 표준편차 증가가 약 0.26등급 상승에 해당해, 분량만 통제했을 때의 약 0.42등급에서 줄지만 여전히 유의한 크기다. ' +
  '반면 E는 재무 통제 후 유의성이 사라져, M1에서 보이던 환경 신호의 상당 부분이 사실은 기업 규모 교란이었음이 드러났다. ' +
  '큰 기업이 환경 서술도 많이 하고 등급도 높은 간접 경로였던 것이다. S는 분량만 통제한 단계에서도 이미 비유의여서, ' +
  '사업보고서 텍스트만으로는 사회 차원의 안정적 측정이 어렵다는 점을 확인하였다. 분량 자체는 재무 통제 후 계수가 절반으로 줄었지만 ' +
  '여전히 강하게 유의해, cheap-talk이 단순한 규모 효과로 환원되지 않는 독립적 연관임을 보강한다.'
));
C.push(h2('4.3 G 신호는 이사회 공시 섹션(VI)에 국소화된다'));
C.push(body(
  '분량을 통제하고 남은 G 신호가 보고서의 어느 부분에서 오는지 추적하기 위해, 합본 텍스트를 II·IV·VI로 복원하고 ' +
  '섹션별 9개 ESG 어휘 강도를 산출하였다. 여기서 핵심은 섹션의 글자 수가 아니라 섹션별 어휘 강도다. ' +
  '섹션 점수와 해당 차원 등급의 Spearman ρ를 행렬로 정리하면 차원 신호가 자기 섹션에 모이는 패턴이 드러난다.'
));
C.push(fig('fig5_localization_heatmap.png', 410, 308, '섹션 국소화 히트맵'));
C.push(cap('그림 5. 섹션별 어휘 강도와 차원 등급 간 Spearman ρ 히트맵. VI_G가 0.526으로 가장 진하며, 전체 문서 기준 G 상관(0.426)을 넘어선다. E는 II·IV에 분산되고 S는 섹션 단위에서도 일관된 신호를 보이지 않는다.'));
C.push(cap('표 5. 섹션 국소화 행렬: ρ(섹션 점수, 차원 등급). ⁿˢ=p≥0.05, 그 외 전부 p<0.05.'));
C.push(tbl(
  ['섹션', 'E (e_grade)', 'S (s_grade)', 'G (g_grade)'],
  [
    ['II (사업내용)', '+0.378', '+0.247', '+0.282'],
    ['IV (경영진단)', '+0.341', '+0.033 ⁿˢ', '+0.446'],
    ['VI (기관)', '+0.129', '+0.315', '+0.526 ★'],
    ['(참고) 전체 문서', '0.451', '0.230', '0.426'],
  ],
  [2800, 2091, 2091, 2090]
));
C.push(body(
  'VI_G의 0.526이 전체 문서 G 상관 0.426을 넘는다는 것은, 지배구조를 그것이 실제 공시되는 섹션에서 측정할 때 신호가 더 선명해진다는 뜻이다. ' +
  '이 선명화가 단순히 VI 섹션이 짧아 G 어휘 밀도가 높아진 결과일 가능성을 배제하기 위해, 섹션 글자 수와 전체 분량을 함께 통제한 회귀를 추가하였다. ' +
  '그 결과 VI_G(β=1.738)와 IV_G(β=1.969)는 섹션 길이를 통제한 뒤에도 유의했으나, II_G(β=0.464, p=0.320)는 길이에 흡수되었다. ' +
  '환경은 반대 지형을 보여, II_E(β=0.592)는 유의했으나 IV_E(β=0.207)는 흡수되었다. 즉 거버넌스의 실질 서술은 기관(VI)·경영진단(IV)에 있고 ' +
  '사업내용(II)의 거버넌스 언급은 분량에 가까운 보일러플레이트이며, 환경은 구조화된 사업내용(II)이 실질이고 경영진단(IV)의 환경 언급은 분량으로 흡수된다. ' +
  '"자발적 서술 섹션일수록 cheap-talk"이라는 단순 도식이 차원마다 다르게 나타난 것이다.'
));
C.push(body(
  '이 국소화가 업종이나 연도의 부산물인지 확인하기 위해 업종·연도 고정효과를 추가했을 때도 VI_G(β=1.755)·IV_G(β=2.079)·II_E는 견고하였고, ' +
  '특히 II_E는 계수가 0.592에서 0.723으로 오히려 강화되었다. 에너지 기업이 환경어를 많이 쓰는 섹터 교란을 통제한 뒤에도, ' +
  '같은 업종 안에서 환경 서술이 많은 firm-year가 더 높은 e_grade를 받는 신호가 남은 것이다. ' +
  '마지막으로 이 국소화가 확장 사전 매칭의 산물이 아닌지 확인하기 위해, 사전을 쓰지 않고 의미 임베딩으로 ' +
  '섹션 문장을 E/S/G/무관 기준 문장에 최근접 분류하였다.'
));
C.push(fig('fig6_section_classification.png', 540, 307, '의미 임베딩 섹션 분류'));
C.push(cap('그림 6. 의미 임베딩 기반 섹션별 E/S/G 문장 비율(60 firm-year 층화표본). VI 섹션 문장의 97.9%가 G로 분류되어, 사전에 의존하지 않는 측정에서도 거버넌스 신호의 VI 집중이 재현된다.'));
C.push(cap('표 6. 의미 임베딩 최근접 분류 기반 섹션별 E/S/G 문장 비율'));
C.push(tbl(
  ['섹션', 'E 비율', 'S 비율', 'G 비율'],
  [
    ['II (사업내용)', '0.060', '0.047', '0.106'],
    ['IV (경영진단)', '0.046', '0.015', '0.119'],
    ['VI (기관)', '0.001', '0.008', '0.979 ★'],
  ],
  [3600, 1824, 1824, 1824]
));
C.push(body(
  '측정 방식을 사전 기반에서 의미 임베딩으로 바꿔도 G의 VI 집중이 그대로 나타났고, E가 II에서 다소 높고 S가 전 섹션에서 미약한 패턴도 본선과 일치하였다. ' +
  '다만 이 분류는 기준 문장 설계에 민감하고 층화표본에 기반하므로, 본선 결과를 대체하지 않는 방향성 교차검증으로만 해석한다.'
));

// --- 5. Discussion ---
C.push(h1('5. Discussion'));
C.push(h2('5.1 cheap-talk의 차원별·섹션별 지형'));
C.push(body(
  '본 분석에서 가장 분명한 사실은 공시 분량의 지배력이다. 토큰 수의 ρ=0.663과 Binary Logit OR≈7.9는 ' +
  '등급이 높은 기업이 사업보고서를 더 길게 쓴다는 점을 강하게 보여준다. 그러나 "분량이 지배적이다"에서 멈추면 그 아래 층위를 놓친다. ' +
  '분량과 재무를 통제한 뒤에도 G 어휘, 특히 VI 섹션의 G 어휘에는 독립 신호가 남기 때문이다.'
));
C.push(body(
  '이 신호가 실제 거버넌스 품질을 반영하는지까지는 본 분석으로 식별할 수 없다. 다만 VI 섹션은 이사회 구성·감사위원회·내부통제처럼 ' +
  '법적으로 의무화된 공시 영역이라는 점에 주목할 만하다. 의무공시 틀이 일정한 정보 생산 기능을 한다면, ' +
  '보고서를 단순히 늘리는 것과 달리 VI에서의 구체적 거버넌스 서술은 측정 가능한 성과 차이와 연결될 여지가 있다. ' +
  '반대로 E 신호가 규모 통제 후 사라진 것은 환경 서술이 주로 기업 규모를 경유해 등급과 연관됨을 시사하며, ' +
  'S 신호의 일관된 비유의는 사회 차원이 사업보고서 II·IV·VI만으로는 충분히 구체적으로 드러나지 않거나 분량 효과와 더 많이 겹친다는 한계를 보여준다.'
));
C.push(h2('5.2 경영·금융학적 함의'));
C.push(body(
  '이 결과는 ESG 공시를 정보로 활용하는 입장에서 두 가지 함의를 갖는다. 첫째, 사업보고서 ESG 어휘량을 그대로 ESG 성과의 대리지표로 쓰는 것은 위험하다. ' +
  '가장 강한 신호가 어휘의 질이 아니라 분량이라는 사실은, 공시 텍스트를 신호로 삼을 때 disclosure verbosity를 반드시 분리해야 함을 보여준다. ' +
  '이는 Berg et al.(2022)이 지적한 ESG 등급의 측정 의존성과 같은 맥락에 있다. ' +
  '텍스트 기반 측정 역시 어떤 어휘를, 어느 섹션에서, 무엇을 통제하고 재느냐에 따라 결론이 달라지기 때문이다.'
));
C.push(body(
  '둘째, 그럼에도 측정을 정교화하면 의미 있는 신호를 분리할 수 있다는 점이다. 거버넌스 신호가 의무공시 보편어가 아니라 실천 어휘에서, ' +
  '그리고 전체 문서가 아니라 해당 섹션에서 더 선명해진다는 발견은, 공시 텍스트 분석이 측정 설계에 따라 외부 평가를 보완하는 ' +
  '독립 정보를 제공할 수 있음을 시사한다. 이는 corpus 특화 사전의 필요성을 강조한 Loughran and McDonald(2011)의 문제의식과도 이어진다.'
));
C.push(h2('5.3 한계'));
C.push(body(
  '본 결과 해석에는 분명한 제약이 있다. 표본 381 firm-year는 수업용 pilot 성격이라 한국 전체 상장기업을 대표하지 않는다. ' +
  'KCGS 단일 등급만 사용하였는데, 평가기관 간 등급 불일치가 크다는 점을 고려하면 결론이 평가기관 선택에 민감할 수 있다. ' +
  '텍스트 원천을 사업보고서로 한정해 지속가능경영보고서 등은 포함하지 않았고, S 등급은 A+에 112건이 몰려 분산이 작아 신호가 약하게 추정될 여지가 있다. ' +
  '또한 공시 시점과 평가 시점을 한 해 차이로 정렬했으나 데이터의 실제 라벨과 이 정의 사이에 불일치가 있을 경우 연관의 크기가 다소 약화될 수 있다. ' +
  '무엇보다 모든 결과는 연관 관찰이며 인과가 아니다. ESG 어휘를 늘리면 등급이 오른다거나, 보고서를 길게 쓰면 평가가 개선된다거나, ' +
  'G 어휘가 풍부하면 실제 지배구조가 우수하다는 주장은 본 분석으로부터 도출할 수 없다.'
));

// --- 6. Conclusion ---
C.push(h1('6. Conclusion'));
C.push(body(
  '사업보고서 ESG 어휘 강도와 KCGS 등급의 관계를 381 firm-year에서 분석한 결과는 세 가지로 정리된다. ' +
  '첫째, 둘 사이에는 통계적 연관이 있으나 가장 강한 요인은 ESG 어휘가 아니라 공시 분량이다. ' +
  '둘째, 분량과 기업 규모를 통제하면 차원별 신호가 갈려, G는 독립 신호로 남고 E는 규모 교란으로 약해지며 S는 비유의에 머문다. ' +
  '셋째, 남은 G 신호는 이사회 공시 섹션(VI)에 국소화되어 그곳에서 측정할 때 등급과의 연관이 가장 선명해지며, ' +
  '이 패턴은 사전에 의존하지 않는 의미 임베딩 분류에서도 재현된다.'
));
C.push(body(
  '본 연구의 기여는 공시 텍스트라는 단일 자료 안에서도 측정의 차원과 섹션을 달리하면 cheap-talk과 실질 신호를 부분적으로 분리할 수 있음을 보인 데 있다. ' +
  '사업보고서 ESG 표현은 외부 등급과 연관되지만 그 연관의 상당 부분은 분량과 얽혀 있으며, ' +
  '보고서가 길고 그럴듯하다는 이유로 ESG 성과가 높다고 단정해서는 안 된다. ' +
  '후속 연구에서 지속가능경영보고서, 복수 평가기관 등급, 더 긴 패널을 결합하면 ' +
  '공시 언어와 실제 성과 사이의 괴리를 한층 정밀하게 추적할 수 있을 것이다.'
));

// --- References ---
C.push(new Paragraph({ children: [new PageBreak()] }));
C.push(h1('References'));
[
  'Berg, F., Koelbel, J. F., & Rigobon, R. (2022). Aggregate confusion: The divergence of ESG ratings. Review of Finance, 26(6), 1315–1344. https://doi.org/10.1093/rof/rfac033',
  '금융감독원. (n.d.). OpenDART API 개발가이드. 전자공시시스템. https://opendart.fss.or.kr',
  '한국ESG기준원. (n.d.). ESG 평가 등급 안내. https://www.cgs.or.kr',
  'Loughran, T., & McDonald, B. (2011). When is a liability not a liability? Textual analysis, dictionaries, and 10-Ks. The Journal of Finance, 66(1), 35–65. https://doi.org/10.1111/j.1540-6261.2010.01625.x',
  'Park, B. (2024). Kiwipiepy: A morphological analyzer for Korean. https://github.com/bab2min/Kiwi',
  'Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825–2830.',
  'Řehůřek, R., & Sojka, P. (2010). Software framework for topic modelling with large corpora. In Proceedings of LREC 2010 Workshop on New Challenges for NLP Frameworks (pp. 45–50).',
].forEach(ref => C.push(new Paragraph({
  alignment: AlignmentType.BOTH,
  indent: { left: 360, hanging: 360 },
  spacing: { before: 0, after: 100, line: LS_BODY, lineRule: 'auto' },
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
  const out = path.join(__dirname, '보고서_v5_상세본.docx');
  fs.writeFileSync(out, buf);
  console.log('완료:', out);
}).catch(e => console.error('오류:', e));
