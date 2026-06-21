---
name: seo-international-opportunities
description: "Use when comparing organic opportunities across countries or languages, evaluating international search demand and existing visibility, finding localized keyword and competitor gaps, sequencing market launches, or planning country/language URL and content strategies."
compatibility: "Requires the official DataForSEO MCP server with DATAFORSEO_LABS, KEYWORDS_DATA, and SERP enabled, plus filesystem write access."
---

# SEO International Opportunities

Compare international markets without treating country or language datasets as interchangeable. Use DataForSEO MCP for every SEO metric.

## Required workflow

1. Read [references/data-contract.md](references/data-contract.md). Require a domain, the site's current language, and at least two unique target country/language combinations. Ask for all missing inputs together and wait before billable calls. Accept an optional device and report root.
2. Normalize the domain safely. Validate each target as an independent `location_name` and `language_code` market key. Do not infer a missing country or language from the domain.
3. Inspect the active schemas for Keywords for Site, Ranked Keywords, Domain Rank Overview, Competitors Domain, Domain Intersection, Keyword Overview, Search Intent, Google Trends Explore, and Google Organic Live Advanced; active schemas override examples.
4. Announce the bounded discovery budget: at most ten calls per market, reduced when fewer than three competitors exist. Ask before retries, pagination, extra competitors, or larger samples.
5. Execute the contract's workflow separately for every market. Keep raw rows, deduplication, clustering, totals, intent, rankings, competitors, terminology, and coverage inside their market key. Preserve nulls and provenance.
6. Present up to three native-term validation candidates per market and the additional call budget. Run one live Google SERP per approved candidate; approval is implicit only when the prompt pre-authorizes a bounded live shortlist.
7. Calculate the market summaries and launch score exactly as defined in the contract. Use Google Trends only for within-market direction; its normalized indices are not absolute demand and are not comparable across separate calls.
8. Identify localized clusters and literal-translation risks from observed demand, intent, competitor language, and live result composition. Label semantic mappings, translation proposals, and URL architecture judgments as analyst inferences.
9. Read [templates/report-template.md](templates/report-template.md) and write the detailed Markdown report. Use the requested root or `<current-working-directory>/SEO`; create `<root>/<domain>/`. Save `<YYYY-MM-DD>_International-Opportunities_<domain>.md`, for example `2026-06-19_International-Opportunities_example.com.md`. Begin the file with the same local ISO date and return its absolute path.

Validate provider and task statuses. Never invent missing metrics. Log every call and returned top-level cost, sum unrounded costs, and disclose incomplete cost coverage.
