from __future__ import annotations

import os
import sqlite3
from collections.abc import Iterable
from datetime import UTC, datetime
from typing import Any

from scraping.schema import Cohort, Document
from scraping.store import get_num_comments, purge_document, upsert_document
from scraping.text import DELETED_MARKERS, author_hash, tag_companies

# Each listing caps at ~1,000 items; the union widens coverage.
LISTINGS: list[tuple[str, str | None]] = [
    ("new", None), ("hot", None), ("rising", None),
    *[("top", t) for t in ("all", "year", "month", "week", "day")],
    *[("controversial", t) for t in ("all", "year", "month")],
]
REQUIRED_ENV = ("REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT")


def make_reddit() -> Any:
    missing = [key for key in REQUIRED_ENV if not os.environ.get(key)]
    if missing:
        raise RuntimeError("missing environment variables: " + ", ".join(missing))
    import praw

    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
        check_for_async=False,
    )


def harvest(subreddit: Any, search_terms: Iterable[str]) -> dict[str, tuple[Any, set[str]]]:
    found: dict[str, tuple[Any, set[str]]] = {}

    def add(items: Iterable[Any], label: str) -> None:
        for item in items:
            found.setdefault(item.id, (item, set()))[1].add(label)

    for kind, time_filter in LISTINGS:
        method = getattr(subreddit, kind)
        if time_filter is None:
            add(method(limit=None), kind)
        else:
            add(method(time_filter=time_filter, limit=None), f"{kind}:{time_filter}")
    for term in search_terms:
        add(subreddit.search(term, sort="new", time_filter="all", limit=None), f"search:{term}")
    return found


def _ts(epoch: float) -> datetime:
    return datetime.fromtimestamp(epoch, UTC)


def submission_to_doc(
    s: Any, cohort: Cohort, labels: set[str], collected_at: datetime, salt: str
) -> Document:
    deleted = s.author is None or s.selftext in DELETED_MARKERS
    return Document(
        doc_id=f"reddit:t3_{s.id}", platform="reddit", doc_type="post", cohort=cohort,
        community=str(s.subreddit), thread_id=f"t3_{s.id}",
        title=None if deleted else s.title,
        body=None if deleted else (s.selftext or None),
        score=s.score, num_comments=s.num_comments, created_at=_ts(s.created_utc),
        collected_at=collected_at,
        author_hash=None if deleted else author_hash(str(s.author), salt),
        author_flair=s.author_flair_text, link_flair=s.link_flair_text,
        url=f"https://www.reddit.com{s.permalink}", is_deleted=deleted, edited=bool(s.edited),
        company_mentions=[] if deleted else tag_companies(f"{s.title}\n{s.selftext}"),
        source_listings=sorted(labels),
    )


def comment_to_doc(
    c: Any, submission_id: str, cohort: Cohort, community: str, collected_at: datetime,
    salt: str,
) -> Document:
    deleted = c.author is None or c.body in DELETED_MARKERS
    return Document(
        doc_id=f"reddit:t1_{c.id}", platform="reddit", doc_type="comment", cohort=cohort,
        community=community, thread_id=f"t3_{submission_id}", parent_id=c.parent_id,
        body=None if deleted else c.body, score=c.score, created_at=_ts(c.created_utc),
        collected_at=collected_at,
        author_hash=None if deleted else author_hash(str(c.author), salt),
        author_flair=c.author_flair_text, url=f"https://www.reddit.com{c.permalink}",
        is_deleted=deleted, edited=bool(c.edited),
        company_mentions=[] if deleted else tag_companies(c.body),
        source_listings=["comments"],
    )


def collect_subreddit(
    reddit: Any, conn: sqlite3.Connection, name: str, cohort: Cohort,
    search_terms: Iterable[str], max_more: int, salt: str, with_comments: bool = True,
    now: datetime | None = None,
) -> dict[str, int]:
    now = now or datetime.now(UTC)
    counts = dict.fromkeys(
        ("posts", "comments", "inserted", "updated", "unchanged", "deleted",
         "comment_fetches_skipped"),
        0,
    )
    for s, labels in harvest(reddit.subreddit(name), search_terms).values():
        doc = submission_to_doc(s, cohort, labels, now, salt)
        previous = get_num_comments(conn, doc.doc_id)
        counts[upsert_document(conn, doc)] += 1
        counts["posts"] += 1
        if with_comments and previous is not None and previous == s.num_comments:
            counts["comment_fetches_skipped"] += 1
        elif with_comments:
            s.comments.replace_more(limit=max_more)
            for c in s.comments.list():
                counts[upsert_document(conn, comment_to_doc(c, s.id, cohort, name, now, salt))] += 1
                counts["comments"] += 1
        conn.commit()  # per submission, so an interrupted run keeps its progress
    return counts


def refresh_deletions(
    reddit: Any, conn: sqlite3.Connection, now: datetime | None = None, batch: int = 100
) -> dict[str, int]:
    """Re-check every stored Reddit item, including ones no listing returns any more."""
    now = now or datetime.now(UTC)
    ids = [r[0] for r in conn.execute(
        "SELECT doc_id FROM documents WHERE platform = 'reddit' AND is_deleted = 0"
    )]
    counts = {"checked": 0, "purged": 0}
    for start in range(0, len(ids), batch):
        fullnames = [doc_id.removeprefix("reddit:") for doc_id in ids[start:start + batch]]
        for item in reddit.info(fullnames=fullnames):
            counts["checked"] += 1
            field = "selftext" if item.fullname.startswith("t3_") else "body"
            if item.author is None or getattr(item, field, None) in DELETED_MARKERS:
                purge_document(conn, f"reddit:{item.fullname}", now)
                counts["purged"] += 1
        conn.commit()
    return counts
