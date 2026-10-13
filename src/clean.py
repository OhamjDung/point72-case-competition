"""Clean raw scraper output into data/clean/items.csv (CONTRACT.md file 1).

Usage, from the project root:
    python src/clean.py
    python src/clean.py --drop-source google      Reddit only (see docs/compliance.md)
    python src/clean.py --reddit data/raw/reddit/documents.csv --reviews data/raw/reviews/documents.csv

Inputs are the `scraping` branch exports (`scraping/data/exports/documents.csv` and
`scraping/data/exports_reviews/documents.csv`) copied into data/raw/ (gitignored, never commit).
Outputs: data/clean/items.csv and data/clean/coverage_report.csv.

Owner: P1. Rules are tasks/P1.md step 3 and CONTRACT.md file 1. Python 3.10+.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

import pandas as pd
from dateutil.relativedelta import relativedelta

ROOT = Path(__file__).resolve().parents[1]

COLUMNS = ["item_id", "source", "banner_hint", "text", "stars", "created_exact",
           "date_low", "date_high", "date_precision", "url", "scraped_at"]
# scraping/export.py prefixes "'" to text starting with these, to stop spreadsheet formulas.
FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")
BANNER_WORDS = re.compile(r"dick'?s|house of sport|golf galaxy|foot ?locker", re.I)
FL_STORE = re.compile(r"foot ?locker|champs", re.I)
EDITED = re.compile(r"^\s*\(?edited\)?\s*[:\-]?\s*", re.I)
RELATIVE = re.compile(r"^(a|an|\d+)\s+(day|week|month|year)s?\s+ago$", re.I)
# First day of FY2021Q1, the first quarter in dks_quarters.csv. Items that end before it cannot
# fall in any quarter, so scoring them would only cost Laya time.
WINDOW_START = pd.Timestamp("2021-01-31")


def unguard(value: str) -> str:
    if value.startswith("'") and value[1:].startswith(FORMULA_PREFIXES):
        return value[1:]
    return value


def iso_utc(ts: pd.Timestamp) -> str:
    return ts.tz_convert("UTC").strftime("%Y-%m-%dT%H:%M:%SZ")


def relative_interval(phrase: str, scraped: pd.Timestamp) -> tuple[pd.Timestamp, pd.Timestamp, str] | None:
    """Turn "3 weeks ago" into (date_low, date_high, precision) per CONTRACT.md file 1."""
    m = RELATIVE.match(phrase.strip())
    if not m:
        return None
    n = 1 if m.group(1).lower() in ("a", "an") else int(m.group(1))
    unit = m.group(2).lower()
    day = scraped.normalize()
    if unit == "day":
        return day - pd.Timedelta(days=n + 1), day - pd.Timedelta(days=n - 1), "week"
    if unit == "week":
        return day - pd.Timedelta(days=(n + 1) * 7), day - pd.Timedelta(days=n * 7), "week"
    step = relativedelta(months=1) if unit == "month" else relativedelta(years=1)
    precision = "month" if unit == "month" else "year"
    return day - step * (n + 1), day - step * n, precision


def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8-sig", dtype=str, keep_default_na=False)
    print(f"{path}: {len(df)} rows; columns: {', '.join(df.columns)}")
    return df


def keep_mask(df: pd.DataFrame) -> pd.Series:
    """CONTRACT.md file 1, "Which documents are items"."""
    mentions = df["company_mentions"].str.split(";")
    mentions_dks_fl = mentions.apply(lambda xs: "DKS" in xs or "FL" in xs)
    fl_store = (df["platform"] != "reddit") & df["banner"].str.contains(FL_STORE)
    return (df["cohort"] == "dks") | mentions_dks_fl | fl_store


def banner_hint(row: pd.Series) -> str:
    if row["platform"] == "reddit":
        flair = row["link_flair"]
        return flair if BANNER_WORDS.search(flair) else row["community"]
    return " - ".join(p for p in (row["banner"], row["city"]) if p)


def to_items(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)
    out["source"] = df["platform"].map(lambda p: "reddit" if p == "reddit" else "google")
    out["banner_hint"] = df.apply(banner_hint, axis=1)
    is_google = out["source"] == "google"
    text = df["text"].map(unguard)
    text[is_google] = text[is_google].str.replace(EDITED, "", n=1, regex=True)
    out["text"] = text.str.strip()
    out["stars"] = pd.to_numeric(df["rating"].where(is_google, ""), errors="coerce")
    out["url"] = df["url"].map(unguard)
    scraped = pd.to_datetime(df["first_collected_at"], utc=True, format="ISO8601")
    out["scraped_at"] = scraped.map(iso_utc)

    created = pd.to_datetime(df["created_at"].where(df["created_at"] != ""), utc=True,
                             format="ISO8601")
    out["created_exact"] = created.map(lambda t: "" if pd.isna(t) else iso_utc(t))
    low, high, precision = [], [], []
    for c, s, raw in zip(created, scraped, df["created_at"]):
        if not pd.isna(c):
            d = c.tz_convert("UTC").normalize().tz_localize(None)
            low.append(d)
            high.append(d)
            precision.append("exact")
            continue
        parsed = relative_interval(raw, s.tz_convert("UTC").tz_localize(None))
        if parsed is None:  # no usable date: the caller drops it
            parsed = (pd.NaT, pd.NaT, "")
        low.append(parsed[0])
        high.append(parsed[1])
        precision.append(parsed[2])
    out["date_low"] = pd.to_datetime(pd.Series(low, index=df.index))
    out["date_high"] = pd.to_datetime(pd.Series(high, index=df.index))
    out["date_precision"] = precision
    out["item_id"] = [
        f"{src}_{hashlib.sha256((u + chr(10) + t).encode('utf-8')).hexdigest()[:16]}"
        for src, u, t in zip(out["source"], out["url"], out["text"])
    ]
    return out


def near_key(text: str) -> str:
    return re.sub(r"[\W_]+", "", text.lower())


def coverage_report(items: pd.DataFrame) -> pd.DataFrame:
    q = items["date_low"].dt.to_period("Q").astype(str)
    return (items.assign(calendar_quarter=q)
            .groupby(["calendar_quarter", "source", "date_precision"]).size()
            .rename("n_items").reset_index())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Clean scraper exports into data/clean/items.csv")
    ap.add_argument("--reddit", default=str(ROOT / "data/raw/reddit/documents.csv"))
    ap.add_argument("--reviews", default=str(ROOT / "data/raw/reviews/documents.csv"))
    ap.add_argument("--out", default=str(ROOT / "data/clean/items.csv"))
    ap.add_argument("--drop-source", choices=["reddit", "google"], action="append", default=[],
                    help="exclude a source (docs/compliance.md recommends excluding google)")
    args = ap.parse_args(argv)

    raw = pd.concat([load(Path(args.reddit)), load(Path(args.reviews))], ignore_index=True)
    print(f"rows in: {len(raw)}")

    def step(df: pd.DataFrame, mask: pd.Series, rule: str) -> pd.DataFrame:
        print(f"  dropped {int((~mask).sum()):>7} : {rule}")
        return df[mask]

    raw = step(raw, keep_mask(raw), "not DKS cohort, no DKS/FL mention, not a Foot Locker/Champs store")
    items = to_items(raw)
    items = step(items, ~items["source"].isin(args.drop_source),
                 f"source excluded by --drop-source {args.drop_source}")
    items = step(items, items["text"] != "", "empty text")
    items = step(items, items["date_low"].notna(), "no usable date")
    items = step(items, items["date_high"] >= WINDOW_START,
                 f"written before FY2021Q1 starts ({WINDOW_START.date()})")
    # Keep the earliest copy of each duplicate.
    items = items.sort_values(["date_low", "item_id"], kind="stable")
    items = step(items, ~items["item_id"].duplicated(), "exact duplicate (same url + text)")
    items = step(items, ~items["text"].map(near_key).duplicated(),
                 "duplicate or near-duplicate text (same after lowercasing, removing punctuation and whitespace)")
    print(f"rows out: {len(items)}")

    report = coverage_report(items)
    out = items[COLUMNS].copy()
    for col in ("date_low", "date_high"):
        out[col] = out[col].dt.strftime("%Y-%m-%d")
    out = out.sort_values("item_id").reset_index(drop=True)
    assert out["item_id"].is_unique
    assert out["item_id"].str.fullmatch(r"(reddit|google)_[0-9a-f]{16}").all()
    assert (out["date_low"] <= out["date_high"]).all() and (out["text"] != "").all()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_path, index=False, encoding="utf-8")
    report.to_csv(out_path.parent / "coverage_report.csv", index=False, encoding="utf-8")
    print(f"wrote {out_path} ({len(out)} rows, {out_path.stat().st_size / 1e6:.1f} MB) "
          "and coverage_report.csv")

    for src, g in items.groupby("source"):
        print(f"{src}: {len(g)} items, date_low {g['date_low'].min().date()} "
              f"to {g['date_low'].max().date()}")
    google = items[items["source"] == "google"]
    if len(google):
        print(f"google share with precision 'year': {(google['date_precision'] == 'year').mean():.1%}")
    print(items.groupby(["source", "banner_hint"]).size().sort_values(ascending=False)
          .head(10).to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
