---
name: seo-keyword-research
description: "Use when researching keywords for a website domain, finding related or long-tail terms, grouping intent, scoring opportunities, calculating a 0-100 Keyword Score, or producing a Markdown report."
license: "(MIT AND CC-BY-SA-4.0). See LICENSE-MIT and LICENSE-CC-BY-SA-4.0"
compatibility: "Requires the official DataForSEO MCP server with the DATAFORSEO_LABS module enabled and filesystem write access."
---

# Keyword Research and Opportunity Scoring

Follow the official [Related Keywords](https://docs.dataforseo.com/v3/dataforseo_labs-google-related_keywords-live/), [Suggestions](https://docs.dataforseo.com/v3/dataforseo_labs-google-keyword_suggestions-live/), [Ranked Keywords](https://docs.dataforseo.com/v3/dataforseo_labs-google-ranked_keywords-live/), and [Bulk KD](https://docs.dataforseo.com/v3/dataforseo_labs-google-bulk_keyword_difficulty-live/) documentation.

## Input

1. Require a project domain. If absent, ask and wait, even when a seed exists. Use a supplied seed for seed mode; without one, use the domain for domain mode. When both exist, default to seed mode unless domain mode is explicit.
2. Default to `location_name: "United States"`, `language_code: "en"`; honor overrides and disclose scope.
3. Normalize the domain to a lowercase hostname without credentials, port, URL suffix, trailing dot, or leading `www.`. Reject malformed input.

## DataForSEO MCP workflow

The request authorizes these billable calls only. Ask before retries, pagination, or extras.

- **Seed:** call `dataforseo_labs_google_related_keywords` with `limit: 200`, then `dataforseo_labs_google_keyword_suggestions` with `limit: 100`.
- **Domain:** call `dataforseo_labs_google_ranked_keywords` with the normalized target, `limit: 100`, `item_types: ["organic"]`, and search-volume-descending order.
- Deduplicate case-insensitively, preserve sources, and call `dataforseo_labs_bulk_keyword_difficulty` once for up to 1,000 unique keywords; merge KD by normalized keyword.
- Validate statuses. Extract keyword, volume, CPC, Ads competition/level, KD, intent, and rank/URL. Never invent metrics; disclose counts and coverage.

## Analysis

Classify one intent in precedence: URL/domain or brand navigation -> **Navigational**; `buy`, `price`, `deal`, `near me`, or brand+product -> **Transactional**; `best`, `review`, `comparison`, or `vs` -> **Commercial**; `how to`, `what is`, `guide`, or `tutorial` -> **Informational**. Otherwise use `main_intent`, then **Informational (inferred)**. Explain ambiguity.

With both metrics calculate:

`opportunity = search_volume / (keyword_difficulty + 10)`

Sort descending and surface 20. Never coerce missing values to zero.

For Keyword Score, let `K` be up to 50 top opportunity rows. Show each component:

- volume = `30 * min(1, log10(1 + average_search_volume(K)) / 5)`;
- low difficulty = `25 * count(KD < 30) / count(valid KD in K)`;
- intent diversity = `15 * distinct_intent_buckets(K) / 4`;
- CPC = `15 * min(1, log10(1 + average_CPC_USD(K)) / log10(11))`;
- long-tail = `15 * min(1, breadth / 100)`, where breadth is suggestions in seed mode or ranked keywords of at least four words in domain mode (label as proxy).

Sum without reweighting, clamp 0-100, and round to one decimal. Score unavailable components zero and disclose them. Justify using the strongest and weakest signals.

## Report

Use the requested report root or `<current-working-directory>/SEO`; create its normalized domain child. Allow letters, numbers, dots, hyphens, and underscores; replace other runs with `_`, trim separators, and cap components at 140 characters. Write `<report-root>/<domain>/<YYYY-MM-DD>_Keyword-Analysis_<target>.md`, sanitizing the seed/domain target separately. Default: `SEO/<domain>/<filename>`. Start with the local ISO date.

Include scope; summary; score components; top-20 opportunities; intent groups; related keywords; suggestions/proxy; deduplicated metrics; content priorities; formulas; MCP calls, cost scope, timestamp, coverage, limitations, and official links. Return the absolute path and summary.
