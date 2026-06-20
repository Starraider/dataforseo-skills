# SEO Competitor Gap Analysis

`seo-competitor-gap-analysis` identifies the domains that actually compete with a target in Google organic search, measures their shared and unique keyword footprints, compares estimated organic traffic, and turns the evidence into a prioritized competitor-gap report.

## What the skill does

The skill:

1. Normalizes the required project domain and applies the requested country and language, defaulting to United States and English.
2. Uses DataForSEO Labs to discover up to 20 organic competitors, excluding the target and common top domains.
3. Ranks competitors primarily by keyword intersections and then by estimated organic traffic value (ETV).
4. Examines the top five competitors in detail. For each, it requests shared keywords, target-only keywords, and competitor-only keywords, with samples limited to 1,000 rows per comparison.
5. Calculates keyword overlap, average organic position gaps, defensive wins, traffic/visibility gaps, and strategic competitor groups.
6. Calculates a reproducible 0–100 Competitive Score.
7. Writes a dated Markdown report with prioritized actions and a complete DataForSEO call-cost log.

Competitors are classified as Direct at 30% or more target-keyword overlap, Adjacent at 10–29.99%, and Aspirational below 10% when their median domain rank is at least 1.5 times the target's. Remaining domains are Low-overlap. The report explains these thresholds.

## Why this analysis matters

The businesses you think of as competitors are not always the websites competing for the same Google searches. This analysis shows which sites repeatedly appear for the terms your audience uses, what they are visible for, and where your own site is missing or falling behind. That makes it easier to learn from the actual search landscape instead of relying on assumptions.

The findings can reveal topics worth covering, existing pages that need improvement, and keywords where a competitor can realistically be overtaken. They also help prevent wasted effort on rivals or search terms that have little relevance to the business. Acting on these gaps can increase the number of useful searches for which the site appears and improve existing positions over time, although no individual change can guarantee a ranking increase.

## Requirements and inputs

- The official DataForSEO MCP server with the DataForSEO Labs module enabled.
- Filesystem write access.
- A project domain or HTTP(S) URL. The skill normalizes it to a hostname.

Optional inputs are country, language, and report root. Defaults are United States, `en`, and `SEO/` below the current working directory. Retries, pagination beyond 1,000 keywords, and additional API calls require approval.

## Invocation examples

Directly by skill name:

```text
Use the seo-competitor-gap-analysis skill for example.com.
```

With a market override:

```text
Identify the true organic competitors of example.co.uk in the United Kingdom using English search data.
```

With a strategic question:

```text
Analyze example.com against its organic-search competitors, show where it loses keywords and traffic, and prioritize the gaps to close.
```

With a custom report location:

```text
Run seo-competitor-gap-analysis for https://www.example.com and save the report under ./reports/q3.
```

If the domain is absent or malformed, the skill asks for a valid domain before making billable requests.

## What to expect in the report

The report starts with the local ISO date and is saved by default as:

```text
SEO/<domain>/<YYYY-MM-DD>_Competitor-Report_<domain>.md
```

It contains:

- Scope, market assumptions, timestamp, and total DataForSEO cost.
- An executive summary and Competitive Score with its exact inputs and interpretation.
- A discovery table of up to 20 competitors and a detailed top-five comparison.
- Shared, target-only, and competitor-only keyword counts and examples for each top-five competitor.
- Average ranking gaps, sample coverage, and the target's strongest defensive wins.
- Direct, Adjacent, Aspirational, and Low-overlap strategic groups.
- Estimated organic traffic and visibility gaps.
- Prioritized SEO actions, methodology, call log, limitations, and official references.

Counts can exceed the displayed keyword samples because DataForSEO returns totals separately from limited result rows. The report labels sampled data and its coverage rather than implying that a partial result is complete. Missing provider metrics or costs are also called out. After writing the report, the skill returns its absolute path and a concise summary.
