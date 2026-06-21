# SEO International Opportunities

`seo-international-opportunities` compares organic search opportunities across countries and languages, keeps each market's evidence isolated, and produces a launch-ready international SEO plan.

## What the skill does

For every supplied country/language pair, the skill uses DataForSEO MCP to measure relevant and ranked keywords, existing domain visibility, organic competitors, competitor-only gaps, keyword metrics, search intent, and five-year trend direction. It then validates up to three approved native terms per market with live Google SERPs.

The analysis produces:

- a market-by-market demand and visibility comparison;
- existing visibility and competitor-strength evidence;
- localized keyword and content clusters;
- a reproducible 0-100 opportunity score and recommended launch order when all components are available;
- country/language URL, subdirectory, subdomain, or ccTLD recommendations;
- terms that require native localization rather than literal translation;
- a phased page and content launch plan.

Raw keyword volumes, rankings, intent, competitors, terminology, and Trends data remain inside their country/language market. Only independently calculated, identically capped summaries are compared.

## Required inputs

- A domain or HTTP(S) URL.
- The site's current language.
- At least two unique target country/language combinations, for example `Germany/de` and `Austria/de`.

Device, report root, supplied competitors, strategic constraints, and a pre-approved live validation count are optional. The skill asks for all missing required inputs before making a billable request.

## Requirements

- The official DataForSEO MCP server with DataForSEO Labs, Keywords Data, and SERP modules enabled.
- DataForSEO credentials configured securely in the MCP server.
- Filesystem write access.

## Invocation examples

```text
Compare international SEO opportunities for example.com. The current language is English. Evaluate Germany/de, Austria/de, and France/fr, then recommend a launch order.
```

```text
Plan localized expansion for example.co.uk from en into United States/en and Canada/en. Keep the country datasets separate and validate the top three terms per market with live SERPs.
```

```text
Use seo-international-opportunities for example.org, current language de, target markets Switzerland/de, Switzerland/fr, and France/fr. Save the report under ./client-reports.
```

## Report

The default report path is:

```text
SEO/<domain>/<YYYY-MM-DD>_International-Opportunities_<domain>.md
```

For example:

```text
SEO/example.com/2026-06-19_International-Opportunities_example.com.md
```

The file begins with the local ISO date and includes the launch order, market summaries, per-market clusters, localization risks, trend and live SERP evidence, URL architecture, page recommendations, phased actions, methodology, coverage, call log, costs, limitations, and official sources.
