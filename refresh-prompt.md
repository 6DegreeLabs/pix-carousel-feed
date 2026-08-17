# Carousel feed refresh — scheduled task prompt

You are refreshing the Pix carousel feed at /Users/ali/pix-carousels/feed-repo/beehiiv-posts.json.

1. `cd /Users/ali/pix-carousels/feed-repo && git pull --ff-only` (someone may have pushed a manual fix).
2. Read `beehiiv-posts.json` and note the newest post `date`.
3. Via the beehiiv MCP (publication pub_1e9c8050-9d8e-47d9-9535-cc0b149cdce0, Pix Media Newsletters), list posts published AFTER that date (status confirmed/published only, no drafts). If none, stop — no commit, no output needed.
4. For each new post, build a post object: id, title, date (ISO 8601 Z), tags (content tag displays, lowercase, matching the feed's existing style, e.g. "book pix", "worth the read"), brand (the tool's brand name, e.g. "book pix", "worth the read +" for premium), url (public web URL).
5. For NON-premium posts (brand not ending in "+"), fetch content via get_post_content (format: text) and add a `text` field: plain editorial text kept VERBATIM — title line, byline, section labels, pick titles/authors/blurbs, quoted reviews. DROP: mastheads/nav, quick links, sponsored or "together with"/"presented by"/"brought to you by"/"a message from" blocks and named advertisers (Inside Hotels, Hotel Spotlight, Curiosity, IXL, Curacity, Kalshi, LifeMD, OneSkin, Pique, Wegovy, Linkby), subscribe/referral promos, polls/surveys, footers, unsubscribe lines, image markup, merge tags like {{first_name}}. Premium posts (brand ends "+") get NO text field.
6. Premium posts only: also append the full post object WITH cleaned text to the local overlay file /Users/ali/pix-carousels/beehiiv-posts.json (insert into its posts list; keep valid JSON). Premium text lives only there, never in the public repo.
7. Write the new post objects as a JSON list to a temp file, then run `python3 merge.py <temp file>`. It appends, dedups (same title+brand within the window becomes metadata-only with duplicate_send: true), prunes >30 days, and validates. If it fails, fix the input and retry — never edit beehiiv-posts.json by hand in this task.
8. `git add beehiiv-posts.json && git commit -m "feed: refresh $(date +%m-%d-%y)" && git push`.

Rules: never push if merge.py failed; never include text for premium or partner (read now) or b2b posts; keep the file valid JSON at all times.
