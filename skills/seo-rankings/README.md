# SEO Rankings

`seo-rankings` checks a domain's current Google organic position for a supplied list of keywords, adds Google Ads search-volume context, groups each keyword into an actionable ranking tier, and writes a dated Markdown report.

## What the skill does

For each unique keyword, the skill runs one live Google organic SERP request and searches the returned organic results for the target domain or one of its subdomains. It uses the lowest organic `rank_group`; it does not use absolute SERP position, which can include unlike result types. It then retrieves search volume for the complete keyword list in one bulk request.

Each keyword receives one tier and action:

| Tier | Position | Recommended action |
| --- | ---: | --- |
| Winning | 1–3 | Defend and monitor weekly |
| Page 1 | 4–10 | Push into the top three with internal links and on-page refinement |
| Close | 11–30 | Re-optimize and build links |
| Long-haul | 31–100 | Decide whether to pivot or invest heavily |
| Not ranking | Not found within requested depth | Decide whether to pursue or drop |

The skill also selects one highest-leverage keyword, favoring the first populated tier in this order: Close, Page 1, Long-haul, Not ranking, Winning. Within that tier it prioritizes search volume, then the better position, then original input order.

## Why this analysis matters

A website can receive very different amounts of attention depending on whether it appears near the top of Google, near the bottom of the first page, or several pages later. A rankings check provides a clear snapshot of where the site currently appears for searches that matter to the business. Adding search volume helps distinguish an important opportunity from a term that very few people use.

The ranking tiers turn that snapshot into practical priorities. A page just outside the first page may need focused improvements, while a top-three result may need monitoring and protection rather than a rewrite. Repeating the analysis after meaningful changes can show whether visibility is moving in the right direction. Rankings naturally change and this report is a point-in-time measurement, so it supports better decisions but cannot guarantee future positions.

## Requirements and inputs

- The official DataForSEO MCP server with the SERP and Keywords Data modules enabled.
- Filesystem write access.
- A domain or HTTP(S) URL.
- One or more keywords. Keywords are trimmed and deduplicated case-insensitively; each must be no longer than 80 characters or 10 words.

Optional inputs are location, language, device, result depth, and report root. Defaults are United States, `en`, desktop, depth 100, and `SEO/` below the current working directory. Device may be desktop or mobile; depth may be 10–100. Lists over the bulk endpoint's 700-keyword limit must be split with approval.

## Invocation examples

Directly by skill name:

```text
Use the seo-rankings skill for example.com with the keywords "seo audit tool", "keyword research", and "ai seo".
```

For mobile results:

```text
Check example.com Google mobile rankings in the United States for "buy widgets" and "best widgets".
```

With another market and a shallower result set:

```text
Run seo-rankings for example.de in Germany, language German, depth 50, for "seo agentur" and "technisches seo".
```

With a custom report location:

```text
Check the live rankings of https://www.example.com for "product analytics", "analytics platform", and "web analytics" and save the report under ./weekly-reports.
```

If either the domain or keyword list is missing, the skill asks for all missing required inputs before making billable requests.

## What to expect in the report

The report starts with the local ISO date and is saved by default as:

```text
SEO/<domain>/<YYYY-MM-DD>_Rankings_<domain>.md
```

It contains:

- Scope, location, language, device, depth, timestamp, and total DataForSEO cost.
- An executive summary.
- Grouped tables containing keyword, organic position, search volume, ranking URL, and next action.
- Counts for Winning, Page 1, Close, Long-haul, and Not ranking keywords.
- The single highest-leverage action with its keyword, position, tier, volume, URL, and recommendation.
- Methodology, endpoint call log, coverage, limitations, and official DataForSEO references.

“Not ranking” means that the domain was not found among the organic results within the requested depth; it does not prove that the domain is absent from all Google results. Missing positions or volumes appear as `—`. Ranking URLs are shown as target-relative paths where possible. After writing the report, the skill returns its absolute path and a concise summary.
