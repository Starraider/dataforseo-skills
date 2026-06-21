# International opportunities data contract

Use the active DataForSEO MCP schemas as authoritative. The endpoint names and limits below define the intended workflow, not permission to repair a failed call with unapproved retries.

## Official sources

- [Keywords for Site](https://docs.dataforseo.com/v3/dataforseo_labs/google/keywords_for_site/live/)
- [Ranked Keywords](https://docs.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live/)
- [Domain Rank Overview](https://docs.dataforseo.com/v3/dataforseo_labs/google/domain_rank_overview/live/)
- [Competitors Domain](https://docs.dataforseo.com/v3/dataforseo_labs/google/competitors_domain/live/)
- [Domain Intersection](https://docs.dataforseo.com/v3/dataforseo_labs/google/domain_intersection/live/)
- [Keyword Overview](https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_overview/live/)
- [Search Intent](https://docs.dataforseo.com/v3/dataforseo_labs/google/search_intent/live/)
- [Google Trends Explore](https://docs.dataforseo.com/v3/keywords_data/google_trends/explore/live/)
- [Google Organic Live Advanced](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/)
- [DataForSEO: location and language](https://dataforseo.com/help-center/location-and-language-in-api-connector)
- [DataForSEO: search volume](https://dataforseo.com/help-center/what-is-search-volume)
- [DataForSEO: Google Trends limits](https://dataforseo.com/help-center/google-trends-api-limits-and-restrictions)

## Inputs and normalization

Require all of:

- `domain`: hostname or HTTP(S) URL. Normalize to a lowercase hostname without credentials, port, path, query, fragment, trailing dot, or leading `www.`. Reject malformed input.
- `current_language`: the language of the site's existing primary content. Keep the user's label and normalize a compatible language code separately.
- `targets`: at least two unique `{country, language_code}` pairs. Use the full DataForSEO country name as `location_name` and an accepted language code.

Optional inputs are current country, exact strategic constraints, device, report root, supplied competitors, and a pre-approved live validation count. Default device to desktop and report root to `SEO/`. Do not invent a current country or complete a partial target pair.

Define `market_key = <location_name>|<language_code>`. The same country with two languages and the same language in two countries are distinct markets.

## Budget and call sequence

The initial budget is at most ten calls per market. It falls by one for every unavailable competitor below three. Steps 7, 8, and 9 are each one batch call, not one call per keyword. Approved live validation in step 10 adds up to three calls per market.

For each market, create a new dataset and run:

1. `dataforseo_labs_google_keywords_for_site`: normalized target, market location/language, `include_subdomains: true`, `limit: 200`, ordered by relevance and then search volume descending.
2. `dataforseo_labs_google_ranked_keywords`: same target and market, `include_subdomains: true`, `item_types: ["organic"]`, `limit: 200`, ordered by search volume descending.
3. `dataforseo_labs_google_domain_rank_overview`: same target and market with `ignore_synonyms: true`.
4. `dataforseo_labs_google_competitors_domain`: same target and market, `exclude_top_domains: true`, `ignore_synonyms: true`, organic items, `limit: 10`. Exclude the target and sort by intersections, then organic ETV.
5. For each of the top three available competitors, call `dataforseo_labs_google_domain_intersection` with competitor as `target1`, project domain as `target2`, `intersections: false`, organic items, `ignore_synonyms: true`, `limit: 200`, and search-volume-descending order. These are competitor-only gaps.
6. Build a market-local candidate set of at most 500 terms from up to 200 Ranked Keywords, 150 Keywords for Site terms, and 50 competitor-only terms from each of up to three competitors. Reserve up to 20 slots for analyst-proposed literal variants that must be checked against observed native alternatives; displace the lowest-priority gap terms rather than exceeding 500. Deduplicate case-insensitively only inside this market and preserve every source.
7. `dataforseo_labs_google_keyword_overview`: the market-local candidate set with the same location/language. Retain keyword, search volume, monthly searches, CPC, paid competition, keyword difficulty when returned, and timestamps.
8. `dataforseo_labs_search_intent`: the same candidate set and language. Retain main intent and probabilities. This endpoint is language-scoped rather than country-scoped, so label that limitation. If the language is unsupported, report intent unavailable; never substitute another language.
9. `kw_data_google_trends_explore`: up to five native cluster-head candidates in one request, the same location/language, web search, `past_5_years`, and graph items. Trend values are relative within that request.
10. After approval, call `serp_organic_live_advanced` once for each of up to three candidates per market with Google, the same market, selected device, `depth: 20`, and one crawl page. Record capture time, dominant organic result types, top ranking domains/URLs, visible terminology, and intent consistency.

Do not paginate, retry, expand competitor counts, or validate more live keywords without approval. Validate HTTP/provider/task statuses and non-empty result arrays before analysis.

## Isolation and coverage rules

- Store raw and derived data under its `market_key`; include the key on every table row.
- Never merge, deduplicate, average, or sum keyword volumes, positions, intent, competitors, or terminology across market keys.
- A repeated spelling in two markets remains two observations.
- Compare markets only through independently calculated summary metrics with identical sample caps.
- Label `total_count` versus returned item count and all capped tables as samples.
- Do not compare Google Trends indices from separate market calls as if they were absolute or on one shared scale.
- Do not claim an absent ranking, keyword, or competitor beyond the sampled and provider-reported coverage.

## Market analysis

### Localized clusters

Cluster terms within one market by meaning, user task, and intent. Merge spelling variants only when their likely need and live result composition agree. Split terms whose spelling is similar but intent or SERP composition differs. Name clusters using the observed native term, not a literal source-language translation.

For each cluster report the head term, related terms, main intent, head-term volume, sampled volume, difficulty, current best rank/URL, competitor coverage, trend direction, and recommended page type. `sampled volume` is a directional sum of returned keyword estimates, not unique searchers.

### Translation-risk flags

Map a current-language concept to a target-market term only when semantics are defensible, and label the mapping as analyst inference. Source concepts may come from returned target SERP titles/descriptions, URLs, or user-supplied content; if these do not expose the current-language concept, recommend native-speaker research instead of inventing it. Flag **localize, do not translate literally** when any observed condition applies:

- the native alternative has at least twice the literal variant's target-market volume;
- the literal variant is absent or zero-volume while the native alternative has demand;
- DataForSEO intent or the live result composition differs materially;
- local competitors and live results consistently use a different term, modifier, unit, spelling, or content format.

Validate both literal and native variants with Keyword Overview when they are used in a volume comparison. Never fabricate a translation. If no defensible equivalent is available, recommend native-speaker research.

### Existing visibility and competitor strength

Use Domain Rank Overview for provider-reported organic keyword count, ETV, and ranking distribution. Supplement with the Ranked Keywords sample's best position, top-10 count, URLs, and ETV. Keep provider totals separate from sample counts.

For the top three competitors report intersections, organic keyword count, organic ETV, and `main_domain_rank` when returned. Define market competitor strength as the median available `main_domain_rank` of those domains; also show median organic ETV. Do not replace missing values with zero.

### Comparable market summaries

Calculate these raw values independently per market using fixed caps:

- `demand_raw`: sum of non-null head-term search volume for the top 20 localized clusters by head-term volume.
- `gap_raw`: sum of non-null head-term volume for the top 20 competitor-only clusters for which the target has no returned ranking.
- `foothold_raw`: provider organic ETV for the target.
- `kd_access_raw`: `(100 - median_KD) / 100`, using KD on the top 20 opportunity clusters and clamping to 0-1.
- `competitor_strength_raw`: median available `main_domain_rank` for the top three competitors.

Across the independently calculated market summaries, min-max normalize `log1p(demand_raw)`, `log1p(gap_raw)`, and `log1p(foothold_raw)` to 0-1. Normalize competitor strength across markets, invert it, and define `accessibility = mean(kd_access_raw, 1 - normalized_competitor_strength)`. If every market has the same value, use `0.5` for that normalized component.

Calculate only when every component is available:

`market_opportunity_score = round(100 * (0.35 * demand + 0.25 * gap + 0.20 * foothold + 0.20 * accessibility), 1)`

This score compares the supplied markets; it is not a universal benchmark. Do not reweight missing components. Mark the score unavailable and give a qualitative launch order with the missing evidence named. Break score ties by lower localization complexity, then lower competitor strength; disclose both judgments.

## URL and launch recommendations

Recommend one primary architecture and exact example paths. Preserve an effective existing architecture unless evidence and operating constraints justify a change.

- Prefer a gTLD subdirectory such as `/de-de/` when markets share a brand, authority, platform, and governance.
- Recommend a language-only directory such as `/de/` only when one version genuinely serves every target country using that language.
- Recommend a country-language directory such as `/en-gb/` when offers, terminology, intent, legal requirements, or SERPs differ by country.
- Recommend a subdomain only for a meaningfully separate platform or operating team.
- Recommend a ccTLD only for a country-specific business with the resources to build and maintain separate local authority.

For each priority cluster give the target market, page type, localized slug, example URL, source/current page when applicable, create/localize/consolidate decision, and launch wave. Include self-canonical and reciprocal hreflang implementation notes, but label architecture as strategic guidance rather than a DataForSEO ranking guarantee.

## Cost and provenance

Log endpoint, market key, purpose, status, returned top-level `cost` in USD, and timestamp for every call. Sum unrounded values and display `Total cost: x,xx USD` using a decimal comma and two digits. Include zero. If any cost is absent, label the subtotal incomplete and name the affected calls.
