from datetime import UTC, datetime
from types import SimpleNamespace as NS

import pytest

from scraping.reddit import collect_subreddit, make_reddit
from scraping.store import connect

T0 = datetime(2026, 10, 1, tzinfo=UTC)
T1 = datetime(2026, 10, 8, tzinfo=UTC)


class FakeComments:
    def __init__(self, items):
        self.items = items
        self.replace_calls = 0

    def replace_more(self, limit):
        self.replace_calls += 1

    def list(self):
        return self.items


def post(pid="p1", author="u1", selftext="Way too much stock", num_comments=0, comments=()):
    return NS(
        id=pid, title="Inventory everywhere", selftext=selftext, author=author,
        subreddit="dickssportinggoods", score=5, num_comments=num_comments,
        created_utc=1767225600.0, author_flair_text="Employee", link_flair_text="Rant",
        permalink=f"/r/dickssportinggoods/comments/{pid}/x/", edited=False,
        comments=FakeComments(list(comments)),
    )


def comment(cid="c1", author="u2", body="Same here, hours cut"):
    return NS(
        id=cid, author=author, body=body, parent_id="t3_p1", score=2,
        created_utc=1767229200.0, author_flair_text=None,
        permalink=f"/r/dickssportinggoods/comments/p1/x/{cid}/", edited=False,
    )


class FakeSubreddit:
    def __init__(self, listings):
        self.listings = listings

    def _get(self, label):
        return list(self.listings.get(label, []))

    def new(self, limit):
        return self._get("new")

    def hot(self, limit):
        return self._get("hot")

    def rising(self, limit):
        return self._get("rising")

    def top(self, time_filter, limit):
        return self._get(f"top:{time_filter}")

    def controversial(self, time_filter, limit):
        return self._get(f"controversial:{time_filter}")

    def search(self, term, sort, time_filter, limit):
        return self._get(f"search:{term}")


class FakeReddit:
    def __init__(self, sub):
        self.sub = sub

    def subreddit(self, name):
        return self.sub


def run(conn, listings, now):
    return collect_subreddit(
        FakeReddit(FakeSubreddit(listings)), conn, "dickssportinggoods", "dks",
        ["inventory"], max_more=8, salt="s", now=now,
    )


def test_harvest_dedupes_and_records_listings(tmp_path):
    conn = connect(tmp_path / "s.sqlite")
    p = post()
    counts = run(conn, {"new": [p], "top:all": [p], "search:inventory": [p]}, T0)
    assert counts["posts"] == 1
    row = conn.execute("SELECT * FROM documents WHERE doc_id = 'reddit:t3_p1'").fetchone()
    assert row["source_listings"] == '["new", "search:inventory", "top:all"]'
    assert (row["cohort"], row["community"], row["author_flair"]) == (
        "dks", "dickssportinggoods", "Employee",
    )
    assert row["created_at"] == "2026-01-01T00:00:00+00:00"


def test_deleted_post_is_purged(tmp_path):
    conn = connect(tmp_path / "s.sqlite")
    run(conn, {"new": [post()]}, T0)
    run(conn, {"new": [post(author=None, selftext="[deleted]")]}, T1)
    row = conn.execute("SELECT * FROM documents WHERE doc_id = 'reddit:t3_p1'").fetchone()
    assert (row["is_deleted"], row["title"], row["body"]) == (1, None, None)


def test_comments_fetched_then_skipped_when_count_unchanged(tmp_path):
    conn = connect(tmp_path / "s.sqlite")
    p = post(num_comments=1, comments=[comment()])
    first = run(conn, {"new": [p]}, T0)
    second = run(conn, {"new": [p]}, T1)
    assert first["comments"] == 1
    assert second["comment_fetches_skipped"] == 1
    assert p.comments.replace_calls == 1
    c = conn.execute("SELECT * FROM documents WHERE doc_id = 'reddit:t1_c1'").fetchone()
    assert (c["thread_id"], c["parent_id"], c["doc_type"]) == ("t3_p1", "t3_p1", "comment")


def test_make_reddit_requires_env(monkeypatch):
    for key in ("REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT"):
        monkeypatch.delenv(key, raising=False)
    with pytest.raises(RuntimeError, match="REDDIT_CLIENT_ID"):
        make_reddit()


def test_refresh_deletions_purges_items_outside_listings(tmp_path):
    from scraping.reddit import refresh_deletions

    conn = connect(tmp_path / "s.sqlite")
    run(conn, {"new": [post("p1"), post("p2")]}, T0)

    class InfoReddit:
        def __init__(self):
            self.calls = []
            self.items = {
                "t3_p1": NS(fullname="t3_p1", author=None, selftext="[deleted]"),
                "t3_p2": NS(fullname="t3_p2", author="u1", selftext="still here"),
            }

        def info(self, fullnames):
            self.calls.append(list(fullnames))
            return [self.items[f] for f in fullnames if f in self.items]

    reddit = InfoReddit()
    counts = refresh_deletions(reddit, conn, now=T1, batch=1)
    assert counts == {"checked": 2, "purged": 1}
    assert len(reddit.calls) == 2
    rows = dict(conn.execute("SELECT doc_id, body FROM documents").fetchall())
    assert rows["reddit:t3_p1"] is None
    assert rows["reddit:t3_p2"] == "Way too much stock"


def test_comments_fetched_after_earlier_no_comments_run(tmp_path):
    conn = connect(tmp_path / "s.sqlite")
    p = post(num_comments=1, comments=[comment()])
    collect_subreddit(
        FakeReddit(FakeSubreddit({"new": [p]})), conn, "dickssportinggoods", "dks",
        [], max_more=8, salt="s", with_comments=False, now=T0,
    )
    counts = run(conn, {"new": [p]}, T1)
    assert counts["comments"] == 1
    assert p.comments.replace_calls == 1
