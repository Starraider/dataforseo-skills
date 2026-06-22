---
name: seo-ranking-watchlist
description: "Use when creating or maintaining a persistent SEO keyword watchlist, discovering up to 100 keywords a domain ranks for, checking saved Google positions again, comparing gains and losses across runs, listing or removing tracked domains and keywords, or producing a ranking-change Markdown report."
compatibility: "Requires the official DataForSEO MCP server with DATAFORSEO_LABS and SERP modules enabled and filesystem write access."
---

# SEO Ranking Watchlist

Follow [Ranked Keywords](https://docs.dataforseo.com/v3/dataforseo_labs-google-ranked_keywords-live/), [Live Advanced SERP](https://docs.dataforseo.com/v3/serp-se-type-live-advanced/), and [DataForSEO rank-tracking guidance](https://dataforseo.com/blog/budget-friendly-rank-tracking-strategies-with-dataforseo-serp-api). Read [references/watchlist-contract.md](references/watchlist-contract.md) before acting.

## Input and storage

Identify `add`, `list`, `check`, or `remove`. Require a domain for all except `list`; `add` accepts zero or more keywords. Ask once for missing required input and wait. Normalize domains to lowercase hostnames without credentials, port, path, trailing dot, or leading `www.`. Reject malformed input.

Default scope is `United States`, `en`, `desktop`, depth `100`. Save it with the domain because only equal scopes are comparable. Default storage is `SEO/<domain>/watchlist.json`; create directories. Read before writing and preserve unrelated domains. Write valid JSON atomically. Never overwrite malformed data; report the error.

## Commands

- **add:** Call `dataforseo_labs_google_ranked_keywords` once with target, scope, `limit: 100`, `item_types: ["organic"]`, `include_subdomains: true`, and descending search volume. Case-insensitively union existing, explicit, and up to 100 discovered keywords, explicit first. Then run the live workflow on the complete set and append the first or next snapshot. A scope change requires explicit confirmation and a fresh history.
- **list:** Make no DataForSEO calls. Scan the selected store(s) and print `Domain | Label | # keywords | Last checked | Last avg position`; average only numeric positions.
- **check:** Load the exact saved keywords and scope, run the live workflow, append one snapshot, and diff it against the immediately previous snapshot.
- **remove:** Remove the normalized domain or one case-insensitively matched keyword. Preserve history when removing one keyword. Make no DataForSEO calls.

## Live workflow

State scope and planned calls. The command authorizes one `serp_organic_live_advanced` call per keyword; ask before retries or extras. Use Google and saved scope. Inspect only organic items, match the target or its subdomains, and store the lowest `rank_group`; use `null` when absent within depth. Never use `rank_absolute` or convert absence to `101`.

Validate every response. If any call fails, leave the file unchanged. Log endpoint costs and sum unrounded values as `Total cost: x,xx USD`. Append local ISO date only after all calls succeed.

## Output

Show movement as 🟢 Up, 🔴 Down, ⚪ Same, 🟢 New, or 🔴 Lost. Numeric delta is `previous_position - current_position`; thus `8 → 5 (+3)`. Treat a numeric delta `<= -5` and any Lost ranking as concerning. Treat positions 11–20 as opportunities.

When asked for a ranking report, create `<YYYY-MM-DD>_Ranking-Report_<domain>.md` in the selected domain directory, beginning with the local ISO date. Include scope, watchlist path, summary, full movement/current tables, concerns, opportunities, action, methodology, cost log, and limitations. Return its absolute path.

Always end with a short take naming concerning drops, opportunities, and one suggested action; say none or not evaluated when applicable.
