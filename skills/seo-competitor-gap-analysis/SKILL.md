---
name: seo-competitor-gap-analysis
description: "Use when identifying a domain's true organic-search competitors, measuring keyword and traffic gaps, classifying direct, adjacent, and aspirational rivals, calculating a 0-100 Competitive Score, or producing a competitor Markdown report."
compatibility: "Requires the official DataForSEO MCP server with the DATAFORSEO_LABS module enabled and filesystem write access."
---

# SEO Competitor Gap Analysis

Use the official [Competitors Domain](https://docs.dataforseo.com/v3/dataforseo_labs-google-competitors_domain-live/) and [Domain Intersection](https://docs.dataforseo.com/v3/dataforseo_labs-google-domain_intersection-live/) documentation.

## Input and scope

1. Require a project domain; if absent, ask and wait. Normalize a hostname or HTTP(S) URL to lowercase without credentials, port, suffix, trailing dot, or leading `www.`; reject malformed input. Use it as target and project directory.
2. Use requested country/language or `United States`/`en`; disclose assumptions. Use Google organic, `ignore_synonyms: true`, and `item_types: ["organic"]`.
3. The analysis authorizes calls below. Ask before retries, pagination beyond 1,000 keywords, or extras.

## DataForSEO MCP workflow

1. Call `dataforseo_labs_google_competitors_domain` with target, scope, `limit: 20`, and `exclude_top_domains: true`. Exclude target; rank by intersections, then organic ETV, descending.
2. Retain organic keyword count and ETV. If target metrics are absent, call `dataforseo_labs_google_domain_rank_overview` once.
3. For each top-five competitor, call `dataforseo_labs_google_domain_intersection` three times with `limit` no higher than 1,000:
   - shared: target1=target, target2=competitor, `intersections: true`;
   - target-only: target1=target, target2=competitor, `intersections: false`;
   - competitor-only: reverse the targets, `intersections: false`.
   Sort by volume descending. Use `total_count` for counts and items for examples.
4. Validate provider/task statuses. Never invent metrics. When `total_count` exceeds `items_count`, label samples and state coverage.

## Cost accounting

Log each call's endpoint and top-level `cost` USD. Sum unrounded values. Scope: `Total cost: x,xx USD` (decimal comma, two digits). Include zero; missing cost means incomplete subtotal; name affected calls.

## Calculations

- `overlap_pct = 100 * shared_count / max(target_organic_keyword_count, 1)`.
- For shared organic `rank_group`, `position_gap = competitor_position - target_position`; #15 versus #4 is `-11`, meaning the target trails. Average rows with both positions.
- A defensive win has a lower target position. Report strongest wins with positions, gap, volume, and available ETV.
- Group as **Direct** at overlap >=30%; **Adjacent** at >=10% and <30%; **Aspirational** below 10% when median competitor `main_domain_rank` is at least 1.5x target, or target is zero and competitor positive; otherwise **Low-overlap**. Explain the threshold.
- Use organic ETV as traffic. Calculate exactly:

  `competitive_score = min(100, 100 * target_traffic / max(sum_of_top_10_competitor_traffic, 1))`

  Sum up to ten competitors, excluding target. Round to one decimal. Interpret >30 as strong, 10-30 as mid-tier, and <10 as challenger.

## Report file and contents

Use requested report root or `<current-working-directory>/SEO`; create its normalized domain child. Sanitize components to letters, numbers, dots, hyphens, and underscores, capped at 140 characters. Write `<report-root>/<domain>/<YYYY-MM-DD>_Competitor-Report_<domain>.md`. Start with local ISO date.

Include: title/Scope with total cost; summary; Competitive Score inputs and interpretation; top-20 discovery and top-five comparison tables; shared/unique counts and examples per top-five competitor; average gaps and coverage; defensive wins; strategic groups; traffic/visibility gaps; prioritized actions; methodology; call log; timestamp; limitations; and official links. Return the absolute path and a concise summary.
