"""Build P3 slide figures from the frozen P2 outputs.

Run ``python src/figures.py --mock`` for MOCK_ inputs/outputs and
``python src/figures.py`` after the data freeze.  The script never substitutes
mock inputs for a real run.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PALETTE = {
    "navy": "#17324D",
    "blue": "#2E75B6",
    "teal": "#2A9D8F",
    "orange": "#F28E2B",
    "red": "#D9534F",
    "gray": "#6B7280",
    "light": "#D9E2F3",
}
FOOTNOTE = (
    "Source: team analysis of Reddit/Google text scored with Laya (open source); "
    "DKS earnings releases."
)


def input_path(path: str, mock: bool) -> Path:
    """Return the contracted path, prefixing only the file name for mock runs."""
    target = ROOT / path
    return target.with_name(f"MOCK_{target.name}") if mock else target


def require(paths: list[Path]) -> None:
    missing = [str(p.relative_to(ROOT)) for p in paths if not p.exists()]
    if missing:
        raise FileNotFoundError("Missing required P2/P1 handoffs:\n- " + "\n- ".join(missing))


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 12,
            "axes.titlesize": 20,
            "axes.titleweight": "bold",
            "axes.labelsize": 12,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        }
    )


def save(fig: plt.Figure, name: str, mock: bool) -> None:
    out = ROOT / "figures" / (f"MOCK_{name}" if mock else name)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.text(0.01, 0.012, FOOTNOTE, fontsize=8, color=PALETTE["gray"])
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")


def signal_vs_comps(index: pd.DataFrame, fundamentals: pd.DataFrame, mock: bool) -> None:
    data = index.loc[index["banner"].eq("all")].copy()
    data = data.merge(
        fundamentals[["fiscal_quarter", "comp_pct"]], on="fiscal_quarter", how="left"
    )
    data = data.sort_values("period_start" if "period_start" in data else "fiscal_quarter")
    x = np.arange(len(data))
    colors = [PALETTE["teal"] if value >= 0 else PALETTE["red"] for value in data["intent_shock"]]

    fig, ax = plt.subplots(figsize=(16, 9))
    bars = ax.bar(x, data["intent_shock"], color=colors, width=0.68)
    ax.axhline(0, color=PALETTE["gray"], linewidth=0.8)
    ax.set_ylabel("Intent shock")
    ax.set_xticks(x, data["fiscal_quarter"], rotation=45, ha="right")
    ax.grid(axis="y", alpha=0.18)

    partial = data.get("partial", pd.Series(False, index=data.index)).fillna(False).astype(bool)
    for pos, (bar, is_partial) in enumerate(zip(bars, partial)):
        if is_partial:
            bar.set_hatch("///")
            coverage = float(data.iloc[pos].get("coverage_frac", np.nan))
            label = "nowcast, partial quarter"
            if not np.isnan(coverage):
                label += f" ({coverage:.0%})"
            ax.annotate(label, (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        xytext=(0, 14), textcoords="offset points", ha="center", fontsize=10)
        n_eff = data.iloc[pos].get("n_effective", np.nan)
        if pd.notna(n_eff):
            ax.text(pos, 0.01, f"n={n_eff:.0f}", transform=ax.get_xaxis_transform(),
                    ha="center", va="bottom", fontsize=8, color=PALETTE["gray"])

    ax2 = ax.twinx()
    ax2.plot(x, data["comp_pct"], color=PALETTE["navy"], marker="o", linewidth=2.5)
    ax2.set_ylabel("DICK'S comparable sales (%)")
    ax2.spines["right"].set_visible(True)
    ax.set_title("Consumer intent signal versus DICK'S comparable sales")
    fig.tight_layout(rect=(0, 0.055, 1, 1))
    save(fig, "signal_vs_comps.png", mock)


def topic_mix(items: pd.DataFrame, features: pd.DataFrame, fundamentals: pd.DataFrame, mock: bool) -> None:
    topic_cols = [c for c in features if c.startswith("p_topic_")]
    if not topic_cols:
        raise ValueError("item_features.csv has no p_topic_* columns")
    df = items.merge(features, on="item_id", how="inner", validate="one_to_one")
    df["date"] = pd.to_datetime(df["date_low"], errors="coerce")
    completed = fundamentals.loc[fundamentals["comp_pct"].notna()].copy()
    completed["period_start"] = pd.to_datetime(completed["period_start"])
    completed["period_end"] = pd.to_datetime(completed["period_end"])
    latest = completed.sort_values("period_end").tail(2)
    if len(latest) < 2:
        raise ValueError("Need at least two completed fiscal quarters")
    current_start, current_end = latest["period_start"].min(), latest["period_end"].max()
    prior_start, prior_end = current_start - pd.DateOffset(years=1), current_end - pd.DateOffset(years=1)
    df["period"] = np.where(
        df["date"].between(current_start, current_end), "Latest 2Q",
        np.where(df["date"].between(prior_start, prior_end), "Year-ago 2Q", None),
    )
    banner_cols = [c for c in features if c.startswith("p_banner_")]
    if banner_cols:
        df["banner"] = df[banner_cols].idxmax(axis=1).str.removeprefix("p_banner_")
    else:
        df["banner"] = df.get("banner", df.get("banner_hint", "unknown"))
    df["weight"] = df.get("p_relevant", 1.0) * df.get("p_author_customer", 1.0)
    df = df.loc[df["period"].notna() & df["banner"].ne("other")].copy()

    rows = []
    for (banner, period), group in df.groupby(["banner", "period"]):
        denom = group["weight"].sum()
        if denom <= 0:
            continue
        row = {"label": f"{banner.replace('_', ' ').title()} | {period}"}
        row.update({c: np.average(group[c], weights=group["weight"]) for c in topic_cols})
        rows.append(row)
    plot = pd.DataFrame(rows).set_index("label")
    if plot.empty:
        raise ValueError("No item-level observations fall in the required comparison windows")
    plot = plot.div(plot.sum(axis=1), axis=0)
    change = plot.groupby(plot.index.str.split(" | ", regex=False).str[0]).diff().abs().max()
    highlight = change.idxmax() if change.notna().any() else topic_cols[0]
    colors = [PALETTE["orange"] if c == highlight else plt.cm.Blues(0.3 + 0.6 * i / max(1, len(topic_cols) - 1))
              for i, c in enumerate(topic_cols)]

    fig, ax = plt.subplots(figsize=(16, 9))
    plot.plot.barh(stacked=True, ax=ax, color=colors, width=0.72)
    ax.set_xlabel("Weighted topic share")
    ax.set_ylabel("")
    ax.set_xlim(0, 1)
    ax.xaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
    ax.grid(axis="x", alpha=0.18)
    ax.set_title(f"Topic mix by banner: largest change in {highlight.removeprefix('p_topic_').replace('_', ' ')}")
    ax.legend([c.removeprefix("p_topic_").replace("_", " ") for c in topic_cols],
              loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=4, frameon=False, fontsize=9)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    save(fig, "topic_mix_by_banner.png", mock)


def backtest_mae(metrics: pd.DataFrame, nowcast: dict, mock: bool) -> None:
    model_col = "model" if "model" in metrics else "Model"
    mae_col = "mae_bp" if "mae_bp" in metrics else "MAE_bp"
    n_col = next((c for c in ("n_oos", "n", "oos_quarters") if c in metrics), None)
    order = ["persist", "ar", "ar_stars", "ar_laya"]
    plot = metrics.loc[metrics[model_col].isin(order)].set_index(model_col).reindex(order).dropna(subset=[mae_col])
    n_oos = int(plot[n_col].max()) if n_col and not plot.empty else int(nowcast.get("n_oos", 0))
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.bar(plot.index, plot[mae_col], color=[PALETTE["gray"], PALETTE["blue"], PALETTE["orange"], PALETTE["teal"]][:len(plot)])
    ax.set_ylabel("Out-of-sample MAE (bp)")
    ax.set_title(f"Backtest accuracy | n = {n_oos} out-of-sample quarters")
    ax.grid(axis="y", alpha=0.18)
    for i, value in enumerate(plot[mae_col]):
        ax.text(i, value, f"{value:.0f}", ha="center", va="bottom", fontweight="bold")
    if str(nowcast.get("verdict", "")).lower() == "scenario":
        ax.text(0.5, 0.92, "The signal did not beat the baseline out of sample",
                transform=ax.transAxes, ha="center", color=PALETTE["red"], fontsize=14)
    fig.tight_layout(rect=(0, 0.055, 1, 1))
    save(fig, "backtest_mae.png", mock)


def pipeline_figure(agreement: dict | None, mock: bool) -> None:
    steps = ["Scraped text", "7 frozen Laya\nquestions", "Quarterly indices", "Expanding-window\nbacktest", "Flagged Excel\ndriver"]
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.axis("off")
    xs = np.linspace(0.09, 0.91, len(steps))
    for i, (x, label) in enumerate(zip(xs, steps)):
        ax.text(x, 0.58, label, ha="center", va="center", fontsize=14, color="white",
                bbox={"boxstyle": "round,pad=0.7", "facecolor": PALETTE["blue"], "edgecolor": "none"})
        if i < len(steps) - 1:
            ax.annotate("", xy=(xs[i + 1] - 0.085, 0.58), xytext=(x + 0.085, 0.58),
                        arrowprops={"arrowstyle": "->", "lw": 2, "color": PALETTE["navy"]})
    if agreement:
        values = []
        questions = agreement.get("questions", [])
        for value in questions:
            key = value.get("question", "question")
            pct = value.get("pct_agreement")
            kappa = value.get("cohen_kappa")
            if pct is not None:
                values.append(f"{key}: {float(pct):.0f}% agreement" + (f", κ={float(kappa):.2f}" if kappa is not None else ""))
        agreement_text = "Human validation (50 hand labels): " + "; ".join(values)
    else:
        agreement_text = "Human validation (50 hand labels): agreement pending P2 handoff"
    ax.text(0.5, 0.33, agreement_text, ha="center", va="center", fontsize=12, color=PALETTE["gray"], wrap=True)
    ax.set_title("From consumer text to one auditable model assumption", pad=35)
    fig.tight_layout(rect=(0, 0.055, 1, 1))
    save(fig, "appendix_pipeline.png", mock)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true", help="Use only MOCK_-prefixed inputs and outputs")
    args = parser.parse_args()
    setup_style()
    paths = {
        "index": input_path("data/indices/quarterly_index.csv", args.mock),
        "fundamentals": input_path("data/fundamentals/dks_quarters.csv", args.mock),
        "items": input_path("data/clean/items.csv", args.mock),
        "features": input_path("data/labels/item_features.csv", args.mock),
        "metrics": input_path("outputs/metrics.csv", args.mock),
        "nowcast": input_path("outputs/nowcast.json", args.mock),
    }
    require(list(paths.values()))
    index = pd.read_csv(paths["index"])
    fundamentals = pd.read_csv(paths["fundamentals"])
    items = pd.read_csv(paths["items"])
    features = pd.read_csv(paths["features"])
    metrics = pd.read_csv(paths["metrics"])
    nowcast = read_json(paths["nowcast"])
    agreement_path = input_path("data/labels/agreement.json", args.mock)
    agreement = read_json(agreement_path) if agreement_path.exists() else None
    signal_vs_comps(index, fundamentals, args.mock)
    topic_mix(items, features, fundamentals, args.mock)
    backtest_mae(metrics, nowcast, args.mock)
    pipeline_figure(agreement, args.mock)


if __name__ == "__main__":
    main()
