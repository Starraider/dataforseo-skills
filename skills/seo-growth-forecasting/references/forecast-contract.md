# SEO growth forecasting contract

Use the active DataForSEO MCP schemas as authoritative. The forecast is a planning model, not a prediction or guarantee.

## Official sources

- [Domain Rank Overview](https://docs.dataforseo.com/v3/dataforseo_labs/google/domain_rank_overview/live/)
- [Relevant Pages](https://docs.dataforseo.com/v3/dataforseo_labs/google/relevant_pages/live/)
- [Ranked Keywords](https://docs.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live/)
- [Keyword Overview](https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_overview/live/)
- [Bulk Keyword Difficulty](https://docs.dataforseo.com/v3/dataforseo_labs/google/bulk_keyword_difficulty/live/)
- [Historical Keyword Data](https://docs.dataforseo.com/v3/dataforseo_labs/google/historical_keyword_data/live/)
- [Historical Rank Overview](https://docs.dataforseo.com/v3/dataforseo_labs/google/historical_rank_overview/live/)
- [Google Trends Explore](https://docs.dataforseo.com/v3/keywords_data/google_trends/explore/live/)
- [How DataForSEO calculates ETV](https://dataforseo.com/help-center/how-is-etv-calculated)
- [How DataForSEO calculates Keyword Difficulty](https://dataforseo.com/help-center/what-is-keyword-difficulty-and-how-is-it-calculated)
- [Google Trends API limits and restrictions](https://dataforseo.com/help-center/google-trends-api-limits-and-restrictions)

## Inputs and scope

Require all of:

- `domain`: hostname or HTTP(S) URL, normalized to a hostname.
- `country`: full DataForSEO country name used as `location_name`.
- `language`: accepted DataForSEO language code used as `language_code`.
- `forecast_period`: a positive number of calendar months or explicit future start/end months. Start with the next complete calendar month when only a duration is supplied.

Optional inputs are priority page URLs, page-level business tiers (`high`, `medium`, `low`), a custom position CTR curve, and report root. Normalize supplied pages but retain their absolute URLs. Reject pages outside the domain. A custom curve must supply numeric values from 0 to 1, be non-increasing as rank worsens, and be documented verbatim.

Use Google organic, `include_subdomains: true` where supported, and `ignore_synonyms: true` where supported. Do not silently substitute a country, language, or forecast period.

## Data acquisition

1. Call `dataforseo_labs_google_domain_rank_overview` for the current provider baseline.
2. Call `dataforseo_labs_google_historical_rank_overview` for historical organic ETV, keyword count, and position buckets.
3. Call `dataforseo_labs_google_relevant_pages` with organic items, `limit: 100`, and organic ETV descending.
4. Call `dataforseo_labs_google_ranked_keywords` with organic items, `limit: 1000`, and organic ETV then search volume descending.
5. Build at most 500 candidates. Include supplied priority pages first, then favor positions 4-50, current ETV, search volume, and high business value. Retain positions 51-100 for expected and ambitious scenarios. Exclude positions 1-3 from opportunity ranking unless a scenario has positive modeled gain.
6. Batch candidates through `dataforseo_labs_google_keyword_overview`, `dataforseo_labs_bulk_keyword_difficulty`, and `dataforseo_labs_google_historical_keyword_data` with the same country/language.
7. Call `kw_data_google_trends_explore` for at most 25 leading candidates in groups of five, using `type: web`, `item_types: ["google_trends_graph"]`, and a period covering at least the forecast horizon plus two prior years when available. Use `past_5_years` when explicit dates are unnecessary.

Validate statuses and non-empty result arrays before analysis. Record `total_count`, returned count, update timestamps, and unmatched or omitted keywords. Do not treat a capped result as complete domain coverage.

## Provider metrics versus derived values

Keep these returned values in clearly labeled **DataForSEO metric** columns without alteration: domain/page organic ETV, keyword ETV, current organic rank, search volume, monthly searches, keyword difficulty, organic keyword counts, and position buckets. DataForSEO ETV is already an estimated monthly traffic metric based on provider CTR and search-volume data.

Keep all modeled demand, target rank, assumed CTR, forecast traffic, incremental traffic, scenario totals, and priority scores in separate **Derived estimate** columns. Never describe them as DataForSEO forecasts. Do not reconcile or force equality among domain ETV, page ETV, and the sampled keyword ETV sum.

## Demand projection

For each keyword:

1. Use current Keyword Overview search volume as `base_volume`. If absent, no numeric traffic forecast is available.
2. Build a 12-month seasonal profile from the latest 12 complete non-null monthly observations. Divide each calendar month's value by their median, clamp each factor to `0.5-1.5`, then rescale the 12 factors to mean `1.0`. With fewer than six observations, use `1.0` and lower confidence.
3. Calculate the median available year-over-year change from the latest 24 complete monthly observations and clamp it to `-20%` through `+20%` per year. With insufficient matched months, use `0%` and lower confidence.
4. Calculate `forecast_volume[m] = base_volume * seasonal_factor[calendar_month] * (1 + annual_change)^(m/12)`.
5. Use Google Trends only to corroborate direction, breakpoints, and recurring seasonality. Its indices are relative within a request and must not be substituted for search volume or added across calls. Lower confidence when Trends and historical volume conflict.

Name every clamp and fallback in the report.

## CTR assumption

Use a user-supplied valid curve when present. Otherwise use the organic-position coefficients published in DataForSEO's [ETV calculation documentation](https://dataforseo.com/help-center/how-is-etv-calculated). Applying these coefficients to future demand and target ranks is still a derived planning assumption, not a returned DataForSEO metric or forecast:

| Rank | CTR |
| ---: | ---: |
| 1 | 30.40% |
| 2 | 16.20% |
| 3 | 9.73% |
| 4 | 6.59% |
| 5 | 4.69% |
| 6 | 3.38% |
| 7 | 2.56% |
| 8 | 1.97% |
| 9 | 1.50% |
| 10 | 1.13% |
| 11 | 0.91% |
| 12 | 0.75% |
| 13 | 0.59% |
| 14 | 0.56% |
| 15 | 0.51% |
| 16 | 0.43% |
| 17 | 0.43% |
| 18 | 0.33% |
| 19 | 0.27% |
| 20 | 0.24% |
| 21 | 0.23% |
| 22 | 0.22% |
| 23-100 | 0.21% |

Use `0.21%` for every rank from 23 through 100. Document the curve, its official source, capture date, whether the user overrode it, and whether it was calibrated. The published ETV method can also apply coefficients when paid results are present. This workflow does not inspect live ads; ratio calibration against current ETV retains the current effective adjustment, while the fallback curve does not model it.

When current ETV and search volume are positive, define `current_ctr = effective_current_ctr = min(1, keyword_etv / current_search_volume)`. Estimate target CTR by scaling this provider-implied current CTR with the documented curve ratio:

`calibrated_target_ctr = min(1, effective_current_ctr * assumed_ctr(target_rank) / assumed_ctr(current_rank))`

When current ETV is null or zero, set `current_ctr = assumed_ctr(current_rank)`, use the documented curve directly for every scenario, and assign low confidence. This fallback is a derived estimate, not provider ETV.

## Ranking scenarios and ramp

Use the current organic `rank_group`. Apply the following target matrix only when the scenario's difficulty gate passes. If a gate fails, target rank equals current rank and modeled gain is zero.

| Current rank | Conservative | Expected | Ambitious |
| --- | ---: | ---: | ---: |
| 1 | 1 | 1 | 1 |
| 2 | 2 | 1 | 1 |
| 3 | 3 | 2 | 1 |
| 4-10 | 3 | 2 | 1 |
| 11-20 | 10 | 5 | 3 |
| 21-50 | 20 | 10 | 5 |
| 51-100 | current | 20 | 10 |

- Conservative gate: KD `0-40`; two-month implementation lag; target reached at the final forecast month.
- Expected gate: KD `0-60`; one-month lag; target reached at 75% of the forecast period.
- Ambitious gate: KD `0-80`; no lag; target reached at 50% of the forecast period.

For missing KD, conservative gain is zero; expected and ambitious may be shown with low confidence and an explicit missing-difficulty warning. KD is a logarithmic 0-100 relative difficulty metric, so do not call a ten-point difference a linear ten-percent change in achievability.

After the scenario lag, linearly ramp CTR from current to target CTR by the target month. For every month calculate:

- `baseline_clicks[m] = forecast_volume[m] * current_ctr`
- `scenario_clicks[m] = forecast_volume[m] * ramped_scenario_ctr[m]`
- `incremental_clicks[m] = max(scenario_clicks[m] - baseline_clicks[m], 0)`

Sum monthly incremental clicks over the supplied period. Do not apply an undisclosed probability multiplier. Round only displayed values; calculate with unrounded values.

## Page aggregation and priority

Assign each keyword to the returned ranking URL. If duplicate keyword rows exist, retain the target-domain organic row with the highest ETV and record the discarded rows; do not double count. Sum unique keyword estimates by exact normalized page URL. Label page totals as sampled derived estimates.

Calculate the opportunity-versus-difficulty score only when expected incremental traffic, KD, current rank, and business tier are available:

- `gain_score`: percentile rank of `log1p(expected_incremental_traffic)` among candidates, scaled 0-100.
- `difficulty_score`: KD 0-20 = 100; 21-40 = 75; 41-60 = 50; 61-80 = 25; 81-100 = 5.
- `proximity_score`: rank 4-10 = 100; 11-20 = 75; 21-50 = 45; 51-100 = 20; otherwise 0.
- `business_score`: high = 100; medium or unspecified = 65; low = 35.
- `opportunity_score = 0.50 * gain_score + 0.25 * difficulty_score + 0.15 * proximity_score + 0.10 * business_score`.

Do not reweight missing components; mark the score unavailable. Business value affects ordering only, never forecast traffic.

## Confidence

Assign per-keyword confidence by evaluating Low conditions before Medium conditions:

- **High:** positive provider ETV and search volume, KD present, at least 12 complete monthly observations, Trends corroborates direction, and forecast period is at most 12 months.
- **Medium:** one high-confidence condition is absent or the period is 13-24 months.
- **Low:** generic CTR fallback, missing KD, fewer than six monthly observations, Trends conflict, unstable URL assignment, or period exceeds 24 months.

Assign each page the lowest confidence among keywords contributing the first 50% of its expected gain. State that confidence describes evidence quality, not probability of achieving the target rank.

## Cost and provenance

For every call log endpoint, purpose, requested/returned coverage, provider/task status, top-level response cost in USD, and timestamp. Sum unrounded costs and display `Total cost: x,xx USD` with a decimal comma and two digits. If any cost is absent, label the subtotal incomplete and name the affected calls.
