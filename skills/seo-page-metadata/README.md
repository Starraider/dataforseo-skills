# SEO Page Metadata

`seo-page-metadata` analyzes one page through DataForSEO MCP, derives five evidence-backed seed keywords from structured primary content, ranks related keyword opportunities, and produces three coherent search and social metadata packages.

## What the skill does

The skill validates one absolute HTTP(S) URL and announces a normal seven-call budget: OnPage Instant Pages, OnPage Content Parsing, and one bounded Related Keywords request for each of five seeds. It uses the active MCP schemas and asks before retries, pagination, extra calls, or more expensive JavaScript rendering.

Instant Pages supplies the current title, description, canonical, meta keywords, and social tags for audit purposes. Those fields and the page URL are not positive topic evidence. Topic, intent, service geography, seeds, and suggested claims come only from qualifying headings and primary text in Content Parsing `main_topic` data. Header, footer, secondary content, navigation, cookie, legal, contact-only, and other boilerplate content are excluded.

A successful keyword run requires five distinct, non-brand seeds supported by that evidence. If the page is broken, primary content is empty, or five seeds cannot be justified, the skill stops before Related Keywords calls. It returns the evidence shortfall and asks before a JavaScript-rendered retry instead of padding the seed list.

## Keyword workflow

Each Related Keywords request uses one approved seed, one selected country/language pair, depth 2, limit 25, and descending search volume. Country and language are resolved independently. User overrides win; otherwise explicit primary-content service geography and content language are used before disclosed United States/`en` defaults. Unsupported or uncertain pairs are resolved through an exposed MCP utility or confirmed with the user.

Results are normalized with Unicode NFKC, collapsed whitespace, and casefolded deduplication. Seed provenance is merged. Zero remains distinct from missing data, metric conflicts are recorded, and every exclusion receives a reason. Complete relevant rows receive the derived score:

```text
opportunity_proxy = search_volume / (keyword_difficulty + 10)
```

The proxy prioritizes the candidate set; it is not a DataForSEO metric or proof of low competition. Organic Keyword Difficulty remains separate from paid Ads competition.

## Requirements and inputs

- Python 3 and filesystem write access.
- Official DataForSEO MCP with OnPage and DataForSEO Labs enabled.
- One absolute HTTP(S) page URL without embedded credentials.

Optional inputs are country, language, report root, and a request for legacy meta keywords. The default report root is `SEO/` below the current working directory.

## Invocation examples

```text
Analyze https://example.com/products/widget and recommend improved search and social metadata.
```

```text
Research keyword opportunities for https://example.org/services/consulting and create three coherent metadata packages.
```

```text
Run seo-page-metadata for https://example.de/leistungen/seo using Germany and de, and save it under ./client-reports.
```

If the page URL is missing, the skill asks for it and makes no billable request.

## Report contents

The report includes scope and timestamp, current metadata, primary-content evidence, market/language provenance, five justified seeds, coverage and exclusion counts, up to 20 ranked keyword opportunities, three coherent metadata packages with Unicode code-point counts, one recommended package, limitations, method, call log, and cost total.

Length ranges are editorial targets rather than display guarantees. Meta keywords are omitted unless explicitly requested; when included, they are labeled legacy-only because Google and Bing do not use them for rankings.

The default path is:

```text
SEO/<domain>/<YYYY-MM-DD>_Page-Metadata_<safe-URL>.md
```

Query and fragment text is excluded from filenames and redacted in the report scope. Every filename ends with a short deterministic hash to prevent collisions without exposing query values. The filename is capped at 140 characters.
