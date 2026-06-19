---
name: seo-keyword-research
description: "Use when researching keywords from a seed term or domain, finding related and long-tail terms, grouping search intent, scoring SEO opportunities, calculating a 0-100 Keyword Score, or producing a detailed keyword-analysis Markdown report."
license: "(MIT AND CC-BY-SA-4.0). See LICENSE-MIT and LICENSE-CC-BY-SA-4.0"
compatibility: "Requires the official DataForSEO MCP server with the DATAFORSEO_LABS module enabled and filesystem write access."
---

# Keyword Research and Opportunity Scoring

Follow the official [Related Keywords](https://docs.dataforseo.com/v3/dataforseo_labs-google-related_keywords-live/), [Suggestions](https://docs.dataforseo.com/v3/dataforseo_labs-google-keyword_suggestions-live/), [Ranked Keywords](https://docs.dataforseo.com/v3/dataforseo_labs-google-ranked_keywords-live/), and [Bulk KD](https://docs.dataforseo.com/v3/dataforseo_labs-google-bulk_keyword_difficulty-live/) documentation.

## Input

1. Require one seed keyword or domain. If absent, ask and wait; if both appear, ask which to use.
2. Default to `location_name: "United States"`, `language_code: "en"`; honor `--location` and `--language` overrides and disclose scope.
3. Normalize domains to lowercase hostnames without credentials, port, URL suffix, trailing dot, or `www.`. Reject malformed input.

## DataForSEO MCP workflow

The request authorizes these billable calls only. Ask before retries, pagination, or extras.

- **Seed:** call `dataforseo_labs_google_related_keywords` with `limit: 200`, then `dataforseo_labs_google_keyword_suggestions` with `limit: 100`.
- **Domain:** call `dataforseo_labs_google_ranked_keywords` with the normalized target, `limit: 100`, `item_types: ["organic"]`, and search-volume-descending order.
- Deduplicate case-insensitively and preserve sources. Call `dataforseo_labs_bulk_keyword_difficulty` once for all unique keywords (maximum 1,000); merge KD by normalized keyword.
- Validate provider/task statuses. Extract keyword, volume, CPC, Ads competition/level, KD, intent, and applicable rank/URL. Never invent metrics; disclose `total_count`, `items_count`, and coverage.

## Analysis

Classify one primary intent in this precedence: URL/domain or clear brand navigation -> **Navigational**; `buy`, `price`, `deal`, `near me`, or brand+product -> **Transactional**; `best`, `review`, `comparison`, or `vs` -> **Commercial**; `how to`, `what is`, `guide`, or `tutorial` -> **Informational**. Otherwise use DataForSEO `main_intent`; if absent, use **Informational (inferred)**. Explain ambiguity.

With both metrics calculate:

`opportunity = search_volume / (keyword_difficulty + 10)`

Sort descending; surface 20. Never coerce missing values to zero.

For Keyword Score, let `K` be up to 50 top opportunity rows. Show each component:

- volume = `30 * min(1, log10(1 + average_search_volume(K)) / 5)`;
- low difficulty = `25 * count(KD < 30) / count(valid KD in K)`;
- intent diversity = `15 * distinct_intent_buckets(K) / 4`;
- CPC = `15 * min(1, log10(1 + average_CPC_USD(K)) / log10(11))`;
- long-tail = `15 * min(1, breadth / 100)`, where breadth is returned suggestions in seed mode and returned ranked keywords of at least four words in domain mode (label this proxy).

Sum without reweighting, clamp 0-100, and round to one decimal. Score unavailable components zero and disclose them. Justify the score in one sentence using its strongest and weakest signals.

## Report

Use the requested directory or `<current-working-directory>/SEO`; create it. Sanitize the target to letters, numbers, dots, hyphens, and underscores; replace other runs with `_`, trim separators, cap at 140 characters. Write `<YYYY-MM-DD>_Keyword-Analysis_<target>.md` with local date as the first line.

Include scope; summary; Keyword Score components; top-20 opportunities; intent distribution/groups; related keywords; suggestions/proxy; complete deduplicated metrics; prioritized content opportunities; formulas; MCP calls, cost scope, timestamp, coverage, limitations, and official links. Return the absolute path and concise summary.
