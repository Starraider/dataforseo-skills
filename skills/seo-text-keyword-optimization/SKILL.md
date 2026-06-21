---
name: seo-text-keyword-optimization
description: "Use when optimizing supplied prose such as a blog post or news article from one to three seed keywords, finding and deduplicating related keywords, prioritizing low-difficulty search demand, or producing three evidence-based text optimization approaches."
---

# SEO Text Keyword Optimization

Use the official DataForSEO MCP server for all keyword evidence. Treat search volume as search demand, not actual page traffic.

## Inputs

1. Require the complete text, pasted or in a readable local text/Markdown file, and one to three non-empty seed keywords. Ask for all missing or invalid inputs and wait without making billable calls.
2. Accept optional location, language, and report root. Default to `United States` and `en`, and disclose this scope. If the text and seeds clearly conflict with English, ask for the intended market instead of guessing.
3. Read [references/ranking-contract.md](references/ranking-contract.md) before making calls.

## DataForSEO MCP workflow

1. Inspect the active schema for `dataforseo_labs_google_related_keywords`; it overrides examples. Announce the normal budget of one billable call per seed.
2. For every seed, call the tool once with the same market, `depth: 2`, `limit: 50`, `include_seed_keyword: false`, `ignore_synonyms: true`, and descending search-volume order when those arguments exist. Use only exposed arguments.
3. Validate top-level and task statuses. Record each call's endpoint, top-level `cost`, returned count, and coverage. Do not retry, paginate, or add calls without permission.
4. Extract keyword, search volume, organic keyword difficulty, Ads competition, intent, language, and update time from documented response paths. Never invent or coerce missing metrics.
5. Apply the ranking contract: deduplicate the combined pool, filter for textual and intent relevance, calculate opportunity only for complete rows, and return the best 20 supported low-hanging-fruit candidates.

## Optimization approaches

Produce three materially different proposals, such as a light-touch edit, a structural rewrite, and a coverage expansion. For each, name its primary and supporting keywords, specify exact insertion or revision points, give example headings or short replacement snippets, explain search-intent fit, and state the editorial tradeoff. Recommend one. Preserve the source's facts and voice; do not keyword-stuff or claim rankings.

## Report

Write a detailed Markdown report beginning with the local ISO date. Include scope and assumptions, a text synopsis, per-seed coverage, deduplication and exclusion counts, the sorted top-20 table, current-text coverage, three proposals, recommendation, methodology, limitations, official sources, and call log.

Sum unrounded costs and show `Total cost: x,xx USD`; report missing cost as an incomplete subtotal. Save under the requested root or `<cwd>/SEO`, in `text-keyword-optimization/<YYYY-MM-DD>_Text-Keyword-Optimization_<safe-first-seed>.md`. Return the absolute path and a concise summary.
