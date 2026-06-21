# Audit Playbook

Use this file for the detailed workflow that no longer fits cleanly in `SKILL.md`.

Validate device parameters and score interpretation against the official [Task POST](https://docs.dataforseo.com/v3/on_page-task_post/), [Instant Pages](https://docs.dataforseo.com/v3/on_page-instant_pages/), [Lighthouse](https://docs.dataforseo.com/v3/on_page-lighthouse-live-json/), and [OnPage score](https://dataforseo.com/help-center/how-on-page-seo-score-is-calculated) documentation.

## Request gating

- Require one absolute HTTP(S) page URL.
- Derive the project domain from the URL hostname.
- Reject malformed URLs, non-HTTP(S) URLs, and credential-bearing URLs.
- Choose one locale for all crawl calls. Use the user-supplied locale when given. Otherwise infer from ccTLD, language subpath, or clear market signals. If still unclear, default to `en-US`.
- Select `desktop` and `mobile` unless the request names only one device. An explicit desktop-only request excludes mobile, and an explicit mobile-only request excludes desktop.
- Default report root is `SEO/<domain>/` unless the user specifies another root.
- The filename must remain `<YYYY-MM-DD>_Techical-Report_<safe-URL>.md`.

## Preferred DataForSEO sequence

1. Create one single-page OnPage crawl with `on_page_task_post` for each selected device. Wait for one task to finish before creating another task for the same host.
   - `target`: normalized domain
   - `start_url`: audited page URL
   - `max_crawl_pages`: `1`
   - `force_sitewide_checks`: `true`
   - `disable_cookie_popup`: `true`
   - `load_resources`: `true`
   - `enable_javascript`: `true`
   - `enable_browser_rendering`: `true`
   - `accept_language`: use the chosen locale; default to `en-US` when there is no stronger signal
   - `validate_micromarkup`: `true`
   - `browser_preset`: the selected `desktop` or `mobile` device
2. Validate each top-level status, task status, returned task ID, and task `browser_preset`.
3. Use each task ID plus audited page URL to collect follow-up evidence from available MCP endpoints:
   - `on_page_pages`
   - `on_page_links`
   - `on_page_redirect_chains`
   - `on_page_non_indexable`
   - `on_page_resources`
   - `on_page_waterfall`
   - `on_page_microdata`
4. Run `on_page_lighthouse` once per selected device with `full_data: true`; set `for_mobile` to `false` for desktop and `true` for mobile. Validate the response task data before labeling its evidence.

## Direct API bridge

If MCP does not expose the task creation or follow-up methods, run:

```bash
python3 <skill-directory>/scripts/fetch_task_onpage.py 'https://example.com/page' --device desktop
python3 <skill-directory>/scripts/fetch_task_onpage.py 'https://example.com/page' --device mobile
```

Run only the command(s) for the selected devices. The helper first reads `<current-project-root>/.env`. The file must define `DATAFORSEO_USERNAME` (or `DATAFORSEO_LOGIN`) and `DATAFORSEO_PASSWORD`. If `.env` is absent, ask the user for the credential file path, wait, and rerun with `--env-file '<path>'`. Pass `--accept-language '<locale>'` whenever the chosen locale is not the default `en-US`. Never ask for or print credential values. Exit status `2` with `status: env_file_required` means a path is still required; it is not an API failure and must not trigger fallback.

The helper creates one device-specific task, polls `summary`, and returns task post, summary, pages, links, redirect chains, non-indexable pages, resources, waterfall, and microdata as one JSON object plus a `normalized` summary block. Treat it as successful only when exit status is `0`, stdout has `status: complete`, and both top-level and normalized `device` match the requested device. Use `costs_usd` for cost accounting. If an endpoint reports more total items than returned items, disclose that the inventory is truncated.

Continue to use matching MCP Lighthouse calls. Do not run the helper when MCP task methods already succeeded, and do not retry it automatically after failure because a task may already have been billed.

## Optional billable escalations

Ask before using these:

- `on_page_content_parsing_live` when title relevance, heading hierarchy, or boilerplate dilution is still unclear.
- `on_page_page_screenshot` when rendered state, hidden content, overlays, or layout instability remain unclear.

## Fallback

If task-based endpoints are unavailable in MCP and the direct API bridge fails, fall back for each selected device to:

- `on_page_instant_pages` with matching `browser_preset`, JavaScript, browser rendering, and resources enabled
- `on_page_lighthouse` with matching `for_mobile`

When falling back, keep the same report structure and explicitly state which exact inventories could not be produced.

## Evidence rules

- Only claim redirect chains when explicit chain evidence is returned.
- Only list broken links or broken assets when DataForSEO returns exact URLs.
- Treat resource-level `checks.is_broken` and exact parser/runtime errors as broken-asset evidence even when `status_code` is `200`.
- If only booleans, counts, or aggregate flags are available, say that exact affected items were not returned.
- Never invent schema types, field errors, redirect hops, broken targets, or score deductions.
- Use rounded DataForSEO `onpage_score` as the Technical Score. Never substitute a Lighthouse score.
- Report one score per selected device. For both devices, present desktop and mobile side by side without averaging or blending. If a score is unavailable, report `0 (audit incomplete)` for that device and explain why.
- Prefer `normalized.page_timing_source`, `normalized.truncated_inventories`, `normalized.broken_resource_urls`, and `normalized.waterfall_page_url_anomaly` over ad hoc response-shape assumptions.

## Analysis checklist

Cover these areas when evidence exists:

- Availability and final status code
- Indexability, robots directives, and non-indexable reasons
- Canonicalization and canonical targets
- Redirects, hreflang, broken links, and link conflicts
- Title, description, headings, content ratios, and relevance signals
- Schema presence, types, field-level issues, and invalid markup
- Resources, caching, compression, minification, size, and loading impact
- TTFB, waterfall bottlenecks, Lighthouse opportunities, and Core Web Vitals
- If the waterfall payload groups resources oddly or reports anomalous page URLs, prefer `pages.page_timing` for page-level timings and cite the waterfall only for resource-level blocking evidence
- Sitewide single-page checks enabled by `force_sitewide_checks`

## Device comparison contract

For one selected device, evaluate the full checklist in that device context. For desktop and mobile together:

1. Use one shared baseline for status/indexability, robots, canonicals, redirects, hreflang, broken links, title/description, headings, content, and schema. Do not repeat identical inventories, findings, or recommendations.
2. Compare only render- or runtime-sensitive evidence: viewport and scaling; touch targets and font size; selected responsive images; resource set, order, priority, and critical path; rendered-content or JavaScript behavior; LCP, CLS, FCP, TBT/interaction proxies, Speed Index, and timing; throttling; cache behavior; service workers; and mobile usability.
3. Report a shared field by device only when direct evidence differs. Label it a parity issue and show both values.
4. Claim a mobile-first-indexing risk only when mobile evidence shows missing, blocked, or materially different primary content, metadata, structured data, canonicals/robots, internal links, images, or required resources. Do not infer it from a slower mobile score alone.
5. Keep shared findings once in the main sections and place material device deltas in the device-comparison section. Omit non-material rows.

## Prioritization

- `P0`: availability or indexation blockers
- `P1`: material discovery, rendering, or user-harm issues
- `P2`: important optimization work
- `P3`: enhancements

Every finding should include:

- evidence
- impact
- fix
- owner
- effort
- validation

Add a `Score Drivers` section that names the major returned issues depressing the score, but do not assign undocumented weights.

## Cost accounting

- Log every endpoint used with its top-level `cost` in USD.
- Sum unrounded values.
- Report `Total cost: x,xx USD`.
- If any cost is missing, mark the subtotal incomplete and name the affected calls.

## Writing rules

- Use the template file as the starting scaffold, not a rigid output.
- Remove empty sections when there is nothing useful to report.
- Keep recommendations concrete and imperative.
- Stay stack-agnostic unless the evidence clearly points to a specific CMS, framework, or server layer.
- Cite exact values from DataForSEO, but do not paste raw customer response bodies.
