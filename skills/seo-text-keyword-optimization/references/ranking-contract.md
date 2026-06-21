# Ranking contract

Follow the official [Related Keywords endpoint](https://docs.dataforseo.com/v3/dataforseo_labs-google-related_keywords-live/) and [Keyword Difficulty guidance](https://dataforseo.com/help-center/what-is-keyword-difficulty-and-how-is-it-calculated). Organic keyword difficulty is the competition signal. Google Ads `competition` and `competition_level` describe paid placement and are supporting context only.

## Response paths

Read rows from `tasks[].result[].items[].keyword_data`:

- keyword: `keyword`
- demand: `keyword_info.search_volume`
- Ads competition: `keyword_info.competition` and `keyword_info.competition_level`
- organic difficulty: `keyword_properties.keyword_difficulty`
- detected language: `keyword_properties.detected_language` and `keyword_properties.is_another_language`
- intent: `search_intent_info.main_intent`
- freshness: `keyword_info.last_updated_time`

Validate response and task status `20000`, non-null result arrays, and the requested versus returned count for every seed.

## Normalize and filter

Create a key by Unicode NFKC normalization, case-folding, trimming surrounding punctuation, and collapsing whitespace. Merge matching keys across seeds and preserve every seed as provenance. If duplicate metrics conflict, show the conflict and rank conservatively with the lowest non-null volume and highest non-null difficulty.

Exclude exact seeds, wrong-language rows, irrelevant or intent-mismatched terms, unrelated third-party brands, zero/null volume, and null difficulty. Record each exclusion reason. Judge relevance against the supplied text, not against the seed alone.

## Prioritize

For each remaining row calculate:

`opportunity = search_volume / (keyword_difficulty + 10)`

Build the final list in difficulty bands: Easy `0-29`, Achievable `30-39`, then Moderate `40-49`. Within each band sort by opportunity descending, search volume descending, difficulty ascending, then keyword ascending. Stop at 20. Do not use difficulty `50+` or incomplete rows as low-hanging fruit. If fewer than 20 qualify, return the supported number and explain the shortfall rather than weakening the label.

For each selected keyword report rank, keyword, seed provenance, volume, difficulty, difficulty band, Ads competition, intent, opportunity rounded to two decimals, and current-text coverage (`present`, `partial`, or `absent`).
