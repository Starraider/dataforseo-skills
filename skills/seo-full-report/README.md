# SEO Full Report

`seo-full-report` consolidates all date-matched SEO analyses for one domain into a concise, action-first Markdown report. It reconciles overlapping findings, separates historical source evidence from a bounded current DataForSEO snapshot, and highlights the strongest opportunities to improve rankings.

## What the skill does

The skill:

1. Requires a domain and one ISO date or inclusive ISO date range.
2. Selects regular files directly under `SEO/<domain>/` whose filenames begin with a matching `YYYY-MM-DD_` prefix.
3. Excludes earlier Full SEO Reports by default so repeated runs do not summarize previous summaries or double count evidence.
4. Reads every selected file and inventories any unsupported or unreadable source.
5. Reconciles duplicate, newer, conflicting, and differently scoped findings without averaging incompatible metrics.
6. Uses DataForSEO MCP Domain Rank Overview for a current visibility snapshot and one capped Ranked Keywords call for organic terms in positions 4–20 with positive demand.
7. Produces no more than five immediate actions, an opportunity shortlist, a 30/60/90-day plan, concrete implementation instructions, ownership, effort, dependencies, success checks, and KPIs.
8. Records source provenance, current-call coverage, costs, assumptions, and limitations.

## Why this analysis matters

Individual SEO reports answer separate questions, but website improvements often depend on seeing how those answers connect. A technical problem may block a promising page, several reports may recommend work on the same URL, or an attractive keyword may deserve attention before a larger content project. This full report brings those signals together, removes repetition, and shows what should happen first. Non-specialists get a short, practical plan, while implementers retain the source evidence and exact checks needed to complete and measure the work.

## Requirements and inputs

- The official DataForSEO MCP server with the DataForSEO Labs module enabled.
- Python 3 and filesystem read/write access.
- A domain or HTTP(S) URL.
- One date or an inclusive start/end date range in `YYYY-MM-DD` format.

The report root is optional and defaults to `SEO/` below the current working directory. The skill asks for missing domain or date inputs before selecting files or making billable calls.

## File-selection behavior

For `example.com` and the range `2026-06-19` through `2026-06-21`, the skill examines files directly inside `SEO/example.com/` and selects filenames beginning with an ISO date inside that inclusive range. Files without a date prefix, nested files, out-of-range files, and earlier `_Full-SEO-Report_` outputs are not source evidence by default.

If the domain folder does not exist or no file matches, the skill reports the exact path and dates checked, then stops without a DataForSEO call or an empty report. This makes selection mistakes visible and avoids unnecessary cost.

## Invocation examples

Single date:

```text
Use seo-full-report for example.com and combine all reports dated 2026-06-20.
```

Inclusive date range:

```text
Create a full SEO report for example.org from 2026-06-01 through 2026-06-15 and emphasize what the team should implement next.
```

Custom report root:

```text
Summarize all dated SEO analyses for https://www.example.co.uk/shop from 2026-05-01 to 2026-05-31 and save the full report under ./client-reports.
```

## What to expect in the report

The report leads with the most critical issue, highest-leverage action, best ranking opportunity, primary risk, and evidence confidence. It then provides:

- no more than five immediate actions with ordered implementation instructions;
- up to ten particularly interesting ranking opportunities;
- a 30/60/90-day execution plan;
- critical findings grouped by workstream;
- a timestamped current DataForSEO visibility and ranking-opportunity snapshot;
- a measurement plan tied to recommended actions;
- a complete source inventory and reconciliation notes; and
- a DataForSEO call log, cost statement, and limitations.

For a single source date, the default path is:

```text
SEO/<domain>/<today>_Full-SEO-Report_<domain>_<source-date>.md
```

For a range, the suffix is `<start>_to_<end>`. The current DataForSEO snapshot is clearly separated from findings that belong to the selected historical period. Metrics from overlapping reports are not added together, and recommendations are labeled as analyst prioritization rather than ranking guarantees.
