# Watchlist contract

## Canonical JSON

Keep the user-visible schema stable. `scope` is persisted because rankings from different markets, languages, devices, or depths cannot be compared safely.

```json
{
  "domains": {
    "example.com": {
      "label": "Main site",
      "scope": {
        "location_name": "United States",
        "language_code": "en",
        "device": "desktop",
        "depth": 100
      },
      "keywords": ["seo audit tool", "keyword research"],
      "history": [
        {
          "date": "2026-04-15",
          "rankings": [
            {"keyword": "seo audit tool", "position": 8},
            {"keyword": "keyword research", "position": null}
          ]
        }
      ]
    }
  }
}
```

Use only an integer `1..depth` or JSON `null` for `position`. `null` means a successful live SERP response did not contain the domain within the saved depth. A failed call is not a ranking result and must not create a history entry.

Preserve keyword spelling from the first occurrence. Trim whitespace, reject empty entries, case-insensitively deduplicate, and reject keywords over 80 characters or 10 words. Keep ranking rows in current keyword order.

Accept only `desktop` or `mobile` and an integer depth from 10 through 100. Use a country-level DataForSEO Labs location for discovery; reject a scope the Ranked Keywords MCP tool cannot represent rather than silently broadening it.

## Store resolution

- Default domain store: `<cwd>/SEO/<domain>/watchlist.json`.
- A supplied `.json` path is an exact shared store and may contain several domain entries.
- A supplied directory is a storage root; use `<root>/<domain>/watchlist.json`.
- For `list`, scan `<root>/*/watchlist.json`, or read the one exact JSON file supplied. Deduplicate identical resolved files.

Use UTF-8, two-space indentation, and a trailing newline. Write a sibling temporary file, flush it, and atomically replace the destination. Preserve unknown top-level and domain fields unless they conflict with the canonical fields being updated.

For a domain removal, delete only that entry. If a domain-specific file then contains no domains, remove `watchlist.json` but leave its directory and reports intact. Removing a keyword changes `keywords` only; historical snapshots remain immutable evidence.

## Retrieval paths

Prefer the bundled Python 3 helper because it reduces verbose SERP responses locally before they reach the agent:

```text
python3 <skill-directory>/scripts/rank_watchlist_api.py preflight [--env-file <path>]
python3 <skill-directory>/scripts/rank_watchlist_api.py add <domain> [scope options] [--keyword <term> ...] --watchlist <path> --limit 100 --commit
python3 <skill-directory>/scripts/rank_watchlist_api.py check <domain> [scope options] --watchlist <path> --commit
python3 <skill-directory>/scripts/rank_watchlist_api.py resume <run-file> [--commit]
```

The helper uses only Python's standard library. It reads `DATAFORSEO_USERNAME` or `DATAFORSEO_LOGIN` plus `DATAFORSEO_PASSWORD` from process environment variables, then from `./.env` or the supplied `--env-file`. Never pass credentials as command arguments, write them to reports, or retain raw responses.

For discovery it calls `POST /v3/dataforseo_labs/google/ranked_keywords/live`. For each live check it calls `POST /v3/serp/google/organic/live/advanced` with `target`, `stop_crawl_on_match`, and `find_targets_in: ["organic"]`.

Before billable calls, the helper creates a durable manifest under `<watchlist-directory>/.watchlist-runs/` unless `--run-file` is supplied. It atomically updates that manifest after every completed live check. With `--commit`, it validates all results, detects concurrent watchlist changes, appends the snapshot through a flushed sibling temporary file and `os.replace`, and marks the manifest `committed`. It preserves unknown watchlist and domain fields. Repeating commit for the same manifest must not duplicate history. For target-filtered live SERP checks, treat DataForSEO task code `40102 No Search Results` as a completed check with `position: null`, not as a retryable failure.

Standard output is a bounded summary containing status, paths, counts, date, and known total cost; full keyword data stays in the run manifest and canonical watchlist. If stdout is absent, inspect those files. Treat a `committed` manifest and matching canonical snapshot as success. Exit `3` / `partial` retains successful paid checks; `resume` requests only keywords missing from `results`. A run stopped before discovery completed is not safely resumable without another approved discovery request.

Use MCP fallback only when Python or the helper cannot start, or preflight reports `status: unavailable` / `fallback_safe: true` before any direct API task. The fallback discovery call must use `limit: 20`, `item_types: ["organic"]`, and descending search volume. Union those first 20 candidates after every explicit and existing keyword, then use one MCP live SERP call per final keyword. Record `source: MCP fallback` and `discovery_limit: 20` in reports. A truncated or otherwise incomplete MCP response is a failed check, not a null position.

If a direct API operation returns `fallback_safe: false`, it may already have incurred cost. Inspect its run manifest first. Do not restart through MCP; ask before resuming missing checks or making another discovery request.

## Command details

### `add`

Preserve an existing `label` when no replacement is supplied; use the domain as the label only for a new unlabeled entry. Order explicit keywords first, then existing keywords, then up to 100 discovery results ordered by descending search volume and better organic `rank_group`. Deduplicate without dropping supplied or existing terms. State the resulting live-call count before checking rankings.

The Ranked Keywords dataset is a discovery source and may be updated weekly; it is not the saved live baseline. Direct API discovery may contribute up to 100 candidates; MCP fallback discovery may contribute up to 20. Run one live SERP request for every final keyword and store only those live positions.

If discovery returns no rows and no explicit or existing keywords remain, do not create an empty watchlist. If an existing entry has history and the requested scope differs, explain that the series would be incomparable; proceed only after explicit confirmation, replace the saved scope, and clear history before recording the new baseline.

### `check`

Reject a missing domain entry or empty keyword list without making billable calls. Compare keywords case-insensitively:

- **Up:** both numeric and current is lower; delta positive.
- **Down:** both numeric and current is higher; delta negative.
- **Same:** equal numeric positions, or both are null.
- **New:** previous is null and current is numeric.
- **Lost:** previous is numeric and current is null.

For the first snapshot, state that a baseline was recorded and no prior comparison exists. Append same-day checks rather than replacing them; the immediately previous array element is the baseline.

Render the human-readable diff in this form, including only populated groups:

```text
Movement since 2026-04-15:
🟢 Up:    "seo audit tool"    8 → 5  (+3)
🔴 Down:  "ai content tool"  12 → 18 (-6)
⚪ Same:  "stable term"       3 → 3
🟢 New:   "new term"          — → 14
🔴 Lost:  "lost term"         9 → —
```

### `list` and `remove`

For Last avg position, use the latest snapshot and exclude null positions; show one decimal or `—`. Missing history means Last checked and Last avg position are both `—`.

Require exact normalized-domain selection for removal. For keywords, case-insensitive equality must resolve to exactly one saved entry. Show what was removed and the resolved store path.

## Report contract

A custom report directory overrides the default. Otherwise, use the domain directory that contains its default watchlist; for an exact shared JSON store, use the file's parent directory.

Treat a ranking-report request for a saved domain as `check` plus report unless the user explicitly requests a report from the latest stored snapshot. Without a saved domain, ask whether to create it with `add` and gather any missing required input before billable calls.

The filename intentionally preserves the requested spelling:

```text
<YYYY-MM-DD>_Rankink-Report_<domain>.md
```

Use these sections:

1. first line: local ISO date;
2. H1 title and executive summary;
3. Scope: domain, label, location, language, device, depth, checked date/time, watchlist path, keyword coverage, and total cost;
4. Movement since the previous check, including New and Lost;
5. Current rankings with keyword, position, previous position, delta/status, and ranking URL when retained from the current response;
6. concerning drops (delta `<= -5`) and Lost rankings;
7. opportunities at positions 11–20;
8. one evidence-based suggested action;
9. methodology, DataForSEO call log, limitations, and official source links;
10. Short take with concerns, opportunities, and the action.

Identify the retrieval source as `direct DataForSEO API` or `MCP fallback`. When fallback was used, disclose that discovery was limited to 20 keywords instead of 100. Do not describe this limit as truncating explicit or previously saved terms.

Do not claim that a null position is absent from Google. Say it was not found within the saved depth. Rankings are volatile point-in-time observations; one movement is not proof of a trend.
