# SEO Cannibalization and Internal Linking

`seo-cannibalization-internal-linking` detects priority pages competing for the same Google organic keywords, selects the best primary target, recommends consolidation or differentiation, and creates a sampled internal-link map.

## What the skill does

The skill uses DataForSEO MCP to discover important pages and ranked keywords, compare up to 20 priority URLs through Page Intersection, and verify the highest-priority overlaps with Instant Pages and Content Parsing. It distinguishes harmful same-intent competition from useful multi-URL visibility.

For each overlapping keyword cluster, it selects a primary page and assigns an evidence-based merge, redirect, canonicalize, differentiate, or retain decision. The internal-link plan supplies source pages, target pages, natural anchor text, placement context, and whether a parsed source already links to the target.

## Requirements and inputs

- Domain, country, and language are required.
- Specific priority URLs are optional because the skill can discover candidates from the domain.
- The official DataForSEO MCP server must expose DataForSEO Labs and OnPage modules.
- Filesystem write access is required.

The skill asks for all missing required inputs before making billable calls. Optional inputs are priority URLs and a report root.

## Invocation examples

```text
Find keyword cannibalization on example.com for United States/en and recommend internal links.
```

```text
Compare https://example.de/leistungen/seo/ and https://example.de/seo-agentur/ for Germany/de, select the primary page, and save the report under ./client-reports.
```

```text
Map pages competing for the same keywords on example.co.uk for United Kingdom/en and tell me what to merge, redirect, canonicalize, differentiate, or retain.
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

It includes candidate coverage, multi-URL keywords, primary and competing page selection, exact consolidation or differentiation actions, page briefs, a sampled internal-link map, costs, methodology, and limitations.

Without the task-based OnPage crawler, the skill analyzes discovered or supplied priority pages. It does not claim to provide a complete site-wide internal-link graph.
