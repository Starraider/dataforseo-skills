---
name: seo-content-decay-refresh
description: "Use when detecting declining organic content, separating ranking decay from seasonality, prioritizing existing pages for refresh, or producing evidence-based content refresh briefs with DataForSEO MCP."
---

# SEO Content Decay Refresh

Use [Historical Rank Overview](https://docs.dataforseo.com/v3/dataforseo_labs/google/historical_rank_overview/live/), [Relevant Pages](https://docs.dataforseo.com/v3/dataforseo_labs/google/relevant_pages/live/), [Ranked Keywords](https://docs.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live/), [Historical SERPs](https://docs.dataforseo.com/v3/dataforseo_labs/google/historical_serps/live/), [Historical Keyword Data](https://docs.dataforseo.com/v3/dataforseo_labs/google/historical_keyword_data/live/), [Google Trends](https://docs.dataforseo.com/v3/keywords_data/google_trends/explore/live/), and [Content Parsing](https://docs.dataforseo.com/v3/on_page/content_parsing/live/).

## Scope

Require a domain; if absent, ask and wait. Normalize it to a lowercase hostname without credentials, port, trailing dot, or leading `www.`. Default to `United States`/`en`; disclose assumptions. Use Google organic and `ignore_synonyms: true`. Ask before retries, pagination, or exceeding the caps below.

## Workflow

1. Call `dataforseo_labs_google_historical_rank_overview` to establish domain-level organic ETV, keyword-count, and position-bucket trends.
2. Call `dataforseo_labs_google_relevant_pages` for 50 pages ordered by organic ETV, then `dataforseo_labs_google_ranked_keywords` for 1,000 organic keywords ordered by ETV. Join exact normalized URLs; preserve unmatched rows.
3. Select up to ten high-ETV keywords across important pages, maximum two per page. Call `dataforseo_labs_google_historical_serps` per keyword for the latest 24 months. Extract the target's monthly organic URL, `rank_group`, and ETV; record URL switching.
4. Batch those keywords through `dataforseo_labs_google_historical_keyword_data`. Call `kw_data_google_trends_explore` in batches of five with `type: web`, `item_types: ["google_trends_graph"]`, and `time_range: past_5_years`.
5. Compare the latest three complete months with the same months one year earlier. Calculate `position_loss = recent_median_position - baseline_median_position`, `demand_change = 100 * (recent_median_volume / baseline_median_volume - 1)`, and `traffic_impact = max(baseline_median_ETV - recent_median_ETV, 0)`. Sum sampled keyword impact per page; never substitute an external CTR model.
6. Classify **Structural** when position loss is at least 3 and demand change is above -10%; **Seasonal** when demand falls at least 15%, positions stay within 2, and Trends shows a comparable recurring dip in two prior years; **Mixed** when position loss is at least 3 and demand falls at least 15%; otherwise **Inconclusive/stable**. Label missing or zero baselines.
7. Prioritize by traffic impact, current ETV, business intent, and confidence. Call `on_page_content_parsing` for up to five pages. Recommend **refresh** for stale/incomplete structural losses; **consolidate** for overlapping URLs or intent cannibalization; **redirect** only for obsolete pages with a relevant replacement; otherwise **leave unchanged**.

## Brief and report

For each priority, provide declining keywords, position and ETV deltas, classification evidence, recommendation, specific additions/removals, an updated H1/H2/H3 outline, and source URL → target URL internal-link suggestions with anchor and rationale. Mark unverified links. Explain that this protects existing traffic while `seo-content-suggestions` proposes new articles.

Validate statuses and sampling; do not invent values. Log endpoint, response cost, and coverage. Sum unrounded costs and show `Total cost: x,xx USD`; identify missing cost values.

Write a detailed Markdown report beginning with the local ISO date. Use the requested root or `SEO/`; create `<root>/<domain>/`. Save `<YYYY-MM-DD>_Content-Decay-Refresh_<domain>.md`, for example `2026-06-19_Content-Decay-Refresh_example.com.md`. Include Scope, summary, domain trend, page/keyword table, impact calculations, classifications, briefs, internal links, methodology, call log, and limitations. Return the absolute path.
