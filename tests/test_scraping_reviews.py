from datetime import UTC, datetime

import httpx

from scraping.places import PlacesClient
from scraping.reviews import fetch_reviews, parse_rfc3339
from scraping.schema import Store
from scraping.store import connect, upsert_store

T0 = datetime(2026, 10, 1, tzinfo=UTC)
T1 = datetime(2026, 11, 1, tzinfo=UTC)


def seed_store(conn, sid, priority=0):
    upsert_store(conn, Store(
        store_id=sid, banner="DICK'S Sporting Goods", company="DKS", cohort="dks",
        priority=priority, name="DICK'S Sporting Goods", address=None, city="Dallas",
        state="TX", postal_code=None, lat=None, lng=None, discovery_query="q",
        discovered_at=T0,
    ))
    conn.commit()


def details_handler(request):
    sid = request.url.path.rsplit("/", 1)[-1]
    return httpx.Response(200, json={
        "id": sid, "rating": 4.2, "userRatingCount": 1500, "businessStatus": "OPERATIONAL",
        "reviews": [{
            "name": f"places/{sid}/reviews/r1", "rating": 2,
            "text": {"text": "Long checkout lines, shelves empty", "languageCode": "en"},
            "publishTime": "2026-09-01T18:22:31.123456789Z",
            "authorAttribution": {"displayName": "Jane D"},
            "googleMapsUri": "https://maps.google.com/x",
        }],
    })


def client():
    return PlacesClient(api_key="k", transport=httpx.MockTransport(details_handler))


def test_parse_rfc3339_truncates_nanoseconds():
    assert parse_rfc3339("2026-09-01T18:22:31.123456789Z") == datetime(
        2026, 9, 1, 18, 22, 31, 123456, tzinfo=UTC
    )
    assert parse_rfc3339("2026-09-01T18:22:31Z") == datetime(2026, 9, 1, 18, 22, 31, tzinfo=UTC)


def test_reviews_keep_store_attribution_and_snapshot(tmp_path):
    conn = connect(tmp_path / "s.sqlite")
    seed_store(conn, "s1")
    counts = fetch_reviews(client(), conn, limit=10, salt="salt", now=T1)
    assert counts["inserted"] == 1
    doc = conn.execute("SELECT * FROM documents").fetchone()
    assert (doc["store_id"], doc["cohort"], doc["rating"], doc["doc_type"]) == (
        "s1", "dks", 2.0, "review",
    )
    assert doc["created_at"] == "2026-09-01T18:22:31.123456+00:00"
    snap = conn.execute("SELECT * FROM store_snapshots").fetchone()
    assert (snap["rating"], snap["user_rating_count"]) == (4.2, 1500)


def test_call_cap_and_rotation(tmp_path):
    conn = connect(tmp_path / "s.sqlite")
    for i, sid in enumerate(["a", "b", "c"]):
        seed_store(conn, sid, priority=i)
    c = client()
    fetch_reviews(c, conn, limit=2, salt="s", now=T0)
    assert c.calls["details"] == 2
    fetch_reviews(c, conn, limit=2, salt="s", now=T1)
    order = [r[0] for r in conn.execute(
        "SELECT store_id FROM store_snapshots WHERE collected_at = ? ORDER BY rowid",
        (T1.isoformat(),),
    )]
    assert order == ["c", "a"]
