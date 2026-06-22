# SEO Ranking Watchlist

`seo-ranking-watchlist` maintains a local, file-based set of Google keyword rankings for one or more domains. It discovers keywords a domain already ranks for, combines them with optional target keywords, checks their live positions through DataForSEO, and compares each successful check with the preceding snapshot.

## What the skill does

The skill supports four commands:

- `add`: creates or updates a domain watchlist, discovers current organic keywords, checks the complete set live, and saves the new baseline.
- `list`: prints Domain, label, keyword count, last checked date, and latest average numeric position without making an API call.
- `check <domain>`: checks every saved keyword again, saves the snapshot, and reports Up, Down, Same, New, and Lost movements.
- `remove <domain>` or `remove <domain> <keyword>`: removes a complete domain entry or one active keyword without deleting historical snapshots for other entries.

The primary Python workflow retrieves up to 100 discovered keywords per domain and unions them with all explicit target and existing watchlist terms. It saves completed checks to a durable local run manifest and atomically commits the watchlist only when every keyword succeeds. Interrupted runs can resume only missing checks, avoiding duplicate requests for already completed keywords. If Python or local API credentials are unavailable before a direct request, the skill uses the DataForSEO MCP server and limits discovery to the first 20 keywords. Explicit and previously saved terms are never removed by this fallback.

## Why this analysis matters

Search rankings can change even when a website has not been intentionally updated. Competitors may improve their pages, Google may adjust its results, or an important page may lose visibility. Checking rankings only once shows where a site stands today, but it does not reveal whether performance is improving or getting worse.

The watchlist creates a simple record of those changes over time. It helps a business notice meaningful drops before they lead to a larger loss of visitors, recognize keywords that are moving in the right direction, and find pages sitting just outside the first page of results that may need only a focused improvement. This makes SEO work easier to prioritize: instead of guessing what to fix, the report points to the keywords and pages that deserve attention first.

## Storage and comparison scope

By default, each domain is stored in:

```text
SEO/<domain>/watchlist.json
```

The file uses a `domains` object and records the label, comparison scope, active keyword list, and dated ranking history. Position is an integer or `null`; null means a successful response did not find the domain within the configured depth. Failed calls never become false losses: a snapshot is written only when all requested live checks succeed.

The default comparison scope is United States, English (`en`), desktop, and depth 100. Scope is persisted because results from different locations, languages, devices, or depths are not comparable. Changing scope starts a fresh history after explicit confirmation.

## Movement rules

Position improvements have a positive delta because lower positions are better. For example, 8 to 5 is `+3`, while 12 to 18 is `-6`. A decline of five or more positions and any transition from a numeric rank to not found within depth is concerning. Positions 11–20 are called out as opportunities just outside the top ten.

Every command ends with a short take that states the concerning drops, current opportunities, and one suggested action. Commands that do not check rankings explicitly say those items were not evaluated.

## Ranking reports

When a detailed ranking report is requested, the skill writes a Markdown file under the domain directory by default:

```text
SEO/<domain>/<YYYY-MM-DD>_Rankink-Report_<domain>.md
```

The report starts with the local ISO date and includes scope, cost, movement, current positions, concerns, opportunities, one suggested action, methodology, call log, and limitations.

## Requirements

- Python 3 for the preferred compact direct API workflow.
- `DATAFORSEO_USERNAME` (or `DATAFORSEO_LOGIN`) and `DATAFORSEO_PASSWORD` in the environment, `./.env`, or another file supplied with `--env-file`.
- The official DataForSEO MCP server with DataForSEO Labs and SERP modules enabled as the fallback path.
- DataForSEO credentials configured securely in the MCP server for fallback use.
- Filesystem write access.
- A valid domain for `add`, `check`, and `remove`.

The bundled `scripts/rank_watchlist_api.py` helper uses only the Python standard library. It sends Basic authentication directly to the fixed DataForSEO API host, filters live SERP checks to the target domain, and prints only a small status summary. When DataForSEO returns SERP task code `40102 No Search Results` for that filtered domain check, the helper records a successful `null` position instead of treating the keyword as a broken run. Normalized run data is staged under `.watchlist-runs/`; credentials, authorization headers, and raw API responses are never stored. Atomic replacement and concurrent-change detection protect existing watchlists.

## Examples

```text
Use seo-ranking-watchlist to add example.com with the label Main site and keywords "seo audit tool" and "keyword research".
```

```text
Check example.com from its saved ranking watchlist and show every movement since the previous run.
```

```text
List all SEO ranking watchlists under ./SEO.
```

```text
Remove "keyword research" from the example.com watchlist.
```

```text
Check example.com and create the detailed ranking report under ./client-reports.
```

The skill follows the official [Ranked Keywords API documentation](https://docs.dataforseo.com/v3/dataforseo_labs-google-ranked_keywords-live/), [Live Advanced SERP documentation](https://docs.dataforseo.com/v3/serp-se-type-live-advanced/), and [DataForSEO rank-tracking cost guidance](https://dataforseo.com/blog/budget-friendly-rank-tracking-strategies-with-dataforseo-serp-api).
