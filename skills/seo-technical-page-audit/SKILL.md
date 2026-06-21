---
name: seo-technical-page-audit
description: "Use when auditing one webpage for technical SEO, indexability, links, metadata, structured data, or desktop/mobile rendering and performance, then producing a prioritized report with DataForSEO-derived Technical Scores."
compatibility: "Requires the official DataForSEO MCP server with the ONPAGE module enabled, Python 3, a DataForSEO credential .env file for direct task API access, and filesystem write access."
---

# SEO Technical Page Audit

Read `references/audit-playbook.md` before acting and use `templates/report-template.md` as the report scaffold. Follow its linked official DataForSEO documentation.

## Workflow

1. Require one absolute HTTP(S) page URL. Derive and normalize its domain; reject malformed or credential-bearing URLs.
2. Choose one locale: requested, clear site signal, then `en-US`. Select desktop and mobile by default. When the request names only one device, select only it and never call or report the other.
3. Prefer MCP task methods. Create one OnPage task per selected device with matching `browser_preset`. Run Lighthouse per selected device with `full_data: true` and `for_mobile: false` for desktop or `true` for mobile.
4. If task methods are absent, locate the project `.env` or ask only for its path. Per selected device run `python3 <skill-directory>/scripts/fetch_task_onpage.py '<page-url>' --device <device>` with optional `--env-file` and `--accept-language`. Accept only exit `0`, `status: complete`, and matching device. Treat exit `2` as a credential-path request. After other failures, use the playbook fallback without automatic billable retries.
5. Ask before `on_page_content_parsing_live` or `on_page_page_screenshot`.
6. For one device, analyze all evidence in that context. For both, report invariant evidence once: availability, indexability, robots, canonicals, redirects, hreflang, broken links, metadata, headings, content, and schema.
7. When both are selected, compare only meaningful render/runtime differences: viewport, touch targets, fonts/scaling, responsive images, resource selection/order and critical path, JavaScript/rendered-content parity, layout shift and performance, throttling, caching/service workers, and mobile-first-indexing risks. Report shared fields by device only when direct evidence materially differs; label these parity issues.
8. Claim chains and broken URLs/assets only from exact evidence. Treat resource `checks.is_broken` or parser/runtime errors as valid with HTTP `200`. Report rounded `onpage_score` per selected device, or `0 (audit incomplete)` when missing. Show dual scores side by side; never blend them or invent weights.
9. Use normalized helper fields for device identity and stable summaries, raw payloads for evidence. Prioritize P0-P3; include evidence, impact, fix, owner, effort, and validation.

## Cost accounting

Log each endpoint and top-level USD cost. Sum unrounded values. Mark missing-cost subtotals incomplete.

## Report file

Use the requested root or `<current-working-directory>/SEO`, then its domain child. Sanitize `<URL>` after removing scheme, query, fragment, and trailing slash. Write:

`<report-root>/<domain>/<YYYY-MM-DD>_Techical-Report_<URL>.md`

Use the local ISO date as the first line. Preserve `Techical-Report`.

## Report structure

Follow the template, remove empty sections, and return the saved absolute path plus a concise summary.
