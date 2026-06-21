# DataForSEO MCP SEO workflows

The sequences below use exact captured tool names. Confirm every name and argument against the active schema before calling it. Values are examples, not defaults. Each call can be billable.

Parsed-response examples are deliberately normalized analysis records, not claims that the MCP returns those compact objects directly.

## Keyword difficulty analysis

For a supplied list, make one call:

```json
{
  "tool": "dataforseo_labs_bulk_keyword_difficulty",
  "arguments": {
    "keywords": ["technical seo audit", "seo audit checklist"],
    "location_name": "United States",
    "language_code": "en"
  }
}
```

For discovery, first call `dataforseo_labs_google_related_keywords` with the seed, market, `depth`, and a conservative `limit`; deduplicate returned `keyword_data.keyword`; then call Bulk Keyword Difficulty once for the unique list. If volume, CPC, intent, and monthly searches are required for an arbitrary supplied list, call `dataforseo_labs_google_keyword_overview` for up to 700 terms.

Normalized parsed result:

```json
{
  "keyword": "technical seo audit",
  "location": "United States",
  "language": "en",
  "keyword_difficulty": 42,
  "difficulty_scale": "0-100",
  "source_tool": "dataforseo_labs_bulk_keyword_difficulty"
}
```

Do not label Google Ads `competition` as organic Keyword Difficulty.

## Live SERP snapshot

1. If the location string is uncertain, call `serp_locations` with `country_iso_code`, optional `location_name`, optional `location_type`, and `search_engine`.
2. Call `serp_organic_live_advanced`:

```json
{
  "keyword": "technical seo consultant",
  "language_code": "en",
  "location_name": "Austin,Texas,United States",
  "search_engine": "google",
  "device": "desktop",
  "depth": 100,
  "max_crawl_pages": 1
}
```

Parse organic results separately from paid, local pack, featured snippet, people-also-ask, and other item types. Retain `rank_group`, `rank_absolute`, domain, URL, title, and the result timestamp when present.

```json
{
  "keyword": "technical seo consultant",
  "captured_at": "provider timestamp",
  "organic": [{"rank_group": 1, "rank_absolute": 3, "domain": "example.com", "url": "https://example.com/"}],
  "features": ["local_pack", "people_also_ask"]
}
```

## Backlink profile extraction

1. Call `backlinks_summary` with the normalized domain and explicit subdomain/internal-link policy.
2. Call `backlinks_backlinks` with `target`, `mode`, `limit`, optional filters, and order. Start with `mode: "one_per_domain"` for prospecting or `as_is` for link-level extraction.
3. Paginate with `offset` only when required. Use `backlinks_referring_domains`, `backlinks_anchors`, or `backlinks_referring_networks` for grouped evidence instead of reconstructing every aggregate from a partial link sample.

```json
{
  "target": "example.com",
  "mode": "one_per_domain",
  "limit": 100,
  "offset": 0,
  "order_by": ["rank,desc"]
}
```

Normalized result:

```json
{
  "target": "example.com",
  "summary": {"backlinks": 1200, "referring_domains": 240},
  "sample": [{"domain_from": "referrer.example", "dofollow": true, "rank": 71}],
  "coverage": {"returned": 100, "total": 1200, "mode": "one_per_domain"}
}
```

## Local search audit

1. Resolve the exact city/region string with `serp_locations`.
2. For each approved keyword, call `serp_organic_live_advanced` with the exact `location_name`, language, and device. Extract local-pack and organic visibility independently.
3. If business-listing evidence is required, call `business_data_business_listings_search` with a `location_coordinate` radius and optional categories/title. This tool has no free-form location-name argument.
4. Compare name/address/contact/category/rating fields only when present; do not infer listing ownership or NAP consistency from absent fields.

```json
{
  "location_coordinate": "30.2672,-97.7431,10",
  "categories": ["seo agency"],
  "limit": 100,
  "order_by": ["rating.value,desc"]
}
```

Use the same market, language, device, and capture time across competitors. A local audit through this catalog is a search/listing audit, not access to Google Business Profile private account data.

## Ranking history over time

For aggregate domain visibility, call `dataforseo_labs_google_historical_rank_overview` once:

```json
{
  "target": "example.com",
  "location_name": "United States",
  "language_code": "en",
  "ignore_synonyms": true
}
```

For a keyword-level history, call `dataforseo_labs_google_historical_serps` once per approved keyword and date range, then match normalized target domains in the returned organic items:

```json
{
  "keyword": "technical seo audit",
  "location_name": "United States",
  "language_code": "en",
  "date_from": "2026-01-01",
  "date_to": "2026-06-01"
}
```

Use `dataforseo_labs_google_ranked_keywords` for a current domain baseline, not as a historical time series. Normalize output as:

```json
{
  "keyword": "technical seo audit",
  "target": "example.com",
  "observations": [
    {"date": "2026-01-01", "rank_group": 12, "url": "https://example.com/a"},
    {"date": "2026-06-01", "rank_group": 7, "url": "https://example.com/a"}
  ]
}
```

Missing observations mean no matching returned result at that snapshot/depth, not rank zero.

## Competitor and keyword gap

1. Discover organic competitors with `dataforseo_labs_google_competitors_domain` or `dataforseo_labs_google_serp_competitors`.
2. Call `dataforseo_labs_google_domain_intersection` for domain keyword overlap or `dataforseo_labs_google_page_intersection` for URL-level overlap.
3. Use `dataforseo_labs_bulk_traffic_estimation` and Bulk Keyword Difficulty only for the approved candidate set.
4. Keep paid and organic items separate and record whether subdomains are included.

For backlink gaps, use `backlinks_competitors`, then `backlinks_domain_intersection` or `backlinks_page_intersection`. Do not merge link gaps with keyword gaps into one undocumented score.

## Single-page technical audit

1. Call `on_page_instant_pages` for page-level optimization and issue evidence.
2. Call `on_page_content_parsing` only when structured headings, anchors, links, or primary text are required.
3. Call `on_page_lighthouse` for Lighthouse categories and audits; request `full_data: true` only when the report needs fields excluded by the reduced response.

All three require an absolute HTTP(S) URL. Keep provider findings, Lighthouse findings, and analyst recommendations distinct. Report crawl/render configuration such as JavaScript, user agent, and Accept-Language.

## Failure and coverage record

For every workflow, preserve a call log:

```json
{
  "tool": "serp_organic_live_advanced",
  "scope": {"keyword": "technical seo consultant", "location": "Austin,Texas,United States", "device": "desktop", "depth": 100},
  "status_code": 20000,
  "cost_usd": 0.0,
  "returned_items": 0,
  "limitations": ["Example structure; use the actual returned cost and item count"]
}
```

Never replace a missing cost with an assumed price. Sum only costs actually returned and disclose incomplete cost coverage.
