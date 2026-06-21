# SEO Growth Forecasting

`seo-growth-forecasting` estimates achievable incremental organic traffic for ranked keywords and pages, compares three ranking scenarios, and prioritizes SEO work by opportunity versus difficulty.

## What the skill does

The skill uses DataForSEO MCP to establish current domain and page visibility, select ranked-keyword opportunities, add current and historical demand plus keyword difficulty, and check leading opportunities with Google Trends. It produces conservative, expected, and ambitious ranking scenarios over a required forecast period.

DataForSEO organic ETV, ranks, volumes, difficulty, and counts remain unchanged in provider-metric columns. Forecast demand, assumed CTR, target ranks, incremental traffic, page totals, and opportunity scores are separately labeled `Derived estimate — not a DataForSEO forecast`. The default position curve uses DataForSEO's published organic ETV coefficients, and the report includes the complete curve, source, calibration, clamps, fallbacks, ramp timing, confidence rules, and equations.

## Why this analysis matters

SEO teams are often asked how much growth is realistically possible before time and budget are committed. A forecast cannot predict Google with certainty, but it can show the difference between a small improvement, a reasonable target, and a more ambitious upside case. That helps decision-makers judge whether a project is worth doing, which pages deserve priority, and what level of result would still count as success.

The report lays out the current baseline first and then compares three future scenarios over the selected time period. It shows which keywords and pages create the biggest upside, how much incremental traffic each scenario could add, what assumptions were used to estimate that outcome, and how confident the evidence is. For non-specialists, that makes the document useful as a planning tool: it connects SEO work to a range of possible traffic outcomes instead of treating optimization as an open-ended activity with no measurable target.

## Required inputs

- Domain or HTTP(S) URL.
- Country as a full DataForSEO location name.
- Language as a DataForSEO language code.
- Forecast period as a positive number of months or explicit future start/end months.

Priority pages, page-level `high`/`medium`/`low` business tiers, a custom CTR curve, and report root are optional. Missing required inputs are requested together before any billable call.

## Outputs

- Current organic visibility baseline.
- Conservative, expected, and ambitious ranking scenarios.
- Estimated incremental traffic by unique keyword and exact page URL.
- Opportunity-versus-difficulty prioritization.
- Pages with the largest potential gain.
- Explicit assumptions and evidence-quality confidence levels.
- DataForSEO call log and summed cost.

Business value affects priority only; it never inflates traffic estimates. Google Trends corroborates direction and seasonality but is never treated as absolute search volume. Backlinks and LLM Mentions endpoints are outside scope.

## Requirements

- Official DataForSEO MCP server with DataForSEO Labs and Keywords Data enabled.
- Securely configured DataForSEO credentials.
- Filesystem write access.

## Invocation examples

```text
Forecast 12 months of SEO growth for example.com in United States/en. Use high business value for /pricing and /solutions, then prioritize the pages with the largest achievable gain.
```

```text
Create conservative, expected, and ambitious organic traffic scenarios for example.org in Germany/de from July 2026 through June 2027.
```

```text
Use seo-growth-forecasting for example.co.uk, United Kingdom/en, forecast period 18 months, and save the report under ./client-reports.
```

## Report

The default report path is:

```text
SEO/<domain>/<YYYY-MM-DD>_Growth-Forecasting_<domain>.md
```

For example:

```text
SEO/example.com/2026-06-19_Growth-Forecasting_example.com.md
```

The file begins with the matching local ISO date and contains the baseline, scenario comparison, page and keyword forecasts, opportunity score, demand and Trends evidence, CTR assumptions, action plan, methodology, confidence, call log, costs, limitations, and official sources.
