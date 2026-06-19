---
name: seo-technical-page-audit
description: "Use when auditing one specific webpage for technical SEO, page health, indexability, redirects, broken links, metadata, structured data, or performance and producing a prioritized Markdown report with a 0-100 Technical Score."
license: "(MIT AND CC-BY-SA-4.0). See LICENSE-MIT and LICENSE-CC-BY-SA-4.0"
compatibility: "Requires the official DataForSEO MCP server with the ONPAGE module enabled and filesystem write access."
---

# SEO Technical Page Audit

Audit one absolute HTTP(S) URL with current DataForSEO evidence and write a decision-ready report.

Use the official [Instant Pages](https://docs.dataforseo.com/v3/on_page/instant_pages/), [Lighthouse](https://docs.dataforseo.com/v3/on_page-lighthouse-live-json/), and [OnPage score](https://dataforseo.com/help-center/how-on-page-seo-score-is-calculated) references.

## Workflow

1. If no page URL was supplied, ask for it and wait. Reject malformed or credential-bearing URLs; keep query strings out of filenames.
2. Use the official DataForSEO MCP server. Call `on_page_instant_pages` with the URL and `enable_javascript: true`. Then call `on_page_lighthouse` with the same URL, `enable_javascript: true`, and `full_data: true`. These live calls are billable; the audit request authorizes these two calls, but ask before retries or additional URL checks.
3. Verify provider and task statuses before interpreting results. Never invent missing fields. State crawl/render failures and evidence limitations explicitly.
4. Inspect HTTP status and redirects; indexability, robots directives, canonicalization, HTTPS, and mixed content; title, description, headings, content signals, and image alt checks; broken-link/resource flags; microdata presence/errors; loading checks, page timing, Lighthouse categories, Core Web Vitals, and render-blocking or oversized assets.
5. Use Lighthouse redirect details to identify a chain only when the returned audit evidence shows multiple hops. A lone redirect is not a chain. If DataForSEO only flags broken links without returning destinations, report the flag and recommend a scoped crawl instead of naming unverified URLs.
6. Set **Technical Score** to the rounded DataForSEO `onpage_score` (0-100). If the page cannot be fetched or scored, use `0 (audit incomplete)` and explain why; do not substitute a Lighthouse category score.
7. Prioritize findings: P0 blocks crawling/indexing or page availability; P1 materially harms discovery, rendering, or users; P2 is an important optimization; P3 is an enhancement. Every finding needs evidence, impact, an implementable fix, effort, and a validation step. Treat missing schema as a gap only when markup is absent, invalid, or clearly appropriate to visible page content.

## Report file

Use the requested directory or `<current-working-directory>/SEO`; create it. Sanitize the target to letters, numbers, dots, hyphens, and underscores; replace other runs with `_`, trim separators, cap at 140 characters. Derive `<URL>` by removing the scheme, fragment, query, and trailing slash, replacing unsafe character runs with `_`, and limiting it to 140 characters. Write:

`<YYYY-MM-DD>_Techical-Report_<URL>.md`

Use the local ISO date; for example, `2026-06-19_Techical-Report_example.com_products_widget.md`. Preserve the requested `Techical-Report` spelling. Make the first line the ISO date.

## Report structure

Include: title and audited URL; executive summary; Technical Score and interpretation; crawl/render facts; prioritized findings table; detailed findings grouped P0-P3; indexability and canonicalization; redirects and links; metadata/content; schema; performance and Core Web Vitals; prioritized implementation plan; verification checklist; methodology, DataForSEO MCP calls, audit timestamp, limitations, and official DataForSEO documentation links. Cite exact returned values without embedding raw customer response data.

Return the saved absolute path and a concise summary.
