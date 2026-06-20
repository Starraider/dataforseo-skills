---
name: seo-technical-page-audit
description: "Use when auditing one webpage for technical SEO, indexability, redirects, links, metadata, structured data, or performance and producing a prioritized report with a 0-100 Technical Score."
compatibility: "Requires the official DataForSEO MCP server with the ONPAGE module enabled, Python 3, a DataForSEO credential .env file for direct task API access, and filesystem write access."
---

# SEO Technical Page Audit

Before acting, read `references/audit-playbook.md` and use `templates/report-template.md` as the default scaffold.

Use the official [Task POST](https://docs.dataforseo.com/v3/on_page/task_post/), [Links](https://docs.dataforseo.com/v3/on_page/links/), [Resources](https://docs.dataforseo.com/v3/on_page/resources/), [Lighthouse](https://docs.dataforseo.com/v3/on_page/lighthouse/live/json/), and [OnPage score](https://dataforseo.com/help-center/how-on-page-seo-score-is-calculated) references.

## Workflow

1. Require one absolute HTTP(S) page URL. Derive the project domain from its hostname. Reject malformed or credential-bearing URLs. Normalize the domain to lowercase without port, trailing dot, or leading `www.`.
2. Choose one locale for all crawl calls: user-supplied first, then clear site/URL signals, otherwise `en-US`.
3. Prefer MCP task methods when `on_page_task_post` and its result methods are exposed. Use the parameters in the playbook and collect all listed task evidence.
4. When those task methods are absent from MCP, look for `.env` in the project root. If absent, ask for the credential file path; never ask for values. Run `python3 <skill-directory>/scripts/fetch_task_onpage.py '<page-url>'`; add `--env-file '<path>'` when supplied and `--accept-language '<locale>'` when not using the default `en-US`. Accept only exit status `0` with `status: complete`. Continue with MCP `on_page_lighthouse` using `full_data: true`.
5. Optional billable escalations only after asking: `on_page_content_parsing_live` and `on_page_page_screenshot`.
6. Exit status `2` or `status: env_file_required` means ask for the `.env` path, not fallback. If the helper fails after credentials are located, fall back to MCP `on_page_instant_pages` plus `on_page_lighthouse` and mark unavailable inventories. Do not retry automatically because Task POST is billable.
7. Analyze availability, indexability, robots, canonicals, redirects, hreflang, exact broken links, metadata, headings, content ratios, schema, resources, TTFB and waterfall, Lighthouse audits, Core Web Vitals, and sitewide checks.
8. Only claim redirect chains from explicit evidence. Only list broken URLs or assets when returned exactly. Treat resource-level `checks.is_broken` or parser/runtime errors as valid broken-asset evidence even when the HTTP status is `200`. Use rounded DataForSEO `onpage_score` as Technical Score; if unavailable use `0 (audit incomplete)`. Add Score Drivers without invented weights.
9. Prefer the helper's `normalized` summary block for timing source, truncated inventories, exact broken assets, and waterfall anomalies; use raw payloads for cited evidence.
10. Prioritize P0-P3. Every finding needs evidence, impact, fix, owner, effort, and validation.

## Cost accounting

Log each endpoint and top-level `cost` USD. Sum unrounded values and report `Total cost: x,xx USD`. Missing cost means an incomplete subtotal; name affected calls.

## Report file

Use the requested report root or `<current-working-directory>/SEO`, then its normalized domain child. Derive `<URL>` by removing scheme, query, fragment, and trailing slash, then sanitizing. Write:

`<report-root>/<domain>/<YYYY-MM-DD>_Techical-Report_<URL>.md`

Use the local ISO date. Preserve `Techical-Report`. Make the first line the ISO date.

## Report structure

Follow the linked template. Include exact inventories when returned, cite exact values instead of raw responses, and return the saved absolute path plus a concise summary.
