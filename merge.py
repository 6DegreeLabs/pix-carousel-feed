#!/usr/bin/env python3
"""Merge newly fetched posts into beehiiv-posts.json, prune the 30-day window, validate.

Usage: python3 merge.py new-posts.json
  new-posts.json: JSON list of post objects {id, title, date, tags, brand, url, text?}
Exits non-zero (changing nothing) on validation failure.
"""

import json
import sys
from datetime import UTC, datetime, timedelta

FEED = "beehiiv-posts.json"
WINDOW_DAYS = 30
PREMIUM_SUFFIX = "+"


def fail(msg: str) -> None:
    print(f"MERGE FAILED: {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: merge.py new-posts.json")

    with open(FEED, encoding="utf-8") as f:
        feed = json.load(f)
    with open(sys.argv[1], encoding="utf-8") as f:
        new_posts = json.load(f)

    if not isinstance(new_posts, list):
        fail("new-posts.json must be a JSON list")

    existing = {p["id"] for p in feed["posts"]}
    seen_content = {(p["title"], p["brand"]) for p in feed["posts"]}
    added, skipped = [], []

    for p in new_posts:
        for key in ("id", "title", "date", "tags", "brand"):
            if key not in p:
                fail(f"post missing '{key}': {json.dumps(p)[:120]}")
        if p["id"] in existing:
            skipped.append((p["id"], "already present"))
            continue
        if (p["title"], p["brand"]) in seen_content:
            p.pop("text", None)
            p["duplicate_send"] = True
        if p["brand"].endswith(PREMIUM_SUFFIX):
            p.pop("text", None)
        if "text" in p and not p["text"].strip():
            fail(f"post {p['id']} has empty text — omit the key instead")
        added.append(p)
        seen_content.add((p["title"], p["brand"]))

    now = datetime.now(UTC)
    cutoff = now - timedelta(days=WINDOW_DAYS)
    posts = feed["posts"] + added
    posts = [p for p in posts if datetime.fromisoformat(p["date"].replace("Z", "+00:00")) >= cutoff]
    posts.sort(key=lambda p: p["date"], reverse=True)

    feed["posts"] = posts
    feed["generatedAt"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    feed["window"] = {
        "days": WINDOW_DAYS,
        "from": cutoff.strftime("%Y-%m-%d"),
        "to": now.strftime("%Y-%m-%d"),
    }

    out = json.dumps(feed, ensure_ascii=False, indent=1)
    json.loads(out)
    with open(FEED, "w", encoding="utf-8") as f:
        f.write(out)

    print(f"added {len(added)}, skipped {len(skipped)}, total {len(posts)}")
    for pid, why in skipped:
        print(f"  skipped {pid}: {why}")


if __name__ == "__main__":
    main()
