# SEO Page Metadata

`seo-page-metadata` analyzes one page through DataForSEO MCP, identifies five evidence-based seed keywords, retrieves up to 25 related keywords for each seed, and turns the best low-difficulty opportunities into implementation-ready metadata suggestions.

## What the skill does

The skill requires an absolute HTTP(S) page URL. It uses DataForSEO OnPage Instant Pages to audit the page's existing title, description, canonical URL, meta keywords, and social tags. Existing metadata is never used to infer the page topic because it may be missing or inaccurate. OnPage Content Parsing separates the primary page text and headings from repeated navigation and footer content; that primary content is the sole evidence for topic, intent, geographic scope, seed keywords, and truthful suggestions.

From the parsed primary content, it derives exactly five distinct seed keywords that represent the page's main topic and search intent. When the content explicitly targets a country, region, or city, the skill incorporates that scope naturally into applicable seeds. It ignores locations found only in boilerplate or a footer address. It then makes one Related Keywords request per seed with search depth 2 and a limit of 25 results. Results are deduplicated case-insensitively while retaining all seed sources.

The skill defines organic competition through DataForSEO Keyword Difficulty. For each relevant keyword with complete metrics, it calculates:

```text
opportunity = search_volume / (keyword_difficulty + 10)
```

It selects the 20 highest-scoring keywords, using search volume and lower difficulty as tie-breakers. Google Ads competition is reported separately because it measures paid-search advertiser competition, not organic ranking difficulty.

## Requirements and inputs

- The official DataForSEO MCP server with OnPage and DataForSEO Labs enabled.
- Filesystem write access.
- One absolute HTTP(S) page URL.

Optional inputs are country, language, and report root. The report root defaults to `SEO/` below the current working directory. A user-specified country and language take precedence. Otherwise, the skill starts with United States and `en`, but uses a country explicitly and unambiguously targeted by the primary page content for keyword calls. The page hostname supplies only the project domain, not topic or location evidence. The skill asks for a missing URL before making billable requests. Retries, pagination, and extra DataForSEO calls require approval.

## Invocation examples

```text
Analyze https://example.com/products/widget and suggest improved page and social metadata.
```

```text
Find low-hanging-fruit keywords for https://example.org/services/consulting and write three metadata options for every field.
```

```text
Run seo-page-metadata for https://example.de/leistungen/seo using Germany and German, and save the report under ./client-reports.
```

If the page URL is missing, the skill asks for it and waits without making DataForSEO calls.

## What to expect in the report

The report begins with the local ISO date and is saved by default as:

```text
SEO/<domain>/<YYYY-MM-DD>_Page-Metadata_<safe-URL>.md
```

For example:

```text
SEO/example.com/2026-06-19_Page-Metadata_https_example.com_products_widget.md
```

It contains:

- Scope, selected market and its source, timestamp, and total DataForSEO cost.
- Existing title, description, canonical, meta keywords, Open Graph, and Twitter Card data.
- Primary-content evidence, detected geographic scope, and rationales for the five seed keywords.
- Requested, returned, unique, complete-metric, and excluded keyword counts.
- A top-20 keyword table with search volume, organic difficulty, Ads competition, opportunity score, and seed provenance.
- Three Page Title, Meta Description, Meta Keywords, Open Graph Title, Open Graph Description, Twitter Card Title, and Twitter Card Description options.
- Character counts, implementation notes, limitations, formula, call log, and official documentation links.

The report states that existing metadata was audited but excluded from topic, intent, location, and seed derivation. The 21 suggestions stay faithful to the parsed primary content and its search intent. The meta-keywords options are included because the workflow requests them, while the report notes that Google does not use the meta keywords tag for ranking.
