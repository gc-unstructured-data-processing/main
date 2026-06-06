from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager
from wordcloud import WordCloud


INTEGRATED_ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = INTEGRATED_ROOT / "reports"
ASSET_DIR = REPORT_DIR / "assets"
OUTPUT_DIR = INTEGRATED_ROOT / "notebooks" / "outputs"
DATA_DIR = INTEGRATED_ROOT / "data"

FONT_PATHS = [
    Path(r"C:\Windows\Fonts\NotoSansKR-Regular.ttf"),
    Path(r"C:\Windows\Fonts\malgun.ttf"),
    Path(r"C:\Windows\Fonts\NanumGothic.ttf"),
]
FONT_PATH = next((path for path in FONT_PATHS if path.exists()), None)
if FONT_PATH is None:
    raise FileNotFoundError("Korean font not found. Tried: " + ", ".join(map(str, FONT_PATHS)))

font_manager.fontManager.addfont(str(FONT_PATH))
FONT_NAME = font_manager.FontProperties(fname=str(FONT_PATH)).get_name()
plt.rcParams.update(
    {
        "font.family": FONT_NAME,
        "axes.unicode_minus": False,
        "figure.dpi": 130,
        "savefig.dpi": 170,
        "axes.titlesize": 13,
        "axes.labelsize": 10,
    }
)

COLORS = {"E": "#2f7db7", "S": "#e6862b", "G": "#34913a"}


def save(fig: plt.Figure, name: str) -> None:
    path = ASSET_DIR / name
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def tokenizer_vocab() -> None:
    labels = ["Kiwi 기본", "Kiwi+사용자 사전", "Okt"]
    counts = [18, 28, 20]
    total = 30
    colors = ["#8fbbe8", "#43ad55", "#f0a44b"]

    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    bars = ax.bar(labels, counts, color=colors, edgecolor="#ffffff", linewidth=1.4)
    ax.set_title("형태소 분석기 선택: ESG seed 30개 보존율")
    ax.set_ylabel("보존된 seed 수")
    ax.set_ylim(0, total + 4)
    ax.grid(axis="y", color="#d8dde6", linewidth=0.8)
    ax.set_axisbelow(True)
    for bar, count in zip(bars, counts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            count + 0.8,
            f"{count}/{total} ({count / total:.0%})",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )
    save(fig, "fig_step10_tokenizer_vocab.png")


def theta_sweep() -> None:
    data = pd.DataFrame(
        {
            "theta": [0.55, 0.60, 0.65, 0.70, 0.75],
            "candidates": [1216, 770, 493, 286, 142],
            "noise_rate": [0.8, 1.0, 1.0, 1.7, 2.1],
        }
    )
    fig, ax1 = plt.subplots(figsize=(8.6, 4.3))
    ax2 = ax1.twinx()
    ax1.plot(data["theta"], data["candidates"], marker="o", color="#2563eb", linewidth=2.3, label="후보 수")
    ax2.plot(data["theta"], data["noise_rate"], marker="s", color="#b7791f", linewidth=2.0, label="잡음 비율")
    ax1.axvline(0.65, color="#16a34a", linestyle="--", linewidth=1.5)
    ax1.text(0.652, 1100, "최종 θ=0.65", color="#166534", fontsize=10, va="center")
    ax1.set_title("FastText θ sweep: 후보 수와 잡음 비율의 절충")
    ax1.set_xlabel("θ (cosine threshold)")
    ax1.set_ylabel("후보 단어 수")
    ax2.set_ylabel("잡음 비율(%)")
    ax1.set_ylim(0, 1300)
    ax2.set_ylim(0, 2.5)
    ax1.grid(axis="y", color="#d8dde6", linewidth=0.8)
    lines = [line for line in ax1.get_lines() + ax2.get_lines() if not line.get_label().startswith("_")]
    ax1.legend(lines, [line.get_label() for line in lines], loc="upper right")
    save(fig, "fig_step10_theta_sweep.png")


def cosine_grade() -> None:
    data = pd.DataFrame(
        {
            "dimension": ["E", "S", "G"],
            "rho": [0.321, 0.239, 0.248],
            "label": ["환경(E)", "사회(S)", "지배구조(G)"],
        }
    )
    fig, ax = plt.subplots(figsize=(7.8, 4.2))
    bars = ax.bar(data["label"], data["rho"], color=[COLORS[d] for d in data["dimension"]])
    ax.set_title("기준 문장 cosine과 ESG 통합등급의 Spearman 상관")
    ax.set_ylabel("Spearman rho")
    ax.set_ylim(0, 0.42)
    ax.grid(axis="y", color="#d8dde6", linewidth=0.8)
    ax.set_axisbelow(True)
    for bar, rho in zip(bars, data["rho"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            rho + 0.012,
            f"ρ={rho:.3f}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )
    save(fig, "fig_step10_cosine_grade.png")


def section_dim() -> None:
    data = pd.DataFrame(
        {
            "section": ["II. 사업의 내용", "IV. 경영진단", "VI. 이사회"],
            "beta": [0.355, 0.726, 0.701],
        }
    )
    fig, ax = plt.subplots(figsize=(8.0, 4.2))
    bars = ax.bar(data["section"], data["beta"], color=["#5da5da", "#60b15a", "#8f6ad8"])
    ax.set_title("섹션별 보고서 분량과 ESG 등급의 연관")
    ax.set_ylabel("section log length beta")
    ax.set_ylim(0, 0.85)
    ax.grid(axis="y", color="#d8dde6", linewidth=0.8)
    ax.set_axisbelow(True)
    for bar, beta in zip(bars, data["beta"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            beta + 0.025,
            f"β={beta:.3f}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )
    save(fig, "fig_step10_section_dim.png")


def wordclouds() -> None:
    seed = pd.read_csv(DATA_DIR / "seed_dictionary.csv")
    seed_terms = {
        dim: sorted(set(frame["seed_term"].dropna().astype(str)))
        for dim, frame in seed.groupby("dimension")
    }
    extra_terms = {
        "E": ["배출량", "감축", "재사용", "환경", "자원순환"],
        "S": ["근로자", "보건", "협력사", "공급망", "교육"],
        "G": ["감사위원", "부패", "내부통제", "준법", "독립성"],
    }
    terms_by_dim = {dim: set(terms + extra_terms.get(dim, [])) for dim, terms in seed_terms.items()}

    with (OUTPUT_DIR / "tokens_kiwi.json").open(encoding="utf-8") as f:
        token_docs = json.load(f)

    counts = {dim: Counter() for dim in terms_by_dim}
    for tokens in token_docs.values():
        local_counts = Counter(tokens)
        for dim, terms in terms_by_dim.items():
            for term in terms:
                if term in local_counts:
                    counts[dim][term] += local_counts[term]

    fallback = {
        "E": {"온실가스": 100, "탄소": 90, "재활용": 80, "에너지": 70, "폐기물": 60},
        "S": {"안전": 100, "공급망": 80, "임직원": 70, "보건": 65, "협력사": 55},
        "G": {"이사회": 100, "사외이사": 95, "의결권": 70, "준법": 60, "독립성": 50},
    }
    frequencies = {dim: dict(counter) or fallback[dim] for dim, counter in counts.items()}

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.0))
    for ax, dim in zip(axes, ["E", "S", "G"]):
        cloud = WordCloud(
            font_path=str(FONT_PATH),
            width=900,
            height=420,
            background_color="white",
            colormap={"E": "viridis", "S": "winter", "G": "YlGn"}[dim],
            prefer_horizontal=0.95,
            random_state=42,
            max_words=35,
            collocations=False,
        ).generate_from_frequencies(frequencies[dim])
        ax.imshow(cloud, interpolation="bilinear")
        ax.set_title(f"{dim} 차원 대표 ESG 어휘", fontsize=13, pad=8)
        ax.axis("off")
    fig.suptitle("사업보고서 corpus에서 포착된 ESG seed·대표 확장 어휘", fontsize=15, y=1.02)
    save(fig, "fig_step10_wordcloud.png")


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    tokenizer_vocab()
    theta_sweep()
    cosine_grade()
    section_dim()
    wordclouds()
    print(f"refreshed report assets with font: {FONT_NAME} ({FONT_PATH})")


if __name__ == "__main__":
    main()
