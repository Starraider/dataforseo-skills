---
name: seo-competitor-gap-analysis
description: "Use when identifying a domain's true organic-search competitors, measuring keyword and traffic gaps, classifying direct, adjacent, and aspirational rivals, calculating a 0-100 Competitive Score, or producing a competitor Markdown report."
license: "(MIT AND CC-BY-SA-4.0). See LICENSE-MIT and LICENSE-CC-BY-SA-4.0"
compatibility: "Requires the official DataForSEO MCP server with the DATAFORSEO_LABS module enabled and filesystem write access."
---

# SEO Competitor Gap Analysis

Use the official [Competitors Domain](https://docs.dataforseo.com/v3/dataforseo_labs-google-competitors_domain-live/) and [Domain Intersection](https://docs.dataforseo.com/v3/dataforseo_labs-google-domain_intersection-live/) documentation.

## Input and scope

1. If no domain was supplied, ask and wait. Accept a hostname or HTTP(S) URL. Normalize to a lowercase hostname without credentials, port, path, query, fragment, trailing dot, or leading `www.`; reject malformed input.
2. Use the requested country and language, otherwise `United States` and `en`; disclose assumptions. Use Google organic results, `ignore_synonyms: true`, and `item_types: ["organic"]`.
3. The analysis authorizes the billable calls below. Ask before retries, pagination beyond 1,000 keywords, or extra endpoints.

## DataForSEO MCP workflow

1. Call `dataforseo_labs_google_competitors_domain` with target, scope, `limit: 20`, and `exclude_top_domains: true`. Cap at 20 competitors, exclude the target, then rank by `intersections` descending and organic ETV descending.
2. Retain full organic keyword count and ETV for the target and candidates. If target metrics are absent, call `dataforseo_labs_google_domain_rank_overview` once.
3. For each top-five competitor, call `dataforseo_labs_google_domain_intersection` three times with `limit` no higher than 1,000:
   - shared: target1=target, target2=competitor, `intersections: true`;
   - target-only: target1=target, target2=competitor, `intersections: false`;
   - competitor-only: reverse the targets, `intersections: false`.
   Sort by search volume descending. Use `total_count` for shared/unique counts and returned items for examples.
4. Validate provider and task statuses. Never invent metrics. When `total_count` exceeds `items_count`, label averages and examples as sampled and state coverage.

## Calculations

- `overlap_pct = 100 * shared_count / max(target_organic_keyword_count, 1)`.
- For shared organic `rank_group`, `position_gap = competitor_position - target_position`; target #15 versus competitor #4 is `-11`, so negative means the target trails. Average rows containing both positions.
- A defensive win has target position lower numerically than competitor position. Report strongest wins with positions, gap, search volume, and ETV when available.
- Group as **Direct** at overlap >=30%; **Adjacent** at >=10% and <30%; **Aspirational** below 10% only when median competitor `main_domain_rank` is at least 1.5x the target median, or target is zero and competitor positive; otherwise **Low-overlap**. Explain this operational threshold.
- Use organic ETV as traffic. Calculate exactly:

  `competitive_score = min(100, 100 * target_traffic / max(sum_of_top_10_competitor_traffic, 1))`

  Sum up to ten competitors excluding the target. Round to one decimal. Interpret >30 as strong, 10-30 inclusive as mid-tier, and <10 as challenger.

## Report file and contents

Use the requested directory or `<current-working-directory>/SEO`; create it. Sanitize the target to letters, numbers, dots, hyphens, and underscores; replace other runs with `_`, trim separators, cap at 140 characters. Write `<YYYY-MM-DD>_Competitor-Report_<domain>.md` using the normalized safe domain. The first line is the local ISO date.

Include: title/scope; executive summary; Competitive Score inputs and interpretation; top-20 discovery and top-five comparison tables; shared/unique counts and examples per top-five competitor; average gaps and coverage; defensive wins; strategic groups; traffic/visibility gaps; prioritized actions; methodology; MCP calls; timestamp; limitations; and official links. Return the absolute path and a concise summary.
