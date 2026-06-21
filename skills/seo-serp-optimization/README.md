# SEO SERP Optimization

`seo-serp-optimization` finds Google SERP features available for keywords where a domain already ranks in positions 1-20, verifies the current result composition with live DataForSEO SERPs, compares target pages with representative feature owners, and produces implementation-ready page-format changes.

## What the skill does

The skill starts with one bounded Ranked Keywords call and uses each keyword's `serp_item_types` inventory to propose up to ten candidates. It waits for approval before making one live SERP call per shortlisted keyword and parsing the distinct target and representative winning pages. This keeps billable fan-out explicit.

The analysis covers featured snippets, answer boxes, People Also Ask, video, images, local packs, shopping, product features, recipes, discussions, news, and other result types exposed by DataForSEO. It records current owners, nested owners, feature prominence, target organic position, and inferred winning page format. Features missing from the successful live SERP are labeled stale rather than treated as opportunities.

## Why this analysis matters

Ranking on the first page is useful, but the search results page often contains much more than standard blue links. Features such as featured snippets, People Also Ask boxes, video panels, image results, or local packs can take a large share of attention before a user ever reaches the normal listings. This analysis helps identify which of those features are realistically available for a site's existing keywords and what changes might improve the page's chance of appearing in them.

The report shows where the domain already ranks, which SERP features are present now, who currently owns those features, and how attainable each opportunity looks. It then translates that into exact page-format recommendations, such as adding clearer answer blocks, improving lists or tables, strengthening supporting questions, or enhancing media and structured data. For non-SEO readers, the document is useful because it turns a complex search-results layout into a practical page-improvement checklist tied to visible opportunities in Google.

## Recommendations and priority

Recommendations focus on actual page composition: answer blocks, headings, ordered or unordered lists, table columns, original imagery, video placement and transcripts, structured-data eligibility, supporting questions, and external dependencies. They identify an exact target URL and insertion point. Structured data is never presented as a display guarantee.

Each current opportunity receives an Owned, High, Medium, Low, External dependency, or Stale/absent classification. A reproducible 0-100 priority score combines target ranking proximity, log-normalized search volume, intent fit, and the feature's absolute live prominence. Missing inputs remain missing rather than being converted to zero.

## Requirements and inputs

- A target domain or HTTP(S) URL; the skill asks when it is absent.
- Official DataForSEO MCP with DataForSEO Labs, SERP, and OnPage enabled.
- Filesystem write access.

Country, language, device, exact Google location, and report root are optional. Defaults are United States, `en`, desktop, and `SEO/` below the current working directory. An exact location is recommended for local-pack work.

## Invocation examples

```text
Analyze example.com for featured-snippet, PAA, image, and video opportunities.
```

```text
Find SERP-feature opportunities for example.de in Germany, de, on mobile and let me approve the live shortlist.
```

```text
Analyze example.org for local-pack and shopping opportunities and save the report under ./client-reports.
```

## Report

The detailed Markdown report contains the opportunity matrix, live owners and target positions, attainability, exact page-structure changes, scoring components, parsed-page comparisons, cost log, and limitations. The default path is:

```text
SEO/<domain>/<YYYY-MM-DD>_Serp-Optimization_<domain>.md
```

For example: `SEO/example.com/2026-06-19_Serp-Optimization_example.com.md`.
