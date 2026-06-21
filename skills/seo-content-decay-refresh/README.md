# SEO Content Decay Refresh

`seo-content-decay-refresh` detects ranking and estimated-traffic declines among a domain's important existing pages, separates likely seasonality from structural losses, and produces evidence-backed refresh briefs.

## What the skill does

The skill uses DataForSEO MCP to:

1. Measure recent domain-level organic visibility trends.
2. identify important pages and their currently ranked keywords.
3. inspect up to ten shortlisted keywords across 24 months of historical SERPs.
4. compare ranking changes with historical search demand and five years of Google Trends data.
5. estimate sampled traffic impact from DataForSEO ETV changes.
6. classify each decline as Structural, Seasonal, Mixed, or Inconclusive/stable.
7. parse up to five priority pages and recommend refresh, consolidation, redirect, or no change.
8. provide an updated heading outline and specific internal-link opportunities for every actionable page.

This skill protects and restores traffic from existing content. Use `seo-content-suggestions` when the primary goal is finding new articles to publish.

## Why this analysis matters

Older pages often lose search visibility gradually, and the reason is not always obvious. A page may have slipped because competitors improved, because the content no longer matches what people expect, or because interest in the topic naturally rises and falls during the year. This analysis helps separate those situations so a team does not waste time rewriting content that is only experiencing normal seasonality or ignore pages that are genuinely losing ground.

The report explains which pages and keywords are declining, how large the likely traffic impact is, and whether the evidence points to a structural problem, a seasonal pattern, or a mixed picture. It also contains a page-by-page action plan, including refresh recommendations, consolidation or redirect suggestions where appropriate, updated outlines, and internal-link ideas. For non-SEO readers, it turns a vague sense that "traffic is down" into a list of specific pages to fix and why they should be fixed.

## Requirements and inputs

- The official DataForSEO MCP server with DataForSEO Labs, Keywords Data, and OnPage modules enabled.
- Filesystem write access.
- A domain or HTTP(S) URL.

Country, language, comparison scope, and report location are optional. Defaults are United States, `en`, the workflow's bounded sampling caps, and `SEO/` below the current working directory. The skill asks for a missing domain before making billable calls.

## Invocation examples

```text
Use seo-content-decay-refresh to find declining pages on example.com and prepare refresh briefs.
```

```text
Separate seasonal demand changes from ranking decay for example.co.uk in the United Kingdom.
```

```text
Prioritize content refreshes for example.org and save the report under ./client-reports.
```

## Report

The detailed Markdown report is saved by default as:

```text
SEO/<domain>/<YYYY-MM-DD>_Content-Decay-Refresh_<domain>.md
```

For example:

```text
SEO/example.com/2026-06-19_Content-Decay-Refresh_example.com.md
```

It includes domain trends; declining pages and keywords; ranking-loss and sampled estimated-traffic impact; seasonal-versus-structural evidence; refresh, consolidate, redirect, or unchanged recommendations; updated outlines; internal-link suggestions; DataForSEO costs; coverage; methodology; and limitations.

Historical SERPs are sampled from keywords that still appear in the current ranked-keyword set. The report therefore does not claim to recover pages or keywords that disappeared entirely before the current snapshot.
