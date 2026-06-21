---
name: seo-page-metadata
description: "Use when analyzing one webpage's primary topic, finding DataForSEO-backed keyword opportunities, or producing evidence-based search, Open Graph, and Twitter metadata in a Markdown report."
compatibility: "Requires Python 3, filesystem write access, and the official DataForSEO MCP server with ONPAGE and DATAFORSEO_LABS enabled."
---

# SEO Page Metadata

Analyze one supplied page without treating its existing metadata or URL as proof of its topic. Use DataForSEO MCP for every SEO data call.

## Required procedure

1. Read [references/data-contract.md](references/data-contract.md) before making calls. It defines URL safety, exact response paths, evidence boundaries, market selection, validation, normalization, scoring, cost accounting, and failure behavior.
2. Require one absolute HTTP(S) URL. Run `python3 <this-skill-directory>/scripts/metadata_support.py filename --url <url> --date <local-date>` to validate it and obtain the normalized domain and filename. Ask and wait when the URL is absent or invalid.
3. Inspect the active MCP schemas for `on_page_instant_pages`, `on_page_content_parsing`, and `dataforseo_labs_google_related_keywords`; active schemas override captured examples. Announce the normal seven-call budget: two OnPage calls and five Related Keywords calls, each with `depth: 2` and `limit: 25`.
4. Call both OnPage tools for the validated request URL. Use only exposed arguments. Do not enable JavaScript initially. Audit current metadata from Instant Pages, then run `extract-content` to classify the evidence mode as either `structured_main_topic` or `projection_degraded_text`. Derive topic, intent, geography, seeds, and suggestions only from qualifying Content Parsing evidence.
5. Continue automatically only when the content contract supports five distinct non-brand seeds. If the evidence mode is `projection_degraded_text`, disclose the lower confidence before keyword calls and stop instead when the fallback text is too noisy or thin to justify all five seeds. Ask before a JavaScript retry or other billable recovery.
6. Select country and language independently using the documented precedence. Disclose conflicts and ask rather than guessing an unsupported pair.
7. Make one Related Keywords call per seed with the same market and explicit descending search-volume order. Do not request parameters absent from the active schema. Remove an exact seed row locally if returned.
8. Normalize and rank results with `scripts/metadata_support.py`; preserve null versus zero, merged seed provenance, metric conflicts, exclusions, coverage, and the derived `opportunity_proxy` formula.
9. Read [templates/report-template.md](templates/report-template.md), produce three coherent metadata packages, and mark one recommended. Treat length ranges as editorial targets. Include legacy meta keywords.
10. Save the report under the requested root or `<cwd>/SEO`, return its absolute path, and summarize the recommendation, keyword coverage, limitations, and total cost.

Ask before every retry, pagination request, extra call, or more expensive JavaScript rendering. Never bypass MCP, invent missing metrics, or persist raw customer responses in the repository.
