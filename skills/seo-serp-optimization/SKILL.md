---
name: seo-serp-optimization
description: "Use when identifying featured-snippet, People Also Ask, video, image, local-pack, shopping, or other Google SERP-feature opportunities and adapting ranked pages to compete for the live result composition."
compatibility: "Requires the official DataForSEO MCP server with DATAFORSEO_LABS, SERP, and ONPAGE enabled, plus filesystem write access."
---

# SEO SERP Optimization

Optimize page format for Google features shown in current results. This is not metadata rewriting or general prose optimization. Use DataForSEO MCP for all SEO evidence.

## Required workflow

1. Read [references/data-contract.md](references/data-contract.md). Require a domain; ask and wait when absent. Normalize it safely. Accept country, language, device, exact location, and report root. Default to United States, `en`, desktop, and `SEO/`; disclose defaults. Exact location overrides country for live SERPs.
2. Inspect the active schemas for `dataforseo_labs_google_ranked_keywords`, `serp_organic_live_advanced`, and `on_page_content_parsing`; they override examples. Announce the initial one-call discovery budget.
3. Call Ranked Keywords for organic target results in positions 1-20, ordered by search volume, limit 200. Retain keyword, target URL and positions, volume, intent, keyword difficulty, timestamps, and `serp_info.serp_item_types`. Preserve nulls.
4. Build up to ten candidate keywords whose feature inventory contains an actionable result type. Present the candidate shortlist, preliminary rationale, and the next call budget. Ask the user to approve keywords before live SERP fan-out unless the prompt already approves a bounded shortlist.
5. For each approved keyword, call Advanced Live SERP with Google, the selected market/language/device, depth 100, and one crawl page. Use PAA click depth 1 only for approved PAA analysis. Record every feature's type and absolute position, target organic position, owner URL/domain where exposed, nested owners, and capture time. Mark features absent from live results as stale rather than opportunities.
6. Select the minimum representative parse set: each distinct target URL plus no more than two distinct winning URLs per keyword, prioritizing feature owners. Deduplicate calls. Do not parse Google-owned entity URLs or inaccessible destinations. Call Content Parsing without JavaScript initially; ask before a JavaScript retry.
7. Compare target and winners using only observed headings, answer form, lists, tables, media, supporting questions, page type, and eligible structured-data context. Label page-format and owner-type determinations as analyst inferences. Never imply that structured data guarantees a feature.
8. Apply the attainability and priority rules in the contract. Give exact page-specific changes: insertion point, proposed heading, answer/list/table structure, media requirements, supporting questions, and eligible schema or external dependency. Do not pad recommendations unsupported by the live composition.
9. Read [templates/report-template.md](templates/report-template.md) and write the detailed Markdown report. Create `<root>/<domain>/` and save `<YYYY-MM-DD>_Serp-Optimization_<domain>.md`; for example, `2026-06-19_Serp-Optimization_example.com.md`. Return the absolute path.

Validate provider task statuses and results. Log each call and returned cost, sum unrounded costs, report incomplete cost coverage, and ask before retries, pagination, extra keywords, or extra winner pages.
