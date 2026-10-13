"""Backtest and nowcast (CONTRACT.md files 5 to 8): outputs/backtest.csv, metrics.csv,
leadlag.csv, and nowcast.json.

Usage, from the project root:
    python src/backtest.py           read the real files
    python src/backtest.py --mock    read and write the MOCK_ files

Owner: P2. The spec is pre-registered in tasks/P2.md step 5 and CONTRACT.md files 5 to 8.
Do not add variants after seeing results. Python 3.10+.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]

TARGET_QUARTER = "FY2026Q3"
SIGNALS = ["intent_shock", "stockout_shock"]  # primary, secondary
MODELS = ["persist", "ar", "ar_laya", "ar_stars", "ar_laya_stockout"]
LEADLAG_SIGNALS = ["intent_idx", "stockout_idx"]
MIN_TRAIN = 6
Z80 = 1.2815515655446004  # normal multiplier for a central 80% interval

BACKTEST_COLUMNS = ["fiscal_quarter", "actual", "pred_persist", "pred_ar", "pred_ar_laya",
                    "pred_ar_stars", "signal_used", "train_end_quarter"]
METRICS_COLUMNS = ["model", "mae_bp", "rmse_bp", "n_oos", "n_beats_ar"]
LEADLAG_COLUMNS = ["signal", "lag", "corr", "n"]
NOWCAST_KEYS = ["target_quarter", "beta", "beta_se", "shock_current", "pred_ar", "pred_ar_laya",
                "delta_comp_bp", "delta_comp_bp_lo80", "delta_comp_bp_hi80", "verdict"]


def paths(mock: bool) -> dict[str, Path]:
    p = "MOCK_" if mock else ""
    return {"index": ROOT / "data" / "indices" / f"{p}quarterly_index.csv",
            "quarters": ROOT / "data" / "fundamentals" / f"{p}dks_quarters.csv",
            "backtest": ROOT / "outputs" / f"{p}backtest.csv",
            "metrics": ROOT / "outputs" / f"{p}metrics.csv",
            "leadlag": ROOT / "outputs" / f"{p}leadlag.csv",
            "nowcast": ROOT / "outputs" / f"{p}nowcast.json"}


def ols(y: np.ndarray, regressors: list[np.ndarray]):
    """OLS with an intercept and classical standard errors."""
    X = np.column_stack([np.ones(len(y))] + regressors)
    return sm.OLS(y, X).fit()


def series(index: pd.DataFrame, quarters: pd.DataFrame) -> dict[str, np.ndarray]:
    """Banner "all" columns in quarter order, plus comp_pct and its one-quarter lag."""
    allq = index[index.banner == "all"].set_index("fiscal_quarter").loc[quarters.fiscal_quarter]
    comp = quarters.comp_pct.to_numpy(float)
    out = {c: allq[c].to_numpy(float) for c in
           ["intent_idx", "stockout_idx", "intent_shock", "stockout_shock", "stars_shock"]}
    out.update(comp=comp, lag=np.r_[np.nan, comp[:-1]],
               partial=allq.partial.astype(str).eq("True").to_numpy())
    return out


def eligible(x: dict, sig: np.ndarray, skip: int | None = None) -> list[int]:
    """Quarters where comp, lagged comp, and the signal are all present."""
    return [j for j in range(len(sig)) if j != skip
            and not (np.isnan(x["comp"][j]) or np.isnan(x["lag"][j]) or np.isnan(sig[j]))]


def run_backtest(index: pd.DataFrame, quarters: pd.DataFrame) -> pd.DataFrame:
    """File 5: expanding window; first training sample = first 6 eligible quarters."""
    x, qnames = series(index, quarters), list(quarters.fiscal_quarter)
    comp, lag, stars = x["comp"], x["lag"], x["stars_shock"]
    rows = []
    for sig_name in SIGNALS:
        sig = x[sig_name]
        elig = eligible(x, sig)
        for k in range(MIN_TRAIN, len(elig)):
            train, t = np.array(elig[:k]), elig[k]
            a = ols(comp[train], [lag[train]]).params
            c = ols(comp[train], [lag[train], sig[train]]).params
            st = train[~np.isnan(stars[train])]
            pred_stars = np.nan
            if len(st) >= MIN_TRAIN and not np.isnan(stars[t]):
                p = ols(comp[st], [lag[st], stars[st]]).params
                pred_stars = p[0] + p[1] * lag[t] + p[2] * stars[t]
            rows.append({"fiscal_quarter": qnames[t], "actual": comp[t], "pred_persist": lag[t],
                         "pred_ar": a[0] + a[1] * lag[t],
                         "pred_ar_laya": c[0] + c[1] * lag[t] + c[2] * sig[t],
                         "pred_ar_stars": pred_stars, "signal_used": sig_name,
                         "train_end_quarter": qnames[train[-1]]})
    return pd.DataFrame(rows, columns=BACKTEST_COLUMNS)


def run_metrics(bt: pd.DataFrame) -> pd.DataFrame:
    """File 7."""
    prim, sec = bt[bt.signal_used == "intent_shock"], bt[bt.signal_used == "stockout_shock"]
    source = {"persist": (prim, "pred_persist"), "ar": (prim, "pred_ar"),
              "ar_laya": (prim, "pred_ar_laya"), "ar_stars": (prim, "pred_ar_stars"),
              "ar_laya_stockout": (sec, "pred_ar_laya")}
    rows = []
    for model in MODELS:
        frame, column = source[model]
        f = frame[frame[column].notna()]
        err = (f[column] - f.actual) * 100
        err_ar = (f.pred_ar - f.actual) * 100
        n = len(f)
        rows.append({"model": model,
                     "mae_bp": err.abs().mean() if n else np.nan,
                     "rmse_bp": math.sqrt((err ** 2).mean()) if n else np.nan,
                     "n_oos": n,
                     "n_beats_ar": int((err.abs() < err_ar.abs()).sum())})
    return pd.DataFrame(rows, columns=METRICS_COLUMNS)


def num(v) -> float | None:
    """A JSON number, or null for missing."""
    return None if v is None or (isinstance(v, float) and math.isnan(v)) else round(float(v), 6)


def run_nowcast(index: pd.DataFrame, quarters: pd.DataFrame, metrics: pd.DataFrame) -> dict:
    """File 6: fit on all eligible completed quarters; predict the target quarter."""
    x, qnames = series(index, quarters), list(quarters.fiscal_quarter)
    comp, lag, sig = x["comp"], x["lag"], x["intent_shock"]
    t = qnames.index(TARGET_QUARTER)
    out = {k: None for k in NOWCAST_KEYS}
    out.update(target_quarter=TARGET_QUARTER, verdict="scenario")
    elig = np.array(eligible(x, sig, skip=t))
    if np.isnan(sig[t]) or np.isnan(lag[t]) or len(elig) < MIN_TRAIN:
        return out
    ar = ols(comp[elig], [lag[elig]]).params
    fit = ols(comp[elig], [lag[elig], sig[elig]])
    beta, beta_se = fit.params[2], fit.bse[2]
    pred_ar = ar[0] + ar[1] * lag[t]
    pred_laya = fit.params[0] + fit.params[1] * lag[t] + beta * sig[t]
    delta = (pred_laya - pred_ar) * 100
    half = Z80 * beta_se * abs(sig[t]) * 100
    b_excludes_zero = beta - Z80 * beta_se > 0 or beta + Z80 * beta_se < 0
    mae = metrics.set_index("model").mae_bp
    beats_ar = bool(mae["ar_laya"] < mae["ar"])  # False when either is missing
    out.update(beta=num(beta), beta_se=num(beta_se), shock_current=num(sig[t]),
               pred_ar=num(pred_ar), pred_ar_laya=num(pred_laya), delta_comp_bp=num(delta),
               delta_comp_bp_lo80=num(delta - half), delta_comp_bp_hi80=num(delta + half),
               verdict="nowcast" if b_excludes_zero and beats_ar else "scenario")
    return out


def run_leadlag(index: pd.DataFrame, quarters: pd.DataFrame) -> pd.DataFrame:
    """File 8: corr of signal(q) with comp(q + lag), completed quarters only."""
    x = series(index, quarters)
    comp, partial, n_q = x["comp"], x["partial"], len(quarters)
    rows = []
    for sig_name in LEADLAG_SIGNALS:
        s = x[sig_name]
        for lag in (-1, 0, 1):
            pairs = [(s[j], comp[j + lag]) for j in range(n_q)
                     if 0 <= j + lag < n_q and not partial[j] and not partial[j + lag]
                     and not np.isnan(s[j]) and not np.isnan(comp[j + lag])]
            corr = float(np.corrcoef(np.array(pairs).T)[0, 1]) if len(pairs) >= 3 else np.nan
            rows.append({"signal": sig_name, "lag": lag, "corr": corr, "n": len(pairs)})
    return pd.DataFrame(rows, columns=LEADLAG_COLUMNS)


def summary(metrics: pd.DataFrame, nowcast: dict) -> str:
    """Plain-English result, including the scenario case."""
    m = metrics.set_index("model")
    n = int(m.loc["ar_laya", "n_oos"])
    lines = [f"Backtest: {n} out-of-sample quarters."]
    if n:
        lines.append(f"  Average miss (MAE): persistence {m.loc['persist', 'mae_bp']:.0f} bp, "
                     f"AR {m.loc['ar', 'mae_bp']:.0f} bp, AR + Laya intent "
                     f"{m.loc['ar_laya', 'mae_bp']:.0f} bp. AR + Laya beat AR in "
                     f"{int(m.loc['ar_laya', 'n_beats_ar'])} of {n} quarters.")
    if nowcast["delta_comp_bp"] is None:
        lines.append(f"Nowcast {TARGET_QUARTER}: not computable (missing shock or too few "
                     "quarters). Verdict: scenario.")
        return "\n".join(lines)
    lo = nowcast["beta"] - Z80 * nowcast["beta_se"]
    hi = nowcast["beta"] + Z80 * nowcast["beta_se"]
    lines.append(f"Nowcast {TARGET_QUARTER}: the Laya signal moves the AR comp forecast by "
                 f"{nowcast['delta_comp_bp']:+.0f} bp (80% range {nowcast['delta_comp_bp_lo80']:+.0f}"
                 f" to {nowcast['delta_comp_bp_hi80']:+.0f} bp).")
    lines.append(f"  Signal coefficient b = {nowcast['beta']:.3f}, 80% interval {lo:.3f} to {hi:.3f}.")
    if nowcast["verdict"] == "nowcast":
        lines.append("Verdict: NOWCAST. The interval for b excludes zero and the signal beat AR "
                     "out of sample.")
    else:
        lines.append("Verdict: SCENARIO. The signal did not both clear zero and beat AR out of "
                     "sample, so the deck sizes it as a scenario, not a forecast.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Backtest and nowcast (CONTRACT.md files 5 to 8).")
    parser.add_argument("--mock", action="store_true", help="use the MOCK_ files")
    args = parser.parse_args(argv)
    p = paths(args.mock)
    index = pd.read_csv(p["index"], keep_default_na=False, na_values=[""])
    quarters = pd.read_csv(p["quarters"], keep_default_na=False, na_values=[""])
    bt = run_backtest(index, quarters)
    metrics = run_metrics(bt)
    nowcast = run_nowcast(index, quarters, metrics)
    leadlag = run_leadlag(index, quarters)
    for key, frame in [("backtest", bt), ("metrics", metrics), ("leadlag", leadlag)]:
        frame.round(6).to_csv(p[key], index=False, lineterminator="\n")
    p["nowcast"].write_text(json.dumps(nowcast, indent=2) + "\n", encoding="utf-8")
    print(summary(metrics, nowcast))
    print("Wrote " + ", ".join(str(p[k].relative_to(ROOT)) for k in
                               ["backtest", "metrics", "leadlag", "nowcast"]) + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main())
