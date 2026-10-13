"""Write MOCK_ versions of CONTRACT.md files 1 to 9, then check them against CONTRACT.md.

Usage, from the project root:
    python src/mock.py            write every MOCK_ file, then run the contract check
    python src/mock.py --check    only check the MOCK_ files that already exist

Every value written here is invented. Never let a MOCK_ number reach the deck or the
Excel model.

Files 1 to 3 and 9 are generated. Files 4 to 8 are computed from the mock items with the
CONTRACT.md method, so build_index and run_backtest also serve as reference versions of
aggregate.py and backtest.py.

Python 3.10+.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from dateutil.relativedelta import relativedelta

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "CONTRACT.md"

SEED = 20261012
N_ITEMS = 5000
FIRST_FY = 2021
LAST_QUARTER = "FY2026Q3"
SCRAPED_AT = datetime(2026, 10, 11, 15, 0, 0, tzinfo=timezone.utc)
SCORED_AT = datetime(2026, 10, 12, 1, 0, 0, tzinfo=timezone.utc)
# MOCK ONLY: assume Foot Locker business comps first appear in FY2025Q3.
# P1 takes the real first quarter from the filings.
FL_FIRST_QUARTER = "FY2025Q3"

BANNERS = ["dicks", "house_of_sport", "golf_galaxy", "foot_locker", "other"]
INDEX_BANNERS = ["all"] + BANNERS
AUTHORS = ["customer", "employee", "other"]
TOPICS = ["availability", "price_promo", "service_staff", "fulfillment_returns",
          "product_quality", "store_experience", "other"]
INTENTS = ["up", "flat", "down"]
INDEX_NAMES = ["intent", "stockout", "promo", "stars"]
SIGNALS = ["intent_shock", "stockout_shock"]
MODELS = ["persist", "ar", "ar_laya", "ar_stars", "ar_laya_stockout"]
LEADLAG_SIGNALS = ["intent_idx", "stockout_idx"]
AGREEMENT_QUESTIONS = ["relevant", "topic", "stockout", "intent"]
MIN_N_EFFECTIVE = 15
MIN_TRAIN = 6
Z80 = 1.2815515655446004  # normal multiplier for a central 80% interval

PATHS = {
    1: "data/clean/MOCK_items.csv",
    2: "data/labels/MOCK_item_features.csv",
    3: "data/fundamentals/MOCK_dks_quarters.csv",
    4: "data/indices/MOCK_quarterly_index.csv",
    5: "outputs/MOCK_backtest.csv",
    6: "outputs/MOCK_nowcast.json",
    7: "outputs/MOCK_metrics.csv",
    8: "outputs/MOCK_leadlag.csv",
    9: "data/labels/MOCK_agreement.json",
}


# ---------------------------------------------------------------- column specs

def col(name, kind, missing=False, allowed=None, lo=None, hi=None, pattern=None):
    """One column (or JSON key) of a contract file. kind is a CONTRACT.md type."""
    return {"name": name, "kind": kind, "missing": missing, "allowed": allowed,
            "lo": lo, "hi": hi, "pattern": pattern}


GROUPS = {
    "banner": [f"p_banner_{b}" for b in BANNERS],
    "author": [f"p_author_{a}" for a in AUTHORS],
    "topic": [f"p_topic_{t}" for t in TOPICS],
    "intent": [f"p_intent_{x}" for x in INTENTS],
}
PROB_COLS = (["p_relevant"] + GROUPS["banner"] + GROUPS["author"] + GROUPS["topic"]
             + ["p_stockout"] + GROUPS["intent"])
ITEM_ID_RE = r"(reddit|google)_[0-9a-f]{16}"

SPECS = {
    1: [col("item_id", "str", pattern=ITEM_ID_RE),
        col("source", "str", allowed=["reddit", "google"]),
        col("banner_hint", "str", missing=True),
        col("text", "str"),
        col("stars", "float", missing=True, lo=1, hi=5),
        col("created_exact", "datetime", missing=True),
        col("date_low", "date"),
        col("date_high", "date"),
        col("date_precision", "str", allowed=["exact", "week", "month", "year"]),
        col("url", "str"),
        col("scraped_at", "datetime")],
    2: ([col("item_id", "str", pattern=ITEM_ID_RE)]
        + [col(c, "float", lo=0, hi=1) for c in PROB_COLS]
        + [col("promo_score_exp", "float", lo=1, hi=5),
           col("promo_entropy", "float", lo=0, hi=math.log(5)),
           col("model_version", "str"),
           col("scored_at", "datetime")]),
    3: [col("fiscal_quarter", "quarter"),
        col("period_start", "date"),
        col("period_end", "date"),
        col("report_date", "date", missing=True),
        col("comp_pct", "float", missing=True),
        col("comp_fl_pct", "float", missing=True),
        col("net_sales_musd", "float", missing=True, lo=0),
        col("gross_margin_pct", "float", missing=True, lo=0, hi=100),
        col("source_url", "str")],
    4: [col("fiscal_quarter", "quarter"),
        col("banner", "str", allowed=INDEX_BANNERS),
        col("n_items", "int", lo=0),
        col("n_effective", "float", lo=0),
        col("intent_idx", "float", missing=True, lo=-1, hi=1),
        col("stockout_idx", "float", missing=True, lo=0, hi=1),
        col("promo_idx", "float", missing=True, lo=1, hi=5),
        col("stars_idx", "float", missing=True, lo=1, hi=5),
        col("volume_log", "float", lo=0),
        col("intent_shock", "float", missing=True),
        col("stockout_shock", "float", missing=True),
        col("promo_shock", "float", missing=True),
        col("stars_shock", "float", missing=True),
        col("partial", "bool"),
        col("coverage_frac", "float", lo=0, hi=1)],
    5: [col("fiscal_quarter", "quarter"),
        col("actual", "float"),
        col("pred_persist", "float"),
        col("pred_ar", "float"),
        col("pred_ar_laya", "float"),
        col("pred_ar_stars", "float", missing=True),
        col("signal_used", "str", allowed=SIGNALS),
        col("train_end_quarter", "quarter")],
    6: [col("target_quarter", "quarter")]
       + [col(k, "float", missing=True) for k in
          ["beta", "beta_se", "shock_current", "pred_ar", "pred_ar_laya",
           "delta_comp_bp", "delta_comp_bp_lo80", "delta_comp_bp_hi80"]]
       + [col("verdict", "str", allowed=["nowcast", "scenario"])],
    7: [col("model", "str", allowed=MODELS),
        col("mae_bp", "float", missing=True, lo=0),
        col("rmse_bp", "float", missing=True, lo=0),
        col("n_oos", "int", lo=0),
        col("n_beats_ar", "int", lo=0)],
    8: [col("signal", "str", allowed=LEADLAG_SIGNALS),
        col("lag", "int", allowed=[-1, 0, 1]),
        col("corr", "float", missing=True, lo=-1, hi=1),
        col("n", "int", lo=0)],
    9: [col("n_items", "int", lo=1),
        col("model_version", "str"),
        col("questions", "list"),
        col("question", "str", allowed=AGREEMENT_QUESTIONS),
        col("n", "int", lo=0),
        col("pct_agreement", "float", lo=0, hi=100),
        col("cohen_kappa", "float", missing=True, lo=-1, hi=1)],
}
QUESTION_KEYS = ["question", "n", "pct_agreement", "cohen_kappa"]


def names(number: int) -> list[str]:
    return [c["name"] for c in SPECS[number]]


# ---------------------------------------------------------------- fiscal calendar

def fiscal_year_end(fy: int) -> date:
    """The Saturday closest to January 31 of the calendar year after fiscal year fy starts."""
    jan31 = date(fy + 1, 1, 31)
    back = (jan31.weekday() - 5) % 7  # days since the previous Saturday
    return jan31 - timedelta(days=back) if back <= 3 else jan31 + timedelta(days=7 - back)


def mock_calendar() -> list[tuple[str, date, date]]:
    """(fiscal_quarter, period_start, period_end) from FY2021Q1 to LAST_QUARTER.

    MOCK ONLY: quarters are 13, 13, 13 weeks and the rest of the year. P1 takes the real
    period dates from the filings.
    """
    out, fy = [], FIRST_FY
    while True:
        start = fiscal_year_end(fy - 1) + timedelta(days=1)
        for q in range(1, 5):
            q_start = start + timedelta(weeks=13 * (q - 1))
            q_end = fiscal_year_end(fy) if q == 4 else q_start + timedelta(days=13 * 7 - 1)
            out.append((f"FY{fy}Q{q}", q_start, q_end))
            if out[-1][0] == LAST_QUARTER:
                return out
        fy += 1


# ---------------------------------------------------------------- generators

def make_quarters(rng) -> tuple[pd.DataFrame, np.ndarray]:
    """File 3. Also returns the hidden true comps, including the unreported last quarter.
    The true comps tilt the mock text so the mock signal has something to find."""
    cal = mock_calendar()
    true_comp, level = np.empty(len(cal)), 9.0
    for j in range(len(cal)):
        level = float(np.clip(3.0 + 0.5 * (level - 3.0) + rng.normal(0, 2.5), -5, 12))
        true_comp[j] = level
    rows = []
    for j, (quarter, start, end) in enumerate(cal):
        reported = quarter != LAST_QUARTER
        has_fl = quarter >= FL_FIRST_QUARTER  # FYyyyyQn strings sort in time order
        q = int(quarter[-1])
        sales = ({1: 2900, 2: 3300, 3: 3000, 4: 3700}[q] * 1.03 ** (j // 4)
                 * (1 + true_comp[j] / 100) + (1900 if has_fl else 0))
        rows.append({
            "fiscal_quarter": quarter,
            "period_start": start.isoformat(),
            "period_end": end.isoformat(),
            "report_date": (end + timedelta(days=24)).isoformat() if reported else "",
            "comp_pct": round(true_comp[j], 1) if reported else np.nan,
            "comp_fl_pct": round(rng.uniform(-4, 6), 1) if reported and has_fl else np.nan,
            "net_sales_musd": round(sales, 1) if reported else np.nan,
            "gross_margin_pct": (round(rng.uniform(35, 37.5) - (1.5 if q == 4 else 0), 2)
                                 if reported else np.nan),
            "source_url": "MOCK",
        })
    return pd.DataFrame(rows)[names(3)], true_comp


PRODUCTS = ["running shoes", "cleats", "a golf driver", "a baseball glove",
            "basketball shoes", "a yoga mat", "a hoodie", "a kayak paddle"]
CITIES = ["Springfield", "Riverside", "Fairview", "Madison", "Georgetown",
          "Franklin", "Clinton", "Arlington", "Salem", "Greenville"]
SUBREDDITS = {"dicks": ["DicksSportingGoods", "running", "baseball"],
              "house_of_sport": ["DicksSportingGoods", "climbing"],
              "golf_galaxy": ["golf"],
              "foot_locker": ["Sneakers", "footlocker"],
              "other": ["RunningShoeGeeks", "retail", ""]}
STORE_NAMES = {"dicks": "DICK'S Sporting Goods", "house_of_sport": "DICK'S House of Sport",
               "golf_galaxy": "Golf Galaxy", "foot_locker": "Foot Locker",
               "other": "Sports Outlet"}
BANNER_TEXT = {"dicks": "Dick's", "house_of_sport": "House of Sport",
               "golf_galaxy": "Golf Galaxy", "foot_locker": "Foot Locker",
               "other": "the outlet store"}
TOPIC_TEXT = {
    "availability": ["They were out of my size in {p}.", "Could not find {p} anywhere in the store."],
    "price_promo": ["Got {p} on sale for 30% off.", "Prices on {p} went up again."],
    "service_staff": ["Waited 20 minutes for someone to help with {p}.",
                      "The staff were really helpful picking {p}."],
    "fulfillment_returns": ["Ordered {p} for pickup and it was ready in an hour.",
                            "Returning {p} took forever."],
    "product_quality": ["The {p} fell apart after two weeks.",
                        "Really happy with the quality of {p}."],
    "store_experience": ["The new store layout is great.", "Store was messy and crowded."],
    "other": ["Just browsing today.", "Parking lot was full."],
}
INTENT_TEXT = {"up": " Will be back.", "flat": "", "down": " Not shopping here again."}


def iso_dt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def google_interval(day: date, scraped: date) -> tuple[date, date, str]:
    """Turn a true date into the interval a Google relative date ("3 months ago") gives,
    using the tasks/P1.md rules."""
    age = max((scraped - day).days, 1)
    if age < 7:
        return scraped - timedelta(days=age + 1), scraped - timedelta(days=age - 1), "week"
    if age < 30:
        n = age // 7
        return scraped - timedelta(days=(n + 1) * 7), scraped - timedelta(days=n * 7), "week"
    if age < 365:
        n = age // 30
        return scraped - relativedelta(months=n + 1), scraped - relativedelta(months=n), "month"
    n = age // 365
    return scraped - relativedelta(years=n + 1), scraped - relativedelta(years=n), "year"


def make_items(rng, quarters: pd.DataFrame, true_comp: np.ndarray) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Files 1 and 2. Each item has a hidden true banner, author, topic, and intent.
    The Laya-style probabilities are noisy versions of those."""
    start_ord = np.array([date.fromisoformat(d).toordinal() for d in quarters.period_start])
    first_day, scraped = date.fromisoformat(quarters.period_start.iloc[0]), SCRAPED_AT.date()
    span = (scraped - first_day).days
    tilt_by_q = (true_comp - 3.0) / 5.0  # above-average comps -> more "shop again" text

    def noisy(k: int, true: int, conc: float) -> np.ndarray:
        alpha = np.full(k, 0.6)
        alpha[true] += conc
        return rng.dirichlet(alpha)

    items, feats = [], []
    for i in range(N_ITEMS):
        # More recent items are more common.
        t = rng.random() if rng.random() < 0.4 else math.sqrt(rng.random())
        day = first_day + timedelta(days=int(t * span))
        tilt = tilt_by_q[np.searchsorted(start_ord, day.toordinal(), side="right") - 1]

        source = "reddit" if rng.random() < 0.4 else "google"
        banner = int(rng.choice(5, p=[0.55, 0.10, 0.10, 0.15, 0.10]))
        author = int(rng.choice(3, p=[0.80, 0.12, 0.08]))
        topic_p = np.array([0.18, 0.18, 0.18, 0.14, 0.12, 0.12, 0.08])
        topic_p[0] = max(0.03, topic_p[0] - 0.05 * tilt)
        topic = int(rng.choice(7, p=topic_p / topic_p.sum()))
        up = float(np.clip(0.35 + 0.12 * tilt, 0.05, 0.8))
        down = float(np.clip(0.25 - 0.12 * tilt, 0.05, 0.8))
        intent = int(rng.choice(3, p=[up, 1 - up - down, down]))
        relevant = rng.random() < 0.8

        b = BANNERS[banner]
        product = PRODUCTS[rng.integers(len(PRODUCTS))]
        if relevant:
            options = TOPIC_TEXT[TOPICS[topic]]
            body = (f"Went to {BANNER_TEXT[b]}. " + options[rng.integers(len(options))].format(p=product)
                    + INTENT_TEXT[INTENTS[intent]])
            title = f"{BANNER_TEXT[b]} visit"
        else:
            body = f"Anyone have a recommendation for {product}? Looking at a few brands."
            title = f"Question about {product}"

        url = f"https://www.example.com/mock/{source}/{i:05d}"
        if source == "reddit":
            text = f"{title}\n\n{body}"
            hint = SUBREDDITS[b][rng.integers(len(SUBREDDITS[b]))]
            latest = 15 * 3600 if day == scraped else 86400  # never after scraped_at
            created = datetime(day.year, day.month, day.day, tzinfo=timezone.utc) + \
                timedelta(seconds=int(rng.integers(latest)))
            low = high = day
            precision, created_s, stars = "exact", iso_dt(created), np.nan
        else:
            text = body
            hint = f"{STORE_NAMES[b]} - {CITIES[rng.integers(len(CITIES))]}"
            low, high, precision = google_interval(day, scraped)
            created_s = ""
            stars = float(rng.choice({0: [4, 5], 1: [3, 4, 5], 2: [1, 2, 3]}[intent]))

        item_id = f"{source}_{hashlib.sha256((url + chr(10) + text).encode('utf-8')).hexdigest()[:16]}"
        items.append({
            "item_id": item_id, "source": source, "banner_hint": hint, "text": text,
            "stars": stars, "created_exact": created_s, "date_low": low.isoformat(),
            "date_high": high.isoformat(), "date_precision": precision, "url": url,
            "scraped_at": iso_dt(SCRAPED_AT),
        })

        conc = 4 + 6 * rng.random()
        level = int(rng.choice([3, 4, 5])) if TOPICS[topic] == "price_promo" else (
            1 if rng.random() < 0.85 else 2)
        promo = noisy(5, level - 1, conc)
        nz = promo[promo > 0]
        row = {"item_id": item_id,
               "p_relevant": rng.beta(8, 2) if relevant else rng.beta(2, 8),
               "p_stockout": rng.beta(6, 2) if TOPICS[topic] == "availability" else rng.beta(1, 12),
               "promo_score_exp": float((np.arange(1, 6) * promo).sum()),
               "promo_entropy": float(-(nz * np.log(nz)).sum()),
               "model_version": "MOCK",
               "scored_at": iso_dt(SCORED_AT)}
        for group, true, k in [("banner", banner, 5), ("author", author, 3),
                               ("topic", topic, 7), ("intent", intent, 3)]:
            row.update(zip(GROUPS[group], noisy(k, true, conc)))
        feats.append(row)
    return pd.DataFrame(items)[names(1)], pd.DataFrame(feats)[names(2)]


def make_agreement(rng) -> dict:
    """File 9."""
    return {"n_items": 50, "model_version": "MOCK",
            "questions": [{"question": q, "n": 50,
                           "pct_agreement": round(float(rng.uniform(70, 92)), 1),
                           "cohen_kappa": round(float(rng.uniform(0.45, 0.80)), 3)}
                          for q in AGREEMENT_QUESTIONS]}


# ---------------------------------------------------------------- file 4 method

def shock(x: np.ndarray) -> np.ndarray:
    """CONTRACT.md file 4 step 10: value minus the mean of the non-missing values in the four
    prior quarters; needs the value and at least 2 prior values."""
    out = np.full(len(x), np.nan)
    for j in range(len(x)):
        prior = x[max(0, j - 4):j]
        prior = prior[~np.isnan(prior)]
        if not np.isnan(x[j]) and len(prior) >= 2:
            out[j] = x[j] - prior.mean()
    return out


def build_index(items: pd.DataFrame, feats: pd.DataFrame, quarters: pd.DataFrame) -> pd.DataFrame:
    """File 4 from files 1 to 3, following CONTRACT.md file 4 steps 1 to 11."""
    df = items.merge(feats, on="item_id", how="inner", validate="one_to_one")
    lo = np.array([date.fromisoformat(d).toordinal() for d in df.date_low])
    hi = np.array([date.fromisoformat(d).toordinal() for d in df.date_high])
    qs = np.array([date.fromisoformat(d).toordinal() for d in quarters.period_start])
    qe = np.array([date.fromisoformat(d).toordinal() for d in quarters.period_end])

    days = np.minimum(hi[:, None], qe[None, :]) - np.maximum(lo[:, None], qs[None, :]) + 1
    share = np.clip(days, 0, None) / (hi - lo + 1)[:, None]                # step 2
    weight = share * df.p_relevant.to_numpy()[:, None]                     # step 3
    banner = np.array(BANNERS)[df[GROUPS["banner"]].to_numpy().argmax(axis=1)]  # step 1

    net = (df.p_intent_up - df.p_intent_down).to_numpy()
    cust = df.p_author_customer.to_numpy()
    stock = df.p_stockout.to_numpy()
    promo = df.promo_score_exp.to_numpy()
    stars = pd.to_numeric(df.stars, errors="coerce").to_numpy()
    has_stars = (~np.isnan(stars)).astype(float)
    stars = np.nan_to_num(stars)

    data_end = max(date.fromisoformat(s[:10]) for s in items.scraped_at).toordinal()
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
    return out[names(4)]


# ---------------------------------------------------------------- files 5 to 8 method

def ols(y: np.ndarray, regressors: list[np.ndarray]):
    """OLS with an intercept and classical standard errors."""
    X = np.column_stack([np.ones(len(y))] + regressors)
    return sm.OLS(y, X).fit()


def series(index: pd.DataFrame, quarters: pd.DataFrame) -> dict[str, np.ndarray]:
    """Banner "all" columns aligned to the quarter order, plus comp and its one-quarter lag."""
    allq = index[index.banner == "all"].set_index("fiscal_quarter").loc[quarters.fiscal_quarter]
    comp = quarters.comp_pct.to_numpy(float)
    out = {c: allq[c].to_numpy(float) for c in
           ["intent_idx", "stockout_idx", "intent_shock", "stockout_shock", "stars_shock"]}
    out.update(comp=comp, lag=np.r_[np.nan, comp[:-1]], partial=allq.partial.to_numpy(bool))
    return out


def run_backtest(index: pd.DataFrame, quarters: pd.DataFrame) -> pd.DataFrame:
    """File 5: expanding-window out-of-sample forecasts."""
    x, qnames = series(index, quarters), list(quarters.fiscal_quarter)
    comp, lag, stars = x["comp"], x["lag"], x["stars_shock"]
    rows = []
    for sig_name in SIGNALS:
        sig = x[sig_name]
        elig = [j for j in range(len(qnames))
                if not (np.isnan(comp[j]) or np.isnan(lag[j]) or np.isnan(sig[j]))]
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
    return pd.DataFrame(rows, columns=names(5))


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
    return pd.DataFrame(rows, columns=names(7))


def num(v) -> float | None:
    """A JSON number, or null for missing."""
    return None if v is None or (isinstance(v, float) and math.isnan(v)) else round(float(v), 6)


def run_nowcast(index: pd.DataFrame, quarters: pd.DataFrame, metrics: pd.DataFrame) -> dict:
    """File 6."""
    x, qnames = series(index, quarters), list(quarters.fiscal_quarter)
    comp, lag, sig = x["comp"], x["lag"], x["intent_shock"]
    t = qnames.index(LAST_QUARTER)
    out = {k: None for k in names(6)}
    out.update(target_quarter=LAST_QUARTER, verdict="scenario")
    elig = np.array([j for j in range(len(qnames)) if j != t
                     and not (np.isnan(comp[j]) or np.isnan(lag[j]) or np.isnan(sig[j]))])
    if np.isnan(sig[t]) or np.isnan(lag[t]) or len(elig) < MIN_TRAIN:
        return out
    ar = ols(comp[elig], [lag[elig]]).params
    fit = ols(comp[elig], [lag[elig], sig[elig]])
    beta, beta_se = fit.params[2], fit.bse[2]
    pred_ar = ar[0] + ar[1] * lag[t]
    pred_laya = fit.params[0] + fit.params[1] * lag[t] + beta * sig[t]
    delta = (pred_laya - pred_ar) * 100
    half = Z80 * beta_se * abs(sig[t]) * 100
    mae = metrics.set_index("model").mae_bp
    beats_ar = bool(mae["ar_laya"] < mae["ar"])  # False when either is missing
    out.update(beta=num(beta), beta_se=num(beta_se), shock_current=num(sig[t]),
               pred_ar=num(pred_ar), pred_ar_laya=num(pred_laya), delta_comp_bp=num(delta),
               delta_comp_bp_lo80=num(delta - half), delta_comp_bp_hi80=num(delta + half),
               verdict="nowcast" if (delta - half > 0 or delta + half < 0) and beats_ar
               else "scenario")
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
    return pd.DataFrame(rows, columns=names(8))


# ---------------------------------------------------------------- writing

def write_csv(df: pd.DataFrame, number: int) -> None:
    path = ROOT / PATHS[number]
    path.parent.mkdir(parents=True, exist_ok=True)
    df.round(6).to_csv(path, index=False, lineterminator="\n")


def write_json(obj: dict, number: int) -> None:
    path = ROOT / PATHS[number]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def write_all() -> None:
    rng = np.random.default_rng(SEED)
    quarters, true_comp = make_quarters(rng)
    items, feats = make_items(rng, quarters, true_comp)
    index = build_index(items, feats, quarters)
    backtest = run_backtest(index, quarters)
    metrics = run_metrics(backtest)
    nowcast = run_nowcast(index, quarters, metrics)
    leadlag = run_leadlag(index, quarters)
    agreement = make_agreement(rng)
    for number, frame in [(1, items), (2, feats), (3, quarters), (4, index),
                          (5, backtest), (7, metrics), (8, leadlag)]:
        write_csv(frame, number)
    write_json(nowcast, 6)
    write_json(agreement, 9)
    print(f"Wrote 9 MOCK_ files (seed {SEED}). Mock verdict: {nowcast['verdict']}, "
          f"delta_comp_bp = {nowcast['delta_comp_bp']}.")


# ---------------------------------------------------------------- contract check

KIND_RE = {"int": r"-?\d+", "bool": r"True|False", "date": r"\d{4}-\d{2}-\d{2}",
           "datetime": r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", "quarter": r"FY\d{4}Q[1-4]"}
KIND_FMT = {"date": "%Y-%m-%d", "datetime": "%Y-%m-%dT%H:%M:%SZ"}


def contract_columns(number: int) -> list[str]:
    """Column names (or JSON keys) listed in CONTRACT.md for file `number`, in order."""
    text = CONTRACT.read_text(encoding="utf-8")
    section = re.search(rf"^## File {number}: .*?$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return re.findall(r"^\| `([^`]+)` \|", section.group(1), re.M) if section else []


def check_column(values: pd.Series, c: dict) -> list[str]:
    """Check one column of text values ("" = missing) against its spec."""
    name, kind, errs = c["name"], c["kind"], []
    empty = values == ""
    if empty.any() and not c["missing"]:
        errs.append(f"{name}: {int(empty.sum())} missing values where none are allowed")
    v = values[~empty]
    if v.empty or kind == "list":
        return errs

    def flag(bad: pd.Series, what: str) -> None:
        if bad.any():
            errs.append(f"{name}: {int(bad.sum())} values {what}, e.g. {v[bad].iloc[0]!r}")

    if kind in KIND_RE:
        bad = ~v.str.fullmatch(KIND_RE[kind])
        if kind in KIND_FMT:
            bad |= pd.to_datetime(v, format=KIND_FMT[kind], errors="coerce").isna()
        flag(bad, f"are not {kind}")
    if c["pattern"]:
        flag(~v.str.fullmatch(c["pattern"]), f"do not match {c['pattern']}")
    if c["allowed"] is not None:
        flag(~v.isin([str(a) for a in c["allowed"]]), f"are not in {c['allowed']}")
    if kind in ("float", "int"):
        x = pd.to_numeric(v, errors="coerce")
        flag(~np.isfinite(x.astype(float)), "are not finite numbers")
        if c["lo"] is not None:
            flag(x < c["lo"] - 1e-9, f"are below {c['lo']}")
        if c["hi"] is not None:
            flag(x > c["hi"] + 1e-9, f"are above {c['hi']}")
    return errs


def as_text(v) -> str:
    """A JSON value as the text a CSV cell would hold."""
    if v is None:
        return ""
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, list):
        return "list"
    return str(v)


def load(number: int) -> tuple[object, list[str], list[str]]:
    """Read one MOCK_ file. Returns (data, header in file order, schema errors)."""
    path = ROOT / PATHS[number]
    if not path.exists():
        return None, [], [f"missing file {PATHS[number]}"]
    if path.suffix == ".csv":
        df = pd.read_csv(path, dtype=str, keep_default_na=False)
        return df, list(df.columns), []
    obj = json.loads(path.read_text(encoding="utf-8"))
    header = list(obj)
    errs = []
    if number == 9:
        qs = obj.get("questions") or [{}]
        header += list(qs[0])
        if any(list(q) != QUESTION_KEYS for q in qs):
            errs.append(f"every question object needs keys {QUESTION_KEYS}")
    return obj, header, errs


def check_schema(number: int, data, header: list[str]) -> list[str]:
    expected = contract_columns(number)
    if names(number) != expected:
        return [f"mock.py spec is out of sync with CONTRACT.md: {names(number)} vs {expected}"]
    if header != expected:
        return [f"columns {header} differ from CONTRACT.md {expected}"]
    if isinstance(data, pd.DataFrame):
        frames = {c: data for c in expected}
    else:
        top = pd.DataFrame([{k: as_text(v) for k, v in data.items()}])
        qs = pd.DataFrame([{k: as_text(v) for k, v in q.items()} for q in data.get("questions", [])])
        frames = {c: (qs if number == 9 and c in QUESTION_KEYS else top) for c in expected}
    errs = []
    for c in SPECS[number]:
        errs += check_column(frames[c["name"]][c["name"]], c)
    return errs


def cross_checks(f: dict) -> dict[int, list[str]]:
    """Rules that span rows or files (CONTRACT.md text plus the mock settings)."""
    e = {n: [] for n in PATHS}
    items, feats, qtr, idx, bt, now, met, ll, agr = (f[n] for n in range(1, 10))
    qnames = [q for q, _, _ in mock_calendar()]
    pos = {q: j for j, q in enumerate(qnames)}

    if len(items) != N_ITEMS:
        e[1].append(f"{len(items)} rows, expected {N_ITEMS}")
    if items.item_id.duplicated().any():
        e[1].append("item_id is not unique")
    if (items.date_low > items.date_high).any():
        e[1].append("date_low after date_high")
    red, goo = items[items.source == "reddit"], items[items.source == "google"]
    if (red.stars != "").any() or (red.created_exact == "").any() or (red.date_precision != "exact").any():
        e[1].append("Reddit rows need created_exact, no stars, precision exact")
    if (goo.created_exact != "").any() or (goo.date_precision == "exact").any():
        e[1].append("Google rows need empty created_exact and a non-exact precision")

    if feats.item_id.duplicated().any():
        e[2].append("item_id is not unique")
    if set(feats.item_id) != set(items.item_id):
        e[2].append("item_ids do not match MOCK_items.csv")
    for group, cols in GROUPS.items():
        if ((feats[cols].astype(float).sum(axis=1) - 1).abs() > 0.001).any():
            e[2].append(f"{group} probabilities do not sum to 1")

    if list(qtr.fiscal_quarter) != qnames:
        e[3].append(f"quarters must run {qnames[0]} to {qnames[-1]} in order")
    starts, ends = pd.to_datetime(qtr.period_start), pd.to_datetime(qtr.period_end)
    if ((ends.iloc[:-1].to_numpy() + np.timedelta64(1, "D")) != starts.iloc[1:].to_numpy()).any():
        e[3].append("quarters are not contiguous")
    reported = qtr[qtr.fiscal_quarter != LAST_QUARTER]
    if (reported.comp_pct == "").any():
        e[3].append("a reported quarter has no comp_pct")
    else:
        comp = reported.comp_pct.astype(float)
        if ((comp < -5) | (comp > 12)).any():
            e[3].append("mock comp_pct outside -5 to +12")
    last = qtr[qtr.fiscal_quarter == LAST_QUARTER].iloc[0]
    if any(last[c] != "" for c in ["report_date", "comp_pct", "comp_fl_pct",
                                    "net_sales_musd", "gross_margin_pct"]):
        e[3].append(f"{LAST_QUARTER} is in progress; its results must be empty")
    if (qtr.loc[qtr.fiscal_quarter < FL_FIRST_QUARTER, "comp_fl_pct"] != "").any():
        e[3].append(f"comp_fl_pct filled before {FL_FIRST_QUARTER} (mock assumption)")

    if list(zip(idx.fiscal_quarter, idx.banner)) != [(q, b) for q in qnames for b in INDEX_BANNERS]:
        e[4].append("rows must be every quarter x banner, sorted by quarter then banner order")
    low = idx.n_effective.astype(float) < MIN_N_EFFECTIVE
    if (idx.loc[low, [f"{n}_idx" for n in INDEX_NAMES]] != "").any().any():
        e[4].append(f"an index is filled where n_effective < {MIN_N_EFFECTIVE}")
    if set(idx.loc[idx.partial == "True", "fiscal_quarter"]) != {LAST_QUARTER}:
        e[4].append(f"only {LAST_QUARTER} should be partial")

    if set(bt.signal_used) != set(SIGNALS):
        e[5].append(f"signal_used must cover {SIGNALS}")
    if any(pos[t] >= pos[q] for q, t in zip(bt.fiscal_quarter, bt.train_end_quarter)):
        e[5].append("train_end_quarter must be before the forecast quarter")

    if now["target_quarter"] != LAST_QUARTER:
        e[6].append(f"target_quarter must be {LAST_QUARTER}")
    if now["delta_comp_bp"] is not None and not (
            now["delta_comp_bp_lo80"] <= now["delta_comp_bp"] <= now["delta_comp_bp_hi80"]):
        e[6].append("delta_comp_bp is outside its own 80% interval")

    if list(met.model) != MODELS:
        e[7].append(f"models must be {MODELS} in order")

    if list(zip(ll.signal, ll.lag)) != [(s, str(g)) for s in LEADLAG_SIGNALS for g in (-1, 0, 1)]:
        e[8].append("rows must be each signal with lag -1, 0, 1 in order")

    if [q["question"] for q in agr["questions"]] != AGREEMENT_QUESTIONS:
        e[9].append(f"questions must be {AGREEMENT_QUESTIONS} in order")
    return e


def check_all() -> bool:
    """Print PASS or FAIL per MOCK_ file. Returns True when every file passes."""
    data, errors = {}, {}
    for number in PATHS:
        obj, header, errs = load(number)
        if obj is not None and not errs:
            errs = check_schema(number, obj, header)
        data[number], errors[number] = obj, errs
    if not any(errors.values()):
        errors = cross_checks(data)
    else:
        print("Cross-file checks skipped until every file passes its schema check.")
    for number, rel in PATHS.items():
        obj = data[number]
        size = f"{len(obj)} rows" if isinstance(obj, pd.DataFrame) else ("1 object" if obj else "")
        print(f"{'FAIL' if errors[number] else 'PASS'}  file {number}  {rel}  {size}")
        for err in errors[number]:
            print(f"      - {err}")
    ok = not any(errors.values())
    print("Contract check: all MOCK_ files match CONTRACT.md." if ok else "Contract check FAILED.")
    return ok


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write and check MOCK_ contract files.")
    parser.add_argument("--check", action="store_true",
                        help="only check the existing MOCK_ files; write nothing")
    args = parser.parse_args(argv)
    if not args.check:
        write_all()
    return 0 if check_all() else 1


if __name__ == "__main__":
    sys.exit(main())
