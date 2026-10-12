from __future__ import annotations

import argparse
import json
import os
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from scraping.store import connect, record_run


def _salt() -> str:
    salt = os.environ.get("SCRAPING_AUTHOR_SALT")
    if not salt:
        raise RuntimeError("missing environment variable: SCRAPING_AUTHOR_SALT")
    return salt


def _dispatch(args: argparse.Namespace, config: dict, conn: sqlite3.Connection) -> dict:
    if args.command == "status":
        from scraping.export import status

        return status(conn)
    if args.command == "export":
        from scraping.export import export_all

        return export_all(conn, args.output)
    if args.command == "reddit":
        salt = _salt()
        from scraping.reddit import collect_subreddit, make_reddit, refresh_deletions

        reddit, cfg = make_reddit(), config["reddit"]
        subs = [s for s in cfg["subreddits"] if args.subreddit in (None, s["name"])]
        result: dict = {
            s["name"]: collect_subreddit(
                reddit, conn, s["name"], s["cohort"], cfg["search_terms"],
                cfg["max_more_comments"], salt, with_comments=not args.no_comments,
            )
            for s in subs
        }
        result["deletion_refresh"] = refresh_deletions(reddit, conn)
        return result
    from scraping.places import PlacesClient, banners_from_config

    banners = banners_from_config(config)
    if args.command == "apify-import":
        from scraping.apify import import_apify

        rows = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
        return import_apify(conn, rows, banners, datetime.now(UTC), _salt())
    salt = _salt() if args.command == "reviews" else ""
    client = PlacesClient()
    try:
        if args.command == "stores-discover":
            from scraping.places import discover_stores

            return discover_stores(client, conn, banners, config["places"]["max_tile_depth"])
        from scraping.reviews import fetch_reviews

        cap = config["places"]["max_details_calls_per_run"]
        return fetch_reviews(client, conn, min(cap, args.max_stores or cap), salt)
    finally:
        client.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m scraping")
    parser.add_argument("--config", default="scraping/config.json")
    parser.add_argument("--db", default="scraping/data/scraping.sqlite")
    sub = parser.add_subparsers(dest="command", required=True)
    reddit = sub.add_parser("reddit", help="Collect posts and comments via PRAW.")
    reddit.add_argument("--subreddit", default=None)
    reddit.add_argument("--no-comments", action="store_true")
    sub.add_parser("stores-discover", help="Find store locations via Google Places Text Search.")
    reviews = sub.add_parser("reviews", help="Fetch reviews and rating snapshots per store.")
    reviews.add_argument("--max-stores", type=int, default=None)
    apify = sub.add_parser("apify-import", help="Import an Apify Google Maps reviews export.")
    apify.add_argument("--input", required=True)
    export = sub.add_parser("export", help="Write sentiment-ready CSVs.")
    export.add_argument("--output", default="scraping/data/exports")
    sub.add_parser("status", help="Coverage by platform, cohort and community.")
    args = parser.parse_args(argv)
    started = datetime.now(UTC)
    try:
        config = json.loads(Path(args.config).read_text(encoding="utf-8-sig"))
        conn = connect(args.db)
        result = _dispatch(args, config, conn)
        record_run(conn, args.command, started, datetime.now(UTC), vars(args), result, "ok")
        print(json.dumps(result, default=str))
        return 0
    except Exception as exc:  # noqa: BLE001 - surface any collector failure as JSON
        print(json.dumps({"error": str(exc), "command": args.command}))
        return 1
