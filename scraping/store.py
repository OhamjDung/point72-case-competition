from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import Literal

from scraping.schema import Document, Store, StoreSnapshot

SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
    doc_id TEXT PRIMARY KEY, platform TEXT NOT NULL, doc_type TEXT NOT NULL,
    cohort TEXT NOT NULL, community TEXT, store_id TEXT, thread_id TEXT, parent_id TEXT,
    title TEXT, body TEXT, rating REAL, score INTEGER, num_comments INTEGER,
    created_at TEXT NOT NULL, first_collected_at TEXT NOT NULL, last_collected_at TEXT NOT NULL,
    author_hash TEXT, author_flair TEXT, link_flair TEXT, url TEXT,
    is_deleted INTEGER NOT NULL, edited INTEGER NOT NULL, company_mentions TEXT NOT NULL,
    source_listings TEXT NOT NULL, content_hash TEXT
);
CREATE TABLE IF NOT EXISTS document_versions (
    doc_id TEXT, collected_at TEXT, content_hash TEXT, title TEXT, body TEXT,
    PRIMARY KEY (doc_id, content_hash)
);
CREATE TABLE IF NOT EXISTS stores (
    store_id TEXT PRIMARY KEY, banner TEXT, company TEXT, cohort TEXT, priority INTEGER,
    name TEXT, address TEXT, city TEXT, state TEXT, postal_code TEXT, lat REAL, lng REAL,
    discovery_query TEXT, discovered_at TEXT
);
CREATE TABLE IF NOT EXISTS store_snapshots (
    store_id TEXT, collected_at TEXT, rating REAL, user_rating_count INTEGER,
    business_status TEXT, PRIMARY KEY (store_id, collected_at)
);
CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY, kind TEXT, started_at TEXT, finished_at TEXT,
    params TEXT, counts TEXT, status TEXT
);
"""

DOC_COLUMNS = (
    "doc_id", "platform", "doc_type", "cohort", "community", "store_id", "thread_id",
    "parent_id", "title", "body", "rating", "score", "num_comments", "created_at",
    "first_collected_at", "last_collected_at", "author_hash", "author_flair", "link_flair",
    "url", "is_deleted", "edited", "company_mentions", "source_listings", "content_hash",
)
INSERT_DOC = (
    f"INSERT INTO documents ({', '.join(DOC_COLUMNS)}) "
    f"VALUES ({', '.join(':' + c for c in DOC_COLUMNS)})"
)
INSERT_VERSION = "INSERT OR IGNORE INTO document_versions VALUES (?, ?, ?, ?, ?)"
STORE_COLUMNS = tuple(Store.model_fields)

Outcome = Literal["inserted", "updated", "unchanged", "deleted"]


def connect(path: str | Path) -> sqlite3.Connection:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def content_hash(title: str | None, body: str | None) -> str:
    return hashlib.sha256(f"{title or ''}\x1f{body or ''}".encode()).hexdigest()


def purge_document(conn: sqlite3.Connection, doc_id: str, collected_at: datetime) -> None:
    """Drop stored text, author hash and edit history for content its author deleted."""
    conn.execute(
        "UPDATE documents SET is_deleted = 1, title = NULL, body = NULL, "
        "author_hash = NULL, content_hash = NULL, company_mentions = '[]', "
        "last_collected_at = ? WHERE doc_id = ?",
        (collected_at.isoformat(), doc_id),
    )
    conn.execute("DELETE FROM document_versions WHERE doc_id = ?", (doc_id,))


def upsert_document(conn: sqlite3.Connection, doc: Document) -> Outcome:
    now = doc.collected_at.isoformat()
    row = conn.execute("SELECT * FROM documents WHERE doc_id = ?", (doc.doc_id,)).fetchone()
    if doc.is_deleted or (row is not None and row["is_deleted"]):
        if row is not None and not row["is_deleted"]:
            purge_document(conn, doc.doc_id, doc.collected_at)
        return "deleted"
    digest = content_hash(doc.title, doc.body)
    if row is None:
        values = doc.model_dump(exclude={"collected_at", "source_listings"})
        values.update(
            created_at=doc.created_at.isoformat(), first_collected_at=now, last_collected_at=now,
            is_deleted=0, edited=int(doc.edited),
            company_mentions=json.dumps(sorted(doc.company_mentions)),
            source_listings=json.dumps(sorted(set(doc.source_listings))), content_hash=digest,
        )
        conn.execute(INSERT_DOC, values)
        conn.execute(INSERT_VERSION, (doc.doc_id, now, digest, doc.title, doc.body))
        return "inserted"
    listings = sorted(set(json.loads(row["source_listings"])) | set(doc.source_listings))
    changed = digest != row["content_hash"]
    conn.execute(
        "UPDATE documents SET title = ?, body = ?, content_hash = ?, rating = ?, score = ?, "
        "num_comments = ?, last_collected_at = ?, source_listings = ?, company_mentions = ?, "
        "edited = ? WHERE doc_id = ?",
        (
            doc.title, doc.body, digest, doc.rating, doc.score, doc.num_comments, now,
            json.dumps(listings), json.dumps(sorted(doc.company_mentions)),
            int(changed or doc.edited or bool(row["edited"])), doc.doc_id,
        ),
    )
    if changed:
        conn.execute(INSERT_VERSION, (doc.doc_id, now, digest, doc.title, doc.body))
    return "updated" if changed else "unchanged"


def get_num_comments(conn: sqlite3.Connection, doc_id: str) -> int | None:
    row = conn.execute("SELECT num_comments FROM documents WHERE doc_id = ?", (doc_id,)).fetchone()
    return None if row is None else row[0]


def upsert_store(conn: sqlite3.Connection, store: Store) -> None:
    data = store.model_dump()
    data["discovered_at"] = store.discovered_at.isoformat()
    updates = ", ".join(
        f"{c} = excluded.{c}" for c in STORE_COLUMNS if c not in ("store_id", "discovered_at")
    )
    conn.execute(
        f"INSERT INTO stores ({', '.join(STORE_COLUMNS)}) "
        f"VALUES ({', '.join(':' + c for c in STORE_COLUMNS)}) "
        f"ON CONFLICT(store_id) DO UPDATE SET {updates}",
        data,
    )


def _store(row: sqlite3.Row) -> Store:
    return Store(**{c: row[c] for c in STORE_COLUMNS})


def get_store(conn: sqlite3.Connection, store_id: str) -> Store | None:
    row = conn.execute("SELECT * FROM stores WHERE store_id = ?", (store_id,)).fetchone()
    return None if row is None else _store(row)


def stores_for_reviews(conn: sqlite3.Connection, limit: int) -> list[Store]:
    """Never-fetched stores first, then stalest snapshot, then config priority."""
    rows = conn.execute(
        "SELECT stores.*, (SELECT MAX(collected_at) FROM store_snapshots s "
        "WHERE s.store_id = stores.store_id) AS last_snap FROM stores "
        "ORDER BY last_snap IS NOT NULL, last_snap, priority, store_id LIMIT ?",
        (limit,),
    ).fetchall()
    return [_store(r) for r in rows]


def add_snapshot(conn: sqlite3.Connection, snap: StoreSnapshot) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO store_snapshots VALUES (?, ?, ?, ?, ?)",
        (snap.store_id, snap.collected_at.isoformat(), snap.rating, snap.user_rating_count,
         snap.business_status),
    )


def record_run(
    conn: sqlite3.Connection, kind: str, started: datetime, finished: datetime,
    params: dict, counts: dict, status: str,
) -> str:
    run_id = uuid.uuid4().hex
    conn.execute(
        "INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?, ?)",
        (run_id, kind, started.isoformat(), finished.isoformat(), json.dumps(params),
         json.dumps(counts, default=str), status),
    )
    conn.commit()
    return run_id
