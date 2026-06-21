---
name: seo-page-metadata
description: "Use when analyzing one webpage's main topic, researching low-competition keyword opportunities, or generating evidence-based title, meta description, Open Graph, Twitter Card, and meta-keywords suggestions in a Markdown report."
compatibility: "Requires the official DataForSEO MCP server with the ONPAGE and DATAFORSEO_LABS modules enabled and filesystem write access."
---

# SEO Page Metadata

Follow the official [Instant Pages](https://docs.dataforseo.com/v3/on_page/instant_pages/), [Content Parsing](https://docs.dataforseo.com/v3/on_page-content_parsing-live/), [Related Keywords](https://docs.dataforseo.com/v3/dataforseo_labs-google-related_keywords-live/), and [Keyword Difficulty](https://dataforseo.com/help-center/what-is-keyword-difficulty-and-how-is-it-calculated) documentation.

## Input

Require an absolute HTTP(S) URL; ask and wait when absent. Reject credentials, malformed URLs, and other schemes. Preserve it for analysis. Normalize the report hostname to lowercase without port, trailing dot, or leading `www.`. Accept market and report-root overrides.

## DataForSEO MCP workflow

Ask before retries or extra calls.

1. Call `on_page_instant_pages`. Capture status, final URL, title, description, meta keywords, canonical, and social tags only for the current-metadata audit. Never use metadata, canonical, domain, path, or TLD to infer topic, intent, geography, or seeds.
2. Call Content Parsing using only exposed parameters. Exclude navigation, footer, and boilerplate. Parsed primary content and headings are the sole evidence for topic, intent, geography, seeds, and truthful suggestions.
3. Accept geography only when primary content defines a market, service/delivery area, or audience. A footer address alone is insufficient. Resolve cities/regions to countries only when unambiguous. User market overrides win; disclose conflicts. Otherwise use the content country, falling back to `United States`/`en` with disclosure.
4. Derive exactly five non-brand seeds solely from primary content. Prefer 2-4 words, allowing longer geographically qualified seeds. Add supported geography naturally to applicable seeds, especially local offerings. Justify each with content evidence.
5. For each seed call `dataforseo_labs_google_related_keywords` with the selected market, `depth: 2`, `limit: 25`, and descending volume. Preserve provenance. Request seed exclusion only if the schema supports it; otherwise remove seed rows during normalization.
6. Validate statuses. Extract keyword, volume, `keyword_properties.keyword_difficulty`, Ads competition, CPC, and seed. Keep missing metrics null.

## Low-hanging-fruit selection

Normalize Unicode/whitespace; deduplicate case-insensitively while merging provenance. Remove brand/navigation noise and unsupported terms. For rows with volume and KD calculate `opportunity = search_volume / (keyword_difficulty + 10)`. Rank by opportunity, volume, then lower KD; select 20. Distinguish organic KD from paid Ads competition. Report any shortfall.

## Metadata suggestions

Write three truthful options each, with counts: Page Title (50-60), Meta Description (140-160), Meta Keywords (note Google ignores them), Open Graph Title (55-65), Open Graph Description (140-180), Twitter Title (55-65), and Twitter Description (125-160). Match content language and intent; avoid stuffing and unsupported claims.

## Cost and report

Log endpoint costs; sum unrounded USD as `Total cost: x,xx USD`. Name calls missing cost and mark the subtotal incomplete.

Report scope, market source, current metadata, primary-content evidence, geography, five seeds, coverage counts, top-20 metrics/provenance, 21 options, guidance, limitations, formula, call log, timestamp, and official references. State that metadata was excluded from derivation.

Use the requested root or `<cwd>/SEO`; create `<root>/<domain>/`. Sanitize the URL to letters, numbers, dots, hyphens, and underscores, capped at 140 characters. Save `<YYYY-MM-DD>_Page-Metadata_<safe-URL>.md`, beginning with the local date. Return its absolute path and summary.
