"""Aggregate scored items into data/indices/quarterly_index.csv (CONTRACT.md file 4).

Usage, from the project root:
    python src/aggregate.py             read the real files
    python src/aggregate.py --mock      read and write the MOCK_ files
    python src/aggregate.py --strict    drop items whose date interval spans a quarter boundary

Owner: P2. The method is CONTRACT.md file 4, steps 1 to 12; comments cite the step numbers.
Python 3.10+.
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

BANNERS = ["dicks", "house_of_sport", "golf_galaxy", "foot_locker", "other"]
INDEX_BANNERS = ["all"] + BANNERS
INDEX_NAMES = ["intent", "stockout", "promo", "stars"]
MIN_N_EFFECTIVE = 15
BANNER_COLS = [f"p_banner_{b}" for b in BANNERS]
COLUMNS = (["fiscal_quarter", "banner", "n_items", "n_effective"]
           + [f"{n}_idx" for n in INDEX_NAMES] + ["volume_log"]
           + [f"{n}_shock" for n in INDEX_NAMES] + ["partial", "coverage_frac"])


def paths(mock: bool) -> dict[str, Path]:
    p = "MOCK_" if mock else ""
    return {"items": ROOT / "data" / "clean" / f"{p}items.csv",
            "features": ROOT / "data" / "labels" / f"{p}item_features.csv",
            "quarters": ROOT / "data" / "fundamentals" / f"{p}dks_quarters.csv",
            "index": ROOT / "data" / "indices" / f"{p}quarterly_index.csv"}


def read_csv(path: Path) -> pd.DataFrame:
    """Read a contract CSV: only an empty field is missing (so text like "NA" stays text)."""
    return pd.read_csv(path, keep_default_na=False, na_values=[""],
                       dtype={"item_id": str, "text": str, "banner_hint": str})


def ordinals(dates: pd.Series) -> np.ndarray:
    return np.array([date.fromisoformat(str(d)[:10]).toordinal() for d in dates])


def shock(x: np.ndarray) -> np.ndarray:
    """Step 10: value minus the mean of the non-missing values in the four prior quarters;
    needs the value and at least 2 prior values."""
    out = np.full(len(x), np.nan)
    for j in range(len(x)):
        prior = x[max(0, j - 4):j]
        prior = prior[~np.isnan(prior)]
        if not np.isnan(x[j]) and len(prior) >= 2:
            out[j] = x[j] - prior.mean()
    return out


def build_index(items: pd.DataFrame, feats: pd.DataFrame, quarters: pd.DataFrame,
                strict: bool = False) -> pd.DataFrame:
    """File 4 from files 1 to 3."""
    df = items.merge(feats, on="item_id", how="inner", validate="one_to_one")
    lo, hi = ordinals(df.date_low), ordinals(df.date_high)
    qs, qe = ordinals(quarters.period_start), ordinals(quarters.period_end)

    days = np.minimum(hi[:, None], qe[None, :]) - np.maximum(lo[:, None], qs[None, :]) + 1
    share = np.clip(days, 0, None) / (hi - lo + 1)[:, None]                # step 2
    if strict:                                                             # step 12
        keep = ~((share > 0) & (share < 1)).any(axis=1)
        df, share = df[keep].reset_index(drop=True), share[keep]
    weight = share * df.p_relevant.to_numpy()[:, None]                     # step 3
    banner = np.array(BANNERS)[df[BANNER_COLS].to_numpy().argmax(axis=1)]  # step 1

    net = (df.p_intent_up - df.p_intent_down).to_numpy()
    cust = df.p_author_customer.to_numpy()
    stock = df.p_stockout.to_numpy()
    promo = df.promo_score_exp.to_numpy()
    stars = pd.to_numeric(df.stars, errors="coerce").to_numpy(float)
    has_stars = (~np.isnan(stars)).astype(float)
    stars = np.nan_to_num(stars)

    data_end = ordinals(items.scraped_at).max()
    cover = np.clip((np.minimum(qe, data_end) - qs + 1) / (qe - qs + 1), 0, 1)  # step 11

    def wmean(values: np.ndarray, w: np.ndarray) -> np.ndarray:
        den = w.sum(axis=0)
        with np.errstate(invalid="ignore", divide="ignore"):
            return np.where(den > 0, (w * values[:, None]).sum(axis=0) / den, np.nan)

    blocks = []
    for b_pos, b in enumerate(INDEX_BANNERS):
        m = np.ones(len(df), bool) if b == "all" else banner == b
        w, s = weight[m], share[m]
        n_eff = w.sum(axis=0)                                              # step 4
        idx = {"intent": wmean(net[m], w * cust[m][:, None]),              # step 5
               "stockout": wmean(stock[m], w),                             # step 6
               "promo": wmean(promo[m], w),                                # step 7
               "stars": wmean(stars[m], s * has_stars[m][:, None])}        # step 8
        block = pd.DataFrame({"fiscal_quarter": quarters.fiscal_quarter.to_numpy(), "banner": b,
                              "n_items": (s > 0).sum(axis=0), "n_effective": n_eff})
        for name in INDEX_NAMES:
            block[f"{name}_idx"] = np.where(n_eff < MIN_N_EFFECTIVE, np.nan, idx[name])  # step 9
        block["volume_log"] = np.log1p(n_eff)
        for name in INDEX_NAMES:
            block[f"{name}_shock"] = shock(block[f"{name}_idx"].to_numpy())  # step 10
        block["partial"] = cover < 1
        block["coverage_frac"] = cover
        block["_q"], block["_b"] = np.arange(len(qs)), b_pos
        blocks.append(block)
    out = pd.concat(blocks).sort_values(["_q", "_b"]).reset_index(drop=True)
    return out[COLUMNS]


def report(index: pd.DataFrame) -> None:
    """Print n_items and n_effective per quarter and banner; warn below the threshold."""
    table = index.pivot(index="fiscal_quarter", columns="banner", values="n_effective")
    table = table.loc[index.fiscal_quarter.unique(), INDEX_BANNERS].round(1)
    print("n_effective by fiscal quarter and banner:")
    print(table.to_string())
    low = index[index.n_effective < MIN_N_EFFECTIVE]
    if len(low):
        print(f"WARNING: {len(low)} quarter-banner cells have n_effective < {MIN_N_EFFECTIVE}; "
              "their indices are empty (missing, not neutral).")
    allq = index[index.banner == "all"]
    usable = allq.intent_shock.notna().sum()
    print(f"Banner 'all': {usable} of {len(allq)} quarters have an intent_shock.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build quarterly_index.csv (CONTRACT.md file 4).")
    parser.add_argument("--mock", action="store_true", help="use the MOCK_ files")
    parser.add_argument("--strict", action="store_true",
                        help="drop items whose date interval spans a quarter boundary")
    args = parser.parse_args(argv)
    p = paths(args.mock)
    items, feats, quarters = read_csv(p["items"]), read_csv(p["features"]), read_csv(p["quarters"])
    unscored = len(set(items.item_id) - set(feats.item_id))
    if unscored:
        print(f"WARNING: {unscored} items have no scores and are left out.")
    index = build_index(items, feats, quarters, strict=args.strict)
    index.round(6).to_csv(p["index"], index=False, lineterminator="\n")
    report(index)
    print(f"Wrote {p['index'].relative_to(ROOT)} ({len(index)} rows).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
