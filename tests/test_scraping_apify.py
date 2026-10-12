from datetime import UTC, datetime

from scraping.apify import import_apify
from scraping.places import Banner
from scraping.store import connect, get_store

T1 = datetime(2026, 10, 2, tzinfo=UTC)
DKS = Banner(
    banner="DICK'S Sporting Goods", company="DKS", cohort="dks", query="DICK'S Sporting Goods",
    name_regex=r"^dick'?s sporting goods", priority=0,
)


def test_apify_import_attributes_store_and_skips_bad_rows(tmp_path):
    conn = connect(tmp_path / "s.sqlite")
    rows = [
        {"reviewId": "x1", "placeId": "pA", "title": "DICK'S Sporting Goods",
         "address": "1 Main St, Plano, TX", "city": "Plano", "state": "Texas",
         "postalCode": "75024", "text": "Great staff", "stars": 5,
         "publishedAtDate": "2025-03-02T10:00:00.000Z", "name": "Bob"},
        {"reviewId": "x2", "placeId": "pB", "title": "Joe's Bait Shop", "text": "ok",
         "stars": 3, "publishedAtDate": "2025-03-02T10:00:00.000Z"},
        {"reviewId": "x3", "placeId": "pA", "title": "DICK'S Sporting Goods",
         "text": "no date", "stars": 1},
    ]
    counts = import_apify(conn, rows, [DKS], collected_at=T1, salt="s")
    assert counts == {
        "inserted": 1, "updated": 0, "unchanged": 0, "deleted": 0,
        "skipped_missing_fields": 1, "skipped_unknown_store": 1, "stores_created": 1,
    }
    store = get_store(conn, "pA")
    assert store is not None and (store.state, store.city) == ("TX", "Plano")
    doc = conn.execute("SELECT * FROM documents").fetchone()
    assert (doc["doc_id"], doc["store_id"], doc["rating"]) == ("apify_gmaps:x1", "pA", 5.0)
