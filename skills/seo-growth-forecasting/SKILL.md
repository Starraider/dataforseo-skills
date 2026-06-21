---
name: seo-growth-forecasting
description: "Use when estimating achievable incremental organic traffic from SEO improvements, forecasting ranking scenarios, or prioritizing keywords and pages by growth potential versus difficulty with DataForSEO MCP."
---

# SEO Growth Forecasting

Use DataForSEO MCP [Domain Rank Overview](https://docs.dataforseo.com/v3/dataforseo_labs/google/domain_rank_overview/live/), [Relevant Pages](https://docs.dataforseo.com/v3/dataforseo_labs/google/relevant_pages/live/), [Ranked Keywords](https://docs.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live/), [Keyword Overview](https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_overview/live/), [Bulk Keyword Difficulty](https://docs.dataforseo.com/v3/dataforseo_labs/google/bulk_keyword_difficulty/live/), [Historical Keyword Data](https://docs.dataforseo.com/v3/dataforseo_labs/google/historical_keyword_data/live/), [Historical Rank Overview](https://docs.dataforseo.com/v3/dataforseo_labs/google/historical_rank_overview/live/), and [Google Trends](https://docs.dataforseo.com/v3/keywords_data/google_trends/explore/live/).

Read [references/forecast-contract.md](references/forecast-contract.md) before analysis and follow [templates/report-template.md](templates/report-template.md) when writing the report.

## Inputs

Require domain, country, language, and forecast period. Ask for every missing value together and wait before billable calls. Accept optional priority pages, per-page business-value tiers, a custom CTR curve, and report root. Normalize the domain to a lowercase hostname without `www.`, credentials, port, path, query, fragment, or trailing dot. Do not invent market or period defaults.

## Workflow

1. Establish current and historical domain visibility with Domain Rank Overview and Historical Rank Overview.
2. Retrieve up to 100 pages by organic ETV and 1,000 organic ranked keywords. Preserve provider totals separately from returned samples.
3. Select at most 500 candidate keywords using priority-page membership, business value, current ETV, search volume, and ranking proximity. Keep one documented URL assignment per keyword.
4. Enrich the candidates in batches with Keyword Overview, Bulk Keyword Difficulty, and Historical Keyword Data. Check up to 25 leading opportunities with Google Trends in batches of five.
5. Calculate conservative, expected, and ambitious scenarios exactly as defined in the contract. Keep DataForSEO metrics unchanged in provider columns. Label every scenario, uplift, aggregate, and priority score **Derived estimate — not a DataForSEO forecast**.
6. Rank keywords and pages by expected incremental traffic and the opportunity-versus-difficulty score. Never multiply traffic by business value; use value only for prioritization.

Validate HTTP, provider, task, and result statuses; preserve nulls; report sampling and missing data. Do not use Backlinks or LLM Mentions endpoints. Do not retry, paginate, expand caps, or make extra billable calls without approval.

## Report

Log every endpoint, purpose, status, returned cost, and timestamp. Sum unrounded costs and display `Total cost: x,xx USD`; identify absent costs.

Write detailed Markdown beginning with the local ISO date. Use the requested root or `SEO/`, create `<root>/<domain>/`, and save `<YYYY-MM-DD>_Growth-Forecasting_<domain>.md`, for example `2026-06-19_Growth-Forecasting_example.com.md`. Return the absolute path.
