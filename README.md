# pix-carousel-feed

Auto-refreshed post index for the Pix carousel design tool.

- `beehiiv-posts.json` — the last 30 days of Pix newsletter posts with cleaned editorial text.
  The design tool (Claude Design copy and the local copy) fetches this file at
  `https://raw.githubusercontent.com/6DegreeLabs/pix-carousel-feed/main/beehiiv-posts.json`.
- Premium posts (Worth the Watch/Read/Listen/Chat +) are **metadata-only** — their text is
  paywalled and is deliberately not published here.
- Partner (`read now`) and B2B sends are included as metadata but never carry text; the tool's
  allowlist hides them from the dropdown.

## How it refreshes

A scheduled Claude Code task on Ali's machine runs several times a day:

1. Pull posts published since the newest entry via the beehiiv connection
   (publication `pub_1e9c8050-9d8e-47d9-9535-cc0b149cdce0`).
2. Strip ads, sponsored blocks ("together with", named advertisers), mastheads, quick links,
   subscribe promos, footers, and image markup. Keep editorial wording verbatim.
3. Append the new posts, drop posts older than 30 days, update `generatedAt` and `window`.
4. Commit and push.

The refresh prompt lives in `refresh-prompt.md`. `merge.py` does the deterministic parts
(append, prune, validate) so the model only handles fetch + clean.

Manual fix-ups: edit `beehiiv-posts.json` and push; the next scheduled run builds on top.
