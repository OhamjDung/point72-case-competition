import json
from datetime import UTC, datetime

import pytest

from scraping.schema import Document, Store
from scraping.store import connect, get_store, upsert_document, upsert_store

T0 = datetime(2026, 10, 1, tzinfo=UTC)
T1 = datetime(2026, 10, 2, tzinfo=UTC)


def doc(**overrides):
    base = dict(
        doc_id="reddit:t3_a", platform="reddit", doc_type="post", cohort="dks",
        community="dickssportinggoods", title="Inventory", body="Too much stock",
        created_at=T0, collected_at=T0, source_listings=["new"],
    )
    base.update(overrides)
    return Document(**base)


def test_insert_then_unchanged_keeps_first_collected(tmp_path):
    conn = connect(tmp_path / "s.sqlite")
    assert upsert_document(conn, doc()) == "inserted"
    assert upsert_document(conn, doc(collected_at=T1, source_listings=["top:all"])) == "unchanged"
    row = conn.execute("SELECT * FROM documents").fetchone()
    assert row["first_collected_at"] == T0.isoformat()
    assert row["last_collected_at"] == T1.isoformat()
    assert json.loads(row["source_listings"]) == ["new", "top:all"]
    assert conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0] == 1


def test_edit_creates_version(tmp_path):
    conn = connect(tmp_path / "s.sqlite")
    upsert_document(conn, doc())
    assert upsert_document(conn, doc(body="edited", collected_at=T1)) == "updated"
    assert conn.execute("SELECT COUNT(*) FROM document_versions").fetchone()[0] == 2
    assert tuple(conn.execute("SELECT edited, body FROM documents").fetchone()) == (1, "edited")


def test_deletion_purges_text_and_versions(tmp_path):
    conn = connect(tmp_path / "s.sqlite")
    upsert_document(conn, doc(author_hash="abc"))
    gone = doc(is_deleted=True, title=None, body=None, collected_at=T1)
    assert upsert_document(conn, gone) == "deleted"
    row = conn.execute("SELECT * FROM documents").fetchone()
    assert (row["title"], row["body"], row["author_hash"], row["is_deleted"]) == (None, None, None, 1)
    assert conn.execute("SELECT COUNT(*) FROM document_versions").fetchone()[0] == 0
    assert upsert_document(conn, doc(collected_at=T1)) == "deleted"  # stays purged


def test_unseen_deleted_doc_is_not_stored(tmp_path):
    conn = connect(tmp_path / "s.sqlite")
    assert upsert_document(conn, doc(is_deleted=True, title=None, body=None)) == "deleted"
    assert conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0] == 0


def test_naive_timestamp_rejected():
    with pytest.raises(ValueError):
        doc(created_at=datetime(2026, 1, 1))


def test_store_upsert_keeps_discovered_at(tmp_path):
    conn = connect(tmp_path / "s.sqlite")
    base = dict(
        store_id="p1", banner="DICK'S Sporting Goods", company="DKS", cohort="dks", priority=0,
        name="DICK'S Sporting Goods", address=None, city="Dallas", state="TX", postal_code=None,
        lat=None, lng=None, discovery_query="q",
    )
    upsert_store(conn, Store(discovered_at=T0, **base))
    upsert_store(conn, Store(discovered_at=T1, **{**base, "name": "DICK'S House of Sport"}))
    store = get_store(conn, "p1")
    assert store is not None
    assert (store.name, store.discovered_at) == ("DICK'S House of Sport", T0)
