import json
from datetime import UTC, datetime

import pandas as pd
import pytest

from scraping.cli import main
from scraping.export import export_all, fiscal_quarter_approx
from scraping.schema import Document, Store
from scraping.store import connect, upsert_document, upsert_store

T1 = datetime(2026, 10, 2, tzinfo=UTC)


@pytest.mark.parametrize(
    ("ts", "label"),
    [
        (datetime(2026, 2, 1, tzinfo=UTC), "FY2026 Q1"),
        (datetime(2026, 4, 30, tzinfo=UTC), "FY2026 Q1"),
        (datetime(2026, 5, 1, tzinfo=UTC), "FY2026 Q2"),
        (datetime(2026, 10, 12, tzinfo=UTC), "FY2026 Q3"),
        (datetime(2027, 1, 31, tzinfo=UTC), "FY2026 Q4"),
    ],
)
def test_fiscal_quarter_approx(ts, label):
    assert fiscal_quarter_approx(ts) == label


def test_export_dedupes_cross_platform_reviews_and_drops_deleted(tmp_path):
    conn = connect(tmp_path / "s.sqlite")
    upsert_store(conn, Store(
        store_id="s1", banner="DICK'S Sporting Goods", company="DKS", cohort="dks", priority=0,
        name="DICK'S Sporting Goods", address=None, city="Dallas", state="TX",
        postal_code=None, lat=None, lng=None, discovery_query="q", discovered_at=T1,
    ))
    review = {
        "cohort": "dks", "store_id": "s1", "doc_type": "review", "body": "Long lines", "rating": 2.0,
        "created_at": datetime(2026, 3, 1, 12, tzinfo=UTC), "collected_at": T1,
    }
    upsert_document(conn, Document(doc_id="gmaps:places/s1/reviews/r1", platform="google_maps",
                                   source_listings=["places_details:most_relevant"], **review))
    upsert_document(conn, Document(doc_id="apify_gmaps:x1", platform="apify_google_maps",
                                   source_listings=["apify_import"], **review))
    post = {"platform": "reddit", "doc_type": "post", "cohort": "dks", "community": "dickssportinggoods",
                "created_at": datetime(2026, 1, 15, tzinfo=UTC), "source_listings": ["new"]}
    upsert_document(conn, Document(doc_id="reddit:t3_a", title="Hours cut", body="again",
                                   collected_at=T1, **post))
    upsert_document(conn, Document(doc_id="reddit:t3_b", title="x", body="y", collected_at=T1,
                                   **post))
    upsert_document(conn, Document(doc_id="reddit:t3_b", is_deleted=True,
                                   collected_at=datetime(2026, 10, 3, tzinfo=UTC), **post))
    conn.commit()
    export_all(conn, tmp_path / "out")
    df = pd.read_csv(tmp_path / "out" / "documents.csv", encoding="utf-8-sig").set_index("doc_id")
    assert sorted(df.index) == ["gmaps:places/s1/reviews/r1", "reddit:t3_a"]
    assert df.loc["reddit:t3_a", "fiscal_quarter_approx"] == "FY2025 Q4"
    assert df.loc["reddit:t3_a", "text"] == "Hours cut\n\nagain"
    assert df.loc["gmaps:places/s1/reviews/r1", "banner"] == "DICK'S Sporting Goods"
    assert df.loc["gmaps:places/s1/reviews/r1", "voice"] == "customer_review"


def test_status_on_empty_db(tmp_path, capsys):
    assert main(["--db", str(tmp_path / "s.sqlite"), "status"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["documents"] == [] and out["snapshots"] == 0


def test_reddit_requires_salt(tmp_path, capsys, monkeypatch):
    monkeypatch.delenv("SCRAPING_AUTHOR_SALT", raising=False)
    assert main(["--db", str(tmp_path / "s.sqlite"), "reddit"]) == 1
    assert "SCRAPING_AUTHOR_SALT" in json.loads(capsys.readouterr().out)["error"]


def test_export_neutralizes_spreadsheet_formulas(tmp_path):
    conn = connect(tmp_path / "s.sqlite")
    upsert_document(conn, Document(
        doc_id="reddit:t3_f", platform="reddit", doc_type="post", cohort="general_retail",
        community="retail", title='=HYPERLINK("http://x","click")', body=None,
        created_at=datetime(2026, 3, 1, tzinfo=UTC), collected_at=T1, source_listings=["new"],
    ))
    conn.commit()
    export_all(conn, tmp_path / "out")
    df = pd.read_csv(tmp_path / "out" / "documents.csv", encoding="utf-8-sig")
    assert df.loc[0, "text"] == "'=HYPERLINK(\"http://x\",\"click\")"


def test_config_with_utf8_bom_is_accepted(tmp_path, capsys):
    config = tmp_path / "config.json"
    config.write_text('{"reddit": {}, "places": {}}', encoding="utf-8-sig")
    assert main(["--config", str(config), "--db", str(tmp_path / "s.sqlite"), "status"]) == 0
