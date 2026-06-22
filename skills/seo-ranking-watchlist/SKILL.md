---
name: seo-ranking-watchlist
description: "Use when creating or maintaining a persistent SEO keyword watchlist, discovering ranked domain keywords, checking Google positions across runs, comparing gains and losses, listing or removing tracked entries, or producing a ranking-change report."
compatibility: "Requires Python 3 with direct DataForSEO API credentials, or the official DataForSEO MCP server with DATAFORSEO_LABS and SERP modules, plus filesystem write access."
---

# SEO Ranking Watchlist

Follow [Ranked Keywords](https://docs.dataforseo.com/v3/dataforseo_labs-google-ranked_keywords-live/) and [Live SERP](https://docs.dataforseo.com/v3/serp-se-type-live-advanced/). Read [references/watchlist-contract.md](references/watchlist-contract.md).

## Input and storage

Identify `add`, `list`, `check`, or `remove`. Require a domain except for `list`. Normalize to a lowercase hostname without credentials, port, path, trailing dot, or `www.`. Default scope is `United States`, `en`, `desktop`, depth `100`; persist it because only equal scopes are comparable.

Default to `SEO/<domain>/watchlist.json`. Preserve unrelated data and never overwrite malformed JSON.

## Retrieval

For `add` or `check`, first run:

```text
python3 <skill-directory>/scripts/rank_watchlist_api.py preflight
```

For `add`, invoke helper `add` with domain, scope, explicit keywords, `--watchlist <path> --limit 100 --commit`. For `check`, invoke helper `check` with the saved path, exact scope, and `--commit`. Accept exit `0` with `status: committed`, then validate the file. The helper stages each result, commits atomically, treats DataForSEO SERP `40102 No Search Results` as a successful `null` position, and prints a bounded summary.

After empty or interrupted output, inspect the watchlist and newest `.watchlist-runs/*.json` before retrying. A `committed` run succeeded without stdout. Exit `3` or `partial` is resumable; after retry approval, use `resume <run-file>` for missing keywords only.

If Python, the helper, or credentials are unavailable before a direct task, use MCP. Discover only `20` organic keywords ordered by search volume, then live-check their union with every explicit and existing term. Disclose reduced coverage. Inspect any `fallback_safe: false` run and ask before retrying.

## Commands

- **add:** Order explicit, existing, then discovered keywords; deduplicate case-insensitively. Commit only after all checks succeed. Confirm scope changes and pass `--reset-scope` when approved.
- **check:** Use exact saved scope and keywords, append one successful snapshot, and diff against its predecessor.
- **list:** Make no external calls. Show Domain, label, keyword count, last checked, and latest average numeric position.
- **remove:** Make no external calls. Remove the normalized domain or one exact case-insensitive keyword; preserve history when removing a keyword.

Store the lowest matching organic `rank_group`, or `null` when a complete response did not find the domain within depth. Never use `rank_absolute` or `101`. Failed or incomplete runs leave the canonical file unchanged. Sum unrounded endpoint costs.

## Output

Classify Up, Down, Same, New, and Lost. Delta is previous minus current, so `8 -> 5` is `+3`. Treat deltas `<= -5` and Lost as concerning; positions 11-20 are opportunities.

For reports, write `<YYYY-MM-DD>_Rankink-Report_<domain>.md` under the domain directory. Include scope, watchlist path, source, discovery coverage, movement/current tables, concerns, opportunities, action, methodology, costs, and limitations. Begin with the local ISO date and return the absolute path.

Always end with a short take naming concerns, opportunities, and one action, or state what was not evaluated.
