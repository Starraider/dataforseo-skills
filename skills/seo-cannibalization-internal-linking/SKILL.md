---
name: seo-cannibalization-internal-linking
description: "Use when detecting pages competing for the same keywords, selecting canonical target pages, deciding whether to merge, redirect, canonicalize, differentiate, or retain overlapping content, or recommending evidence-based internal links with DataForSEO MCP."
compatibility: "Requires the official DataForSEO MCP server with DATAFORSEO_LABS and ONPAGE enabled, plus filesystem write access."
---

# SEO Cannibalization and Internal Linking

Use [Relevant Pages](https://docs.dataforseo.com/v3/dataforseo_labs-google-relevant_pages-live/), [Ranked Keywords](https://docs.dataforseo.com/v3/dataforseo_labs-google-ranked_keywords-live/), [Page Intersection](https://docs.dataforseo.com/v3/dataforseo_labs-google-page_intersection-live/), [Content Parsing](https://docs.dataforseo.com/v3/on_page-content_parsing-live/), and [Instant Pages](https://docs.dataforseo.com/v3/on_page-instant_pages/).

## Inputs and scope

Require domain, country, and language; ask for every missing value and wait. Accept optional priority URLs and report root. Normalize the domain to a lowercase hostname without credentials, port, trailing dot, or leading `www.`. Require supplied pages to be absolute HTTP(S) URLs on that hostname or its subdomains. Use Google organic, the supplied market, and `ignore_synonyms: true` where supported. Inspect active MCP schemas before calls; they override examples.

## Workflow

1. Call `dataforseo_labs_google_relevant_pages` for 50 pages ordered by organic ETV and `dataforseo_labs_google_ranked_keywords` for 1,000 keywords ordered by ETV. Preserve exact URLs, positions, ETV, volume, difficulty, intent, and nulls.
2. Build a maximum 20-page sample from supplied URLs first, then high-ETV relevant pages with distinct paths and keyword coverage. State exclusions and caps.
3. Call `dataforseo_labs_google_page_intersection` once with those pages, `intersection_mode: union`, organic items, and `limit: 1000`. Treat a keyword as multi-URL only when at least two populated per-page organic results exist. Group close variants only when intent matches.
4. Prioritize up to three overlapping clusters by search demand, ranking proximity, ETV, URL switching evidence if present, and intent overlap. Multiple ranking URLs alone do not prove harmful cannibalization.
5. For no more than ten distinct competing, primary, and potential source pages, call both `on_page_instant_pages` and `on_page_content_parsing`. Verify status, indexability/canonical signals when returned, titles, headings, topic and intent, content overlap, existing links, and anchors.
6. Select the primary page by intent fit first, then current position/ETV, topical completeness, internal-link support, technical eligibility, and stated business priority. Explain ties and uncertainty.
7. Assign **merge**, **redirect**, **canonicalize**, **differentiate**, or **retain**. Reserve canonicalization for duplicate pages that must remain reachable; prefer a redirect after merging when the weaker URL can be retired. Never recommend redirecting a page with distinct valuable intent without evidence.
8. Create a sampled link map from parsed pages. Include source, target, natural anchor, placement context, existing-link status, and rationale. Avoid repetitive exact-match anchors and do not claim unparsed links are absent.

Validate response statuses, costs, coverage, and URL joins. Do not invent metrics. Ask before retries, pagination, or larger caps. Log each endpoint and cost; sum unrounded costs and show `Total cost: x,xx USD`, naming calls with missing cost.

## Report

Follow [templates/report-template.md](templates/report-template.md). Use the requested root or `SEO/`; create `<root>/<domain>/`. Save `<YYYY-MM-DD>_Content-Decay-Refresh_<domain>.md`, for example `2026-06-19_Content-Decay-Refresh_example.com.md`, and return the absolute path.

State prominently that without the task-based OnPage crawler this covers discovered or supplied priority pages and does not guarantee a complete site-wide internal-link graph.
