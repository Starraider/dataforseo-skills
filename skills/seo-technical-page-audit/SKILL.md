---
name: seo-technical-page-audit
description: "Use when auditing one webpage for technical SEO, indexability, redirects, links, metadata, structured data, or performance and producing a prioritized report with a 0-100 Technical Score."
license: "(MIT AND CC-BY-SA-4.0). See LICENSE-MIT and LICENSE-CC-BY-SA-4.0"
compatibility: "Requires the official DataForSEO MCP server with the ONPAGE module enabled and filesystem write access."
---

# SEO Technical Page Audit

Use the official [Instant Pages](https://docs.dataforseo.com/v3/on_page/instant_pages/), [Lighthouse](https://docs.dataforseo.com/v3/on_page-lighthouse-live-json/), and [OnPage score](https://dataforseo.com/help-center/how-on-page-seo-score-is-calculated) references.

## Workflow

1. Require a project domain. Derive it from a supplied absolute page URL; otherwise ask and wait. Also ask when the URL is absent. Reject malformed or credential-bearing URLs. Normalize the domain to a lowercase hostname without port, URL suffix, trailing dot, or leading `www.`.
2. Through DataForSEO MCP, call `on_page_instant_pages` with the URL and `enable_javascript: true`, then `on_page_lighthouse` with the same URL, JavaScript enabled, and `full_data: true`. The request authorizes these billable calls; ask before retries or additional URLs.
3. Validate provider/task statuses. Never invent fields; state failures and limitations.
4. Inspect HTTP status and redirects; indexability, robots directives, canonicalization, HTTPS, and mixed content; title, description, headings, content signals, and image alt checks; broken-link/resource flags; microdata presence/errors; loading checks, page timing, Lighthouse categories, Core Web Vitals, and render-blocking or oversized assets.
5. Claim a redirect chain only when Lighthouse shows multiple hops. If only a broken-link flag exists, recommend a scoped crawl without inventing URLs.
6. Set **Technical Score** to rounded DataForSEO `onpage_score` (0-100). If unavailable, use `0 (audit incomplete)` and explain; never substitute Lighthouse.
7. Prioritize P0 availability/indexing blockers, P1 material discovery/rendering/user harm, P2 important optimizations, and P3 enhancements. Each finding needs evidence, impact, fix, effort, and validation. Flag missing schema only when absent, invalid, or appropriate to visible content.

## Report file

Use the requested report root or `<current-working-directory>/SEO`; create its normalized domain child. Allow letters, numbers, dots, hyphens, and underscores; replace other runs with `_`, trim separators, and cap components at 140 characters. Derive `<URL>` by removing scheme, fragment, query, and trailing slash, then sanitizing. Write:

`<report-root>/<domain>/<YYYY-MM-DD>_Techical-Report_<URL>.md`

Use the local ISO date; for example, `SEO/example.com/2026-06-19_Techical-Report_example.com_products_widget.md`. Preserve the requested `Techical-Report` spelling. Make the first line the ISO date.

## Report structure

Include title/URL; summary; score; crawl/render facts; prioritized table and P0-P3 details; indexability/canonicalization; redirects/links; metadata/content; schema; performance/Core Web Vitals; implementation plan; verification; methodology, MCP calls, timestamp, limitations, and official links. Cite exact values without raw customer responses.

Return the saved absolute path and a concise summary.
