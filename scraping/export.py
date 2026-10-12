from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd

PLATFORM_PREFERENCE = {"google_maps": 0, "apify_google_maps": 1, "reddit": 2}
VOICE = {"review": "customer_review", "post": "reddit_post", "comment": "reddit_comment"}
EXPORT_COLUMNS = [
    "doc_id", "platform", "doc_type", "voice", "cohort", "community", "store_id", "banner",
    "company", "state", "city", "created_at", "fiscal_quarter_approx", "text", "char_len",
    "rating", "score", "num_comments", "author_hash", "author_flair", "link_flair",
    "company_mentions", "thread_id", "parent_id", "url", "first_collected_at",
]


FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


def _csv_safe(frame: pd.DataFrame) -> pd.DataFrame:
    """Prefix untrusted text that Excel/Sheets would evaluate as a formula."""
    safe = frame.copy()
    for column in safe.columns:  # pandas 3 stores text as "str", not object dtype
        safe[column] = safe[column].map(
            lambda v: f"'{v}" if isinstance(v, str) and v.startswith(FORMULA_PREFIXES) else v
        )
    return safe


def fiscal_quarter_approx(ts: datetime) -> str:
    """DKS fiscal year starts in February, labelled by its starting calendar year."""
    year = ts.year if ts.month >= 2 else ts.year - 1
    return f"FY{year} Q{((ts.month - 2) % 12) // 3 + 1}"


def export_all(conn: sqlite3.Connection, out_dir: str | Path) -> dict:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    docs = pd.read_sql_query(
        "SELECT d.*, s.banner, s.company, s.state, s.city FROM documents d "
        "LEFT JOIN stores s ON s.store_id = d.store_id WHERE d.is_deleted = 0",
        conn,
    )
    docs["text"] = (docs["title"].fillna("") + "\n\n" + docs["body"].fillna("")).str.strip()
    docs = docs[(docs["text"] != "") | docs["rating"].notna()].copy()
    created = pd.to_datetime(docs["created_at"], utc=True, format="ISO8601")
    docs["char_len"] = docs["text"].str.len()
    docs["fiscal_quarter_approx"] = [fiscal_quarter_approx(t) for t in created]
    docs["voice"] = docs["doc_type"].map(VOICE)
    docs["company_mentions"] = docs["company_mentions"].map(lambda s: ";".join(json.loads(s)))
    docs["_pref"] = docs["platform"].map(PLATFORM_PREFERENCE)
    docs["_day"] = created.dt.date
    is_review = docs["doc_type"] == "review"
    reviews = docs[is_review].sort_values("_pref").drop_duplicates(
        subset=["store_id", "_day", "text", "rating"]
    )
    docs = pd.concat([reviews, docs[~is_review]]).sort_values("created_at")
    _csv_safe(docs[EXPORT_COLUMNS]).to_csv(out / "documents.csv", index=False, encoding="utf-8-sig")
    stores = pd.read_sql_query("SELECT * FROM stores", conn)
    _csv_safe(stores).to_csv(out / "stores.csv", index=False, encoding="utf-8-sig")
    snaps = pd.read_sql_query("SELECT * FROM store_snapshots", conn)
    snaps.to_csv(out / "store_snapshots.csv", index=False, encoding="utf-8-sig")
    return {"documents": len(docs), "stores": len(stores), "snapshots": len(snaps),
            "output": str(out.resolve())}


def status(conn: sqlite3.Connection) -> dict:
    documents = [dict(r) for r in conn.execute(
        "SELECT platform, cohort, community, COUNT(*) AS n, MIN(created_at) AS oldest, "
        "MAX(created_at) AS newest FROM documents WHERE is_deleted = 0 "
        "GROUP BY platform, cohort, community ORDER BY platform, cohort, community"
    )]
    stores = [dict(r) for r in conn.execute(
        "SELECT banner, company, COUNT(*) AS n FROM stores GROUP BY banner, company"
    )]
    snapshots = conn.execute("SELECT COUNT(*) FROM store_snapshots").fetchone()[0]
    return {"documents": documents, "stores": stores, "snapshots": snapshots}
