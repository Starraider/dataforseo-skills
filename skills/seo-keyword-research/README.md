# SEO Keyword Research

`seo-keyword-research` finds and evaluates Google keyword opportunities for a website. It supports seed-based discovery and domain-based analysis, enriches the result with DataForSEO search metrics, groups search intent, calculates opportunity values and a 0–100 Keyword Score, and writes a detailed Markdown report.

## What the skill does

The skill has two modes:

- **Seed mode:** retrieves up to 200 related keywords and 100 keyword suggestions for a supplied seed.
- **Domain mode:** retrieves up to 100 organic keywords for which the supplied domain already ranks.

When both a seed and domain are supplied, seed mode is used unless domain mode is explicitly requested. A project domain is required in both modes because it determines the project and report location.

After discovery, the skill deduplicates keywords case-insensitively, preserves their sources, and retrieves bulk keyword difficulty for up to 1,000 unique terms. It reports available search volume, CPC, Google Ads competition, keyword difficulty, intent, ranking position, and URL.

It surfaces the top 20 opportunities and calculates a transparent 0–100 Keyword Score from volume, low-difficulty prevalence, intent diversity, CPC, and long-tail breadth. Missing components score zero and are disclosed rather than filled with invented values.

## Why this analysis matters

People may search for a product, service, or answer using very different words from those used inside a business. Keyword research reveals the language people actually type into Google, how often they search, what they are probably trying to accomplish, and how difficult it may be to compete for their attention. Without this information, a site can publish good material that answers the wrong question or uses wording its audience rarely searches for.

The analysis helps choose topics with a useful balance of demand, relevance, and competition. It can guide new pages, improve the wording and focus of existing pages, and match informational searches with helpful content or buying searches with suitable product and service pages. This clearer match between a page and a searcher's need can improve visibility and rankings over time, but the report identifies opportunities rather than promising results.

## Requirements and inputs

- The official DataForSEO MCP server with the DataForSEO Labs module enabled.
- Filesystem write access.
- A project domain or HTTP(S) URL.
- A seed keyword for seed mode, or an explicit request for domain mode.

Optional inputs are country, language, and report root. Defaults are United States, `en`, and `SEO/` below the current working directory. Retries, pagination, and extra API calls require approval.

## Invocation examples

Directly by skill name:

```text
Use the seo-keyword-research skill to research "electric bikes" for example.com.
```

For domain mode:

```text
Run seo-keyword-research in domain mode for example.com and find opportunities among its existing organic keywords.
```

With a market override:

```text
Research the seed "wärmepumpe kosten" for example.de using Germany and German search data.
```

With a custom report location and analysis emphasis:

```text
Find long-tail keywords related to "accounting software" for example.com, group them by intent, and save the report under ./client-reports.
```

If the project domain is missing—even when a seed is present—the skill asks for it before making billable requests.

## What to expect in the report

The report starts with the local ISO date and is saved by default as:

```text
SEO/<domain>/<YYYY-MM-DD>_Keyword-Analysis_<safe-target>.md
```

It contains:

- Scope, mode, country/language assumptions, timestamp, and total DataForSEO cost.
- An executive summary and Keyword Score with every component shown.
- The top 20 volume-to-difficulty opportunities.
- Navigational, Transactional, Commercial, and Informational intent groups.
- Related keywords and suggestions in seed mode, or ranked-keyword/long-tail proxy data in domain mode.
- Available volume, CPC, Ads competition, difficulty, rank, URL, and source metrics.
- Recommended content priorities and an explanation of all formulas.
- Endpoint call log, coverage, limitations, and official DataForSEO references.

The report distinguishes missing metrics from zero values and explains incomplete keyword-difficulty or sample coverage. The score is an opportunity signal, not a traffic forecast. After writing the report, the skill returns its absolute path and a concise summary.
