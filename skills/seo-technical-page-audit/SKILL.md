---
name: seo-technical-page-audit
description: "Use when auditing one webpage for technical SEO, indexability, redirects, links, metadata, structured data, or performance and producing a prioritized report with a 0-100 Technical Score."
compatibility: "Requires the official DataForSEO MCP server with the ONPAGE module enabled and filesystem write access."
---

# SEO Technical Page Audit

Before acting, read `references/audit-playbook.md` and use `templates/report-template.md` as the default scaffold.

Use the official [Task POST](https://docs.dataforseo.com/v3/on_page/task_post/), [Links](https://docs.dataforseo.com/v3/on_page/links/), [Resources](https://docs.dataforseo.com/v3/on_page/resources/), [Lighthouse](https://docs.dataforseo.com/v3/on_page/lighthouse/live/json/), and [OnPage score](https://dataforseo.com/help-center/how-on-page-seo-score-is-calculated) references.

## Workflow

1. Require an absolute HTTP(S) page URL. Derive the project domain from its hostname; otherwise ask and wait. Reject malformed or credential-bearing URLs. Normalize the domain to lowercase without port, trailing dot, or leading `www.`.
2. Prefer a task-based crawl via `on_page_task_post` with `target` = domain, `start_url` = page URL, `max_crawl_pages: 1`, `force_sitewide_checks: true`, `load_resources: true`, `enable_javascript: true`, `validate_micromarkup: true`, and `browser_preset: desktop`.
3. Validate statuses and keep the task ID plus audited page URL. Then collect available follow-up evidence from `on_page_pages`, `on_page_links`, `on_page_redirect_chains`, `on_page_non_indexable`, `on_page_resources`, `on_page_waterfall`, `on_page_microdata`, and `on_page_lighthouse` with `full_data: true`.
4. Optional billable escalations only after asking: `on_page_content_parsing_live` and `on_page_page_screenshot`.
5. If task-based endpoints are unavailable, fall back to `on_page_instant_pages` plus `on_page_lighthouse` and mark exact inventories that could not be produced.
6. Analyze availability, indexability, robots, canonicals, redirects, hreflang, exact broken links, metadata, headings, content ratios, schema, resources, TTFB and waterfall, Lighthouse audits, Core Web Vitals, and sitewide checks.
7. Only claim redirect chains from explicit evidence. Only list broken URLs or assets when returned exactly. Use rounded DataForSEO `onpage_score` as Technical Score; if unavailable use `0 (audit incomplete)`. Add Score Drivers without invented weights.
8. Prioritize P0-P3. Every finding needs evidence, impact, fix, owner, effort, and validation.

## Cost accounting

Log each endpoint and top-level `cost` USD. Sum unrounded values and report `Total cost: x,xx USD`. Missing cost means incomplete subtotal; name affected calls.

## Report file

Use the requested report root or `<current-working-directory>/SEO`, then its normalized domain child. Derive `<URL>` by removing scheme, query, fragment, and trailing slash, then sanitizing. Write:

`<report-root>/<domain>/<YYYY-MM-DD>_Techical-Report_<URL>.md`

Use the local ISO date; for example, `SEO/example.com/2026-06-20_Techical-Report_example.com_products_widget.md`. Preserve `Techical-Report`. Make the first line the ISO date.

## Report structure

Follow the linked template. Include exact inventories when DataForSEO returns them, cite exact values instead of raw responses, and return the saved absolute path plus a concise summary.
