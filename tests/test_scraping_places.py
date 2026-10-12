import json
from datetime import UTC, datetime

import httpx
import pytest

from scraping.places import RESULT_CAP, Banner, PlacesClient, discover_stores, search_tiled
from scraping.store import connect

T0 = datetime(2026, 10, 1, tzinfo=UTC)
ROOT = (30.0, -100.0, 40.0, -90.0)
DKS = Banner(
    banner="DICK'S Sporting Goods", company="DKS", cohort="dks", query="DICK'S Sporting Goods",
    name_regex=r"^dick'?s sporting goods", priority=0,
)


def place(pid, name="DICK'S Sporting Goods"):
    return {
        "id": pid, "displayName": {"text": name}, "formattedAddress": "1 Main St",
        "location": {"latitude": 32.0, "longitude": -96.0},
        "addressComponents": [
            {"longText": "Dallas", "shortText": "Dallas", "types": ["locality"]},
            {"longText": "Texas", "shortText": "TX", "types": ["administrative_area_level_1"]},
            {"longText": "75201", "shortText": "75201", "types": ["postal_code"]},
        ],
    }


def tiling_handler(request):
    body = json.loads(request.content)
    rect = body["locationRestriction"]["rectangle"]
    box = (rect["low"]["latitude"], rect["low"]["longitude"],
           rect["high"]["latitude"], rect["high"]["longitude"])
    if box == ROOT:
        page = {None: 0, "p1": 1, "p2": 2}[body.get("pageToken")]
        data = {"places": [place(f"root{page * 20 + i}") for i in range(20)]}
        if page < 2:
            data["nextPageToken"] = f"p{page + 1}"
        return httpx.Response(200, json=data)
    return httpx.Response(200, json={"places": [place(f"child{box}")]})


def test_tile_split_when_result_cap_hit():
    client = PlacesClient(api_key="k", transport=httpx.MockTransport(tiling_handler))
    truncated = []
    found = search_tiled(client, "q", ROOT, max_depth=1, truncated=truncated)
    assert len([k for k in found if k.startswith("root")]) == RESULT_CAP
    assert len([k for k in found if k.startswith("child")]) == 4
    assert client.calls["search"] == 3 + 4
    assert truncated == []


def test_cap_at_max_depth_is_reported():
    client = PlacesClient(api_key="k", transport=httpx.MockTransport(tiling_handler))
    truncated = []
    search_tiled(client, "q", ROOT, max_depth=0, truncated=truncated)
    assert truncated == [ROOT]


def test_discover_filters_lookalikes_and_parses_address(tmp_path):
    def handler(request):
        return httpx.Response(200, json={"places": [
            place("a", "DICK’S Sporting Goods"), place("b", "Dick's Last Resort"),
        ]})

    client = PlacesClient(api_key="k", transport=httpx.MockTransport(handler))
    conn = connect(tmp_path / "s.sqlite")
    counts = discover_stores(client, conn, [DKS], max_depth=0, now=T0)
    assert (counts["matched"], counts["rejected_name"]) == (1, 1)
    row = conn.execute("SELECT * FROM stores").fetchone()
    assert (row["store_id"], row["city"], row["state"], row["postal_code"]) == (
        "a", "Dallas", "TX", "75201",
    )


def test_retries_429_with_retry_after():
    responses = iter([
        httpx.Response(429, headers={"Retry-After": "0"}),
        httpx.Response(200, json={"places": []}),
    ])
    sleeps = []
    client = PlacesClient(
        api_key="k", transport=httpx.MockTransport(lambda r: next(responses)),
        sleep=sleeps.append,
    )
    assert client.search_text("q", ROOT) == []
    assert sleeps == [0.0]


def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("GOOGLE_MAPS_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="GOOGLE_MAPS_API_KEY"):
        PlacesClient()
