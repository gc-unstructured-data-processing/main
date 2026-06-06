from __future__ import annotations

from pathlib import Path


REPORT_DIR = Path(__file__).resolve().parents[1]
MD_PATH = REPORT_DIR / "보고서_v2.md"
HTML_PATH = REPORT_DIR / "보고서_내용_v2.html"
INTERNAL_DIR = REPORT_DIR / "_internal"
INTERNAL_QA_PATH = INTERNAL_DIR / "발표_예상_QA_내부용.md"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise ValueError(f"pattern not found: {label}")
    return text.replace(old, new, 1)


def split_block(text: str, start: str, end: str, label: str) -> tuple[str, str]:
    start_idx = text.find(start)
    if start_idx == -1:
        raise ValueError(f"start not found: {label}")
    end_idx = text.find(end, start_idx)
    if end_idx == -1:
        raise ValueError(f"end not found: {label}")
    return text[start_idx:end_idx], text[:start_idx] + text[end_idx:]


def update_markdown() -> None:
    text = MD_PATH.read_text(encoding="utf-8")

    qa_block, without_qa = split_block(
        text,
        "## 12. 발표와 심층 면접 대비 Q&A 30",
        "## 13. 재현 산출물",
        "markdown q&a",
    )
    INTERNAL_DIR.mkdir(parents=True, exist_ok=True)
    INTERNAL_QA_PATH.write_text(
        "# 발표 예상 Q&A 내부용\n\n"
        "> 제출용 보고서 말미에는 붙이지 않고, 발표·심층 면접 준비 때만 참고한다.\n\n"
        + qa_block.strip()
        + "\n",
        encoding="utf-8",
    )

    text = without_qa
    text = text.replace("## 13. 재현 산출물", "## 12. 재현 산출물", 1)
    text = text.replace("## 14. 외부 참고 문헌 및 도구 문서", "## 13. 외부 참고 문헌 및 도구 문서", 1)
    text = text.replace(
        "질의응답 방어력을 보강했다",
        "본문 설명력과 발표 방어력을 보강했다",
        1,
    )

    qna_figure_block, text = split_block(
        text,
        "### 6.6 보고서에 첨부할 시각 자료",
        "---\n\n## 7. Validity 검증",
        "markdown figure dump",
    )
    del qna_figure_block
    text = text.replace("\n\n\n## 7. Validity 검증", "\n\n---\n\n## 7. Validity 검증", 1)

    text = replace_once(
        text,
        "따라서 본 보고서의 최종 주장은 다음과 같다.\n\n"
        "> 이 표본에서는 ESG 관련 공시 언어와 KCGS 등급 사이에 통계적 연관이 존재한다. 그러나 그 연관의 상당 부분은 ESG 어휘의 질적 내용보다 공시 분량, 즉 verbosity와 연결되어 있다. 이는 cheap-talk 가능성과 일관되며, 결과는 인과가 아닌 연관으로만 해석해야 한다.\n\n---",
        "따라서 본 보고서의 최종 주장은 다음과 같다.\n\n"
        "> 이 표본에서는 ESG 관련 공시 언어와 KCGS 등급 사이에 통계적 연관이 존재한다. 그러나 그 연관의 상당 부분은 ESG 어휘의 질적 내용보다 공시 분량, 즉 verbosity와 연결되어 있다. 이는 cheap-talk 가능성과 일관되며, 결과는 인과가 아닌 연관으로만 해석해야 한다.\n\n"
        "발표나 심층 면접에서 이 연구를 설명할 때는 \"예측 모델\"보다 \"공시 언어 연구\"라는 점을 먼저 말해야 한다. 본문 전체에서도 같은 원칙을 유지한다. 즉, `맞혔다`, `원인이다`, `평가 알고리즘을 알아냈다`가 아니라 `이 표본에서는`, `통계적으로 연관된다`, `cheap-talk 가능성과 일관된다`라는 표현을 사용한다.\n\n---",
        "markdown section 1 stance",
    )

    text = replace_once(
        text,
        "실패 행은 0으로 채우지 않고 `collection_meta.csv`의 `status`와 `reason`에 기록하도록 설계했다. 최종 실행에서는 381/381건 모두 SUCCESS였다.\n\n### 2.3 KCGS 등급",
        "실패 행은 0으로 채우지 않고 `collection_meta.csv`의 `status`와 `reason`에 기록하도록 설계했다. 최종 실행에서는 381/381건 모두 SUCCESS였다.\n\n"
        "이 단위를 택한 이유는 같은 회사라도 회계연도마다 사업보고서와 등급이 달라질 수 있기 때문이다. 다만 한 기업이 3개 연도 반복 관측되므로 완전 독립 표본이라고 말하지는 않는다. 향후 표본 기간이 길어지면 기업 고정효과 또는 cluster-robust 표준오차를 추가하는 것이 자연스러운 확장이다.\n\n### 2.3 KCGS 등급",
        "markdown firm-year explanation",
    )

    text = replace_once(
        text,
        "즉 MCP와 Skill은 탐색·인계·검토를 돕는 도구이고, 최종 분석 결과는 Python 코드가 OpenDART 원문을 직접 파싱해 만든 값이다. 이 구조 덕분에 \"LLM이 만든 표를 그대로 제출했다\"는 위험을 피하고, DART lineage와 재현성을 함께 확보했다.\n\n### 3.4 보고서 판단 안내",
        "즉 MCP와 Skill은 탐색·인계·검토를 돕는 도구이고, 최종 분석 결과는 Python 코드가 OpenDART 원문을 직접 파싱해 만든 값이다. 이 구조 덕분에 \"LLM이 만든 표를 그대로 제출했다\"는 위험을 피하고, DART lineage와 재현성을 함께 확보했다. OpenDART API를 직접 사용한 이유도 여기에 있다. `stock_code -> corp_code -> rcept_no -> document.xml` 경로를 남기면 어느 회사·어느 회계연도의 어떤 접수문서를 분석했는지 다시 추적할 수 있다.\n\n### 3.4 보고서 판단 안내",
        "markdown tools explanation",
    )

    text = replace_once(
        text,
        "Komoran과 Kkma는 본선 비교 대상에서 제외했다. Kkma는 느려 전체 381 firm-year 처리에 비효율적이고, Komoran은 사용자 사전 등록 절차가 파일 기반으로 복잡하며 본 프로젝트의 반복 실험 흐름에 덜 적합했다. 다만 이는 이론적으로 불가능하다는 뜻이 아니라, 본 프로젝트의 시간·재현성·seed 보존 목적에 비추어 우선순위에서 제외했다는 의미다.\n\n### 5.3 불용어와 seed 보호",
        "Komoran과 Kkma는 본선 비교 대상에서 제외했다. Kkma는 느려 전체 381 firm-year 처리에 비효율적이고, Komoran은 사용자 사전 등록 절차가 파일 기반으로 복잡하며 본 프로젝트의 반복 실험 흐름에 덜 적합했다. 다만 이는 이론적으로 불가능하다는 뜻이 아니라, 본 프로젝트의 시간·재현성·seed 보존 목적에 비추어 우선순위에서 제외했다는 의미다.\n\n"
        "**그림 1. 형태소 분석기 seed 보존율**  \n"
        "속도보다 복합명사 보존율을 우선했다는 결정을 보여준다. Kiwi는 사용자 사전을 적용했을 때 seed 28/30개를 보존해 최종 분석기로 채택되었다.\n\n"
        "![형태소 분석기 seed 보존율](assets/fig_step10_tokenizer_vocab.png)\n\n### 5.3 불용어와 seed 보호",
        "markdown tokenizer figure",
    )

    text = replace_once(
        text,
        "최종 theta=0.65는 후보 수가 직접 검토 가능한 수준이고, 희소한 S 차원 후보를 과도하게 잃지 않는 절충점이었다.\n\n### 6.4 Expanded dictionary 큐레이션",
        "최종 theta=0.65는 후보 수가 직접 검토 가능한 수준이고, 희소한 S 차원 후보를 과도하게 잃지 않는 절충점이었다. theta 선택은 모형 성능을 높이기 위한 사후 조정이 아니라, 후보 수·잡음·수동 검토 가능성 사이의 균형을 잡는 절차였다.\n\n"
        "**그림 2. FastText theta sweep**  \n"
        "theta가 낮으면 후보가 너무 많아 검토가 어려워지고, theta가 높으면 희소한 S 후보가 사라진다. 본문에서 설명한 trade-off를 시각적으로 확인할 수 있다.\n\n"
        "![FastText theta sweep](assets/fig_step10_theta_sweep.png)\n\n### 6.4 Expanded dictionary 큐레이션",
        "markdown theta figure",
    )

    text = replace_once(
        text,
        "G 차원에서 expanded dictionary의 효과가 가장 컸다. 이는 의무공시 어휘가 아니라 실제로 firm-year별 차이를 보이는 지배구조 관련 실천 어휘를 포착했기 때문이다.\n\n### 6.5 기준 문장 cosine similarity",
        "G 차원에서 expanded dictionary의 효과가 가장 컸다. 이는 의무공시 어휘가 아니라 실제로 firm-year별 차이를 보이는 지배구조 관련 실천 어휘를 포착했기 때문이다.\n\n"
        "**그림 3. ESG seed·대표 확장 어휘 분포**  \n"
        "단어구름은 점수 계산의 근거가 아니라 sanity check용 시각화다. 실제 corpus에서 seed와 대표 확장 어휘가 어떤 규모로 포착되는지 직관적으로 확인하기 위해 넣었다.\n\n"
        "![ESG seed와 대표 확장 어휘](assets/fig_step10_wordcloud.png)\n\n### 6.5 기준 문장 cosine similarity",
        "markdown wordcloud figure",
    )

    text = replace_once(
        text,
        "따라서 이 값은 \"실제 의미 유사도\"나 \"ESG 성과 판정 점수\"로 과해석하지 않았다. 절대값보다 firm-year 간 상대적 순위에 의미를 둔 보조 feature로 사용했다. 향후 심화 분석에서는 dense vector 또는 문장 임베딩 기반 cosine을 적용해 짧은 기준 문장과 긴 공시 문서 사이의 의미적 거리를 더 안정적으로 측정할 수 있다.\n\n---",
        "따라서 이 값은 \"실제 의미 유사도\"나 \"ESG 성과 판정 점수\"로 과해석하지 않았다. 절대값보다 firm-year 간 상대적 순위에 의미를 둔 보조 feature로 사용했다. 향후 심화 분석에서는 dense vector 또는 문장 임베딩 기반 cosine을 적용해 짧은 기준 문장과 긴 공시 문서 사이의 의미적 거리를 더 안정적으로 측정할 수 있다.\n\n"
        "**그림 4. 기준 문장 cosine과 ESG 통합등급의 연관**  \n"
        "이 그림은 예전 산점도처럼 한 점만 보이는 진단용 그림이 아니라, 보고서 본문 수치와 연결되는 Spearman rho 요약이다. cosine은 보조 지표이며 E가 상대적으로 강하고 S·G는 약한 양의 연관을 보인다.\n\n"
        "![기준 문장 cosine과 ESG 통합등급의 연관](assets/fig_step10_cosine_grade.png)\n\n---",
        "markdown cosine figure",
    )

    text = replace_once(
        text,
        "| VI. 이사회 | 0.701 | <0.001 | G 의무공시와 관련 |\n\nIV 섹션이 가장 강했다. 이는 경영진이 자발적으로 성과와 방향성을 설명하는 섹션의 분량이 KCGS 등급과 더 강하게 연결됨을 시사한다. 다만 IV가 강한 이유가 실제 ESG 의지인지, 보고서 작성 관행인지까지는 식별할 수 없다.",
        "| VI. 이사회 | 0.701 | <0.001 | G 의무공시와 관련 |\n\n"
        "**그림 5. 섹션별 분량 효과**  \n"
        "IV와 VI의 beta가 II보다 크다. 이는 ESG 관련 공시가 단순 사업 설명보다 경영진 서술 및 지배구조 공시 영역에서 더 강하게 드러난다는 해석을 뒷받침한다.\n\n"
        "![섹션별 보고서 분량과 ESG 등급의 연관](assets/fig_step10_section_dim.png)\n\nIV 섹션이 가장 강했다. 이는 경영진이 자발적으로 성과와 방향성을 설명하는 섹션의 분량이 KCGS 등급과 더 강하게 연결됨을 시사한다. 다만 IV가 강한 이유가 실제 ESG 의지인지, 보고서 작성 관행인지까지는 식별할 수 없다.",
        "markdown section figure",
    )

    text = replace_once(
        text,
        "본 결과는 cheap-talk 가설과 일관된다.\n\n### 11.2 하면 안 되는 주장",
        "본 결과는 cheap-talk 가설과 일관된다.\n\n"
        "다만 이 표현도 조심해서 써야 한다. 여기서 cheap-talk는 기업이 의도적으로 과장했다는 증명이 아니라, 공시 언어의 양과 외부 평가가 강하게 같이 움직여 실제 ESG 성과와 공시 표현 사이의 괴리가 있을 수 있다는 해석 틀이다.\n\n### 11.2 하면 안 되는 주장",
        "markdown cheap-talk caveat",
    )

    MD_PATH.write_text(text, encoding="utf-8", newline="\n")


def update_html() -> None:
    text = HTML_PATH.read_text(encoding="utf-8")

    qa_block, without_qa = split_block(
        text,
        '    <section id="qa">',
        '    <section id="outputs">',
        "html q&a",
    )
    del qa_block
    text = without_qa

    figures_block, text = split_block(
        text,
        '    <section id="figures">',
        '    <section id="validity">',
        "html figures",
    )
    del figures_block

    text = text.replace('      <a href="#figures">시각자료</a>\n', "", 1)
    text = text.replace('      <a href="#qa">Q&amp;A 30</a>\n', "", 1)
    text = text.replace(
        "시각자료, 발표 Q&amp;A를 보강한 두 번째 버전입니다.",
        "시각자료를 본문 위치에 분산 배치하고 발표 방어 논리를 보강한 두 번째 버전입니다.",
        1,
    )
    text = text.replace(
        "ESG 단어 사용이 등급 변화를 직접 유발한다는 주장은 불가능합니다. 본 분석은 연관 분석입니다.</p>",
        "ESG 단어 사용이 등급 변화를 직접 유발한다는 주장은 불가능합니다. 본 분석은 연관 분석이며, 발표에서는 \"이 표본에서는\", \"연관\", \"가능성\"이라는 표현을 유지해야 합니다.</p>",
        1,
    )

    text = replace_once(
        text,
        "      <div class=\"callout amber\">\n"
        "        <b>S 차원 주의:</b> 최종 노트북의 등급 분포에서 <code>s_grade</code> A+가 112건으로 많아 S 차원 신호가 약하게 추정될 수 있습니다. 이는 S 성과가 중요하지 않다는 뜻이 아니라, 표본 분포와 측정 방식의 한계입니다.\n"
        "      </div>\n"
        "    </section>",
        "      <div class=\"callout amber\">\n"
        "        <b>S 차원 주의:</b> 최종 노트북의 등급 분포에서 <code>s_grade</code> A+가 112건으로 많아 S 차원 신호가 약하게 추정될 수 있습니다. 이는 S 성과가 중요하지 않다는 뜻이 아니라, 표본 분포와 측정 방식의 한계입니다.\n"
        "      </div>\n"
        "      <p>분석 단위를 firm-year로 둔 이유는 같은 회사라도 회계연도마다 사업보고서와 등급이 달라질 수 있기 때문입니다. 다만 같은 기업이 3개 연도 반복 관측되므로, 향후에는 기업 고정효과나 cluster-robust 표준오차를 추가하는 것이 자연스러운 확장입니다.</p>\n"
        "    </section>",
        "html data addendum",
    )

    text = replace_once(
        text,
        "      <table>\n"
        "        <tr><th>섹션</th><th>의미</th><th>선택 이유</th></tr>\n"
        "        <tr><td>II. 사업의 내용</td><td>사업 현황, 환경·사회 활동</td><td>E·S 표현 핵심</td></tr>\n"
        "        <tr><td>IV. 이사의 경영진단 및 분석의견</td><td>경영진의 성과·위험·방향성</td><td>자발적 ESG 서술 가능성</td></tr>\n"
        "        <tr><td>VI. 이사회 등 회사의 기관</td><td>이사회, 감사위원회, 내부통제</td><td>G 공시 핵심</td></tr>\n"
        "      </table>\n"
        "    </section>",
        "      <div class=\"grid two\" style=\"margin-top:14px\">\n"
        "        <figure>\n"
        "          <img src=\"assets/fig_step10_tokenizer_vocab.png\" alt=\"형태소 분석기 seed 보존율\">\n"
        "          <figcaption><b>형태소 분석기 seed 보존율.</b> Kiwi 사용자 사전을 적용했을 때 ESG seed 28/30개를 보존했습니다.</figcaption>\n"
        "        </figure>\n"
        "        <figure>\n"
        "          <img src=\"assets/fig_step10_theta_sweep.png\" alt=\"FastText theta sweep\">\n"
        "          <figcaption><b>FastText θ sweep.</b> θ=0.65는 후보 수와 잡음 비율, 수동 검토 가능성 사이의 절충점입니다.</figcaption>\n"
        "        </figure>\n"
        "      </div>\n"
        "      <table>\n"
        "        <tr><th>섹션</th><th>의미</th><th>선택 이유</th></tr>\n"
        "        <tr><td>II. 사업의 내용</td><td>사업 현황, 환경·사회 활동</td><td>E·S 표현 핵심</td></tr>\n"
        "        <tr><td>IV. 이사의 경영진단 및 분석의견</td><td>경영진의 성과·위험·방향성</td><td>자발적 ESG 서술 가능성</td></tr>\n"
        "        <tr><td>VI. 이사회 등 회사의 기관</td><td>이사회, 감사위원회, 내부통제</td><td>G 공시 핵심</td></tr>\n"
        "      </table>\n"
        "      <figure style=\"margin-top:14px\">\n"
        "        <img src=\"assets/fig_step10_wordcloud.png\" alt=\"ESG seed와 대표 확장 어휘\">\n"
        "        <figcaption><b>ESG seed·대표 확장 어휘.</b> 점수 산출 자체가 아니라 corpus sanity check용 시각화입니다.</figcaption>\n"
        "      </figure>\n"
        "    </section>",
        "html method figures",
    )

    text = replace_once(
        text,
        "      <div class=\"callout red\">\n"
        "        <b>숨기면 안 되는 결과:</b> ESG feature보다 토큰 수가 더 강합니다. 교수님 가이드상 이런 결과를 회피하지 않고 cheap-talk 해석으로 정면 처리해야 합니다.\n"
        "      </div>\n"
        "    </section>",
        "      <figure style=\"margin-top:14px\">\n"
        "        <img src=\"assets/fig_step10_cosine_grade.png\" alt=\"기준 문장 cosine과 ESG 통합등급의 Spearman 상관\">\n"
        "        <figcaption><b>Cosine과 등급 관계.</b> 기준 문장 cosine은 보조 지표이며, 절대값보다 등급과의 순위 연관을 봅니다.</figcaption>\n"
        "      </figure>\n"
        "      <div class=\"callout red\">\n"
        "        <b>숨기면 안 되는 결과:</b> ESG feature보다 토큰 수가 더 강합니다. 교수님 가이드상 이런 결과를 회피하지 않고 cheap-talk 해석으로 정면 처리해야 합니다.\n"
        "      </div>\n"
        "    </section>",
        "html validity figure",
    )

    text = replace_once(
        text,
        "        <tr><td>Governance paradox</td><td>G seed와 expanded G는 왜 다른가?</td><td>seed_G 0점 73.8%, expanded_G 0점 2.4%</td><td>어휘가 실제 품질을 직접 증명하지 않음</td></tr>\n"
        "      </table>\n"
        "    </section>",
        "        <tr><td>Governance paradox</td><td>G seed와 expanded G는 왜 다른가?</td><td>seed_G 0점 73.8%, expanded_G 0점 2.4%</td><td>어휘가 실제 품질을 직접 증명하지 않음</td></tr>\n"
        "      </table>\n"
        "      <figure style=\"margin-top:14px\">\n"
        "        <img src=\"assets/fig_step10_section_dim.png\" alt=\"섹션별 보고서 분량과 ESG 등급의 연관\">\n"
        "        <figcaption><b>섹션별 분량 효과.</b> IV·VI 섹션이 II보다 강하지만, 실제 의지인지 작성 관행인지는 식별할 수 없습니다.</figcaption>\n"
        "      </figure>\n"
        "    </section>",
        "html models figure",
    )

    text = text.replace("<h2>6. Validity 검증</h2>", "<h2>5. Validity 검증</h2>", 1)
    text = text.replace("<h2>7. 회귀와 알파 분석</h2>", "<h2>6. 회귀와 알파 분석</h2>", 1)
    text = text.replace("<h2>8. 해석과 한계</h2>", "<h2>7. 해석과 한계</h2>", 1)
    text = text.replace("<h2>10. 재현 산출물</h2>", "<h2>8. 재현 산출물</h2>", 1)
    text = text.replace(
        "보고서 v2 HTML. 기존 보고서 파일은 보존하고, 최종 노트북 출력값 기준으로 보강했습니다.",
        "보고서 v2 HTML. Q&A는 본문 서술에 흡수하고, 시각자료는 관련 절에 분산 배치했습니다.",
        1,
    )

    HTML_PATH.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    update_markdown()
    update_html()
    print(f"updated {MD_PATH.name}, {HTML_PATH.name}; internal Q&A: {INTERNAL_QA_PATH.name}")


if __name__ == "__main__":
    main()
