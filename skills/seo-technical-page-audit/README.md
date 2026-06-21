# SEO Technical Page Audit

`seo-technical-page-audit` audits one specific, publicly reachable HTTP(S) page for technical SEO problems. It analyzes desktop and mobile by default, or only the explicitly requested device, using DataForSEO page, crawl, link, resource, schema, rendering, and Lighthouse evidence. It reports provider-derived Technical Scores and writes a prioritized, implementation-ready Markdown report.

## What the skill does

The skill:

1. Validates the supplied absolute page URL and derives the project domain.
2. Chooses one locale for all crawl calls, using a requested locale, a clear site signal, or `en-US`.
3. Selects desktop and mobile unless the request asks for only one of them, then runs one matching task-based DataForSEO OnPage crawl and Lighthouse audit per selected device. If task methods are unavailable, it uses the included Python bridge and a git-ignored DataForSEO credential `.env` file.
4. Collects HTTP status, redirects, indexability, robots directives, canonicals, hreflang, links, metadata, headings, content ratios, structured data, resources, page timing, Lighthouse audits, and Core Web Vitals. Dual-device reports present invariant evidence once and compare only meaningful render or runtime differences.
5. Uses the rounded DataForSEO `onpage_score` as the Technical Score for each selected device. It reports `0 (audit incomplete)` when a device score is unavailable and never blends device scores or substitutes Lighthouse scores.
6. Prioritizes every supported finding from P0 to P3 and supplies evidence, impact, fix, owner, effort, and a validation step.
7. Records DataForSEO endpoint costs and writes the final report to disk.

The audit is for one supplied page, although task-based evidence may expose sitewide issues relevant to that page. It only reports exact broken URLs, assets, or redirect chains when DataForSEO returned the necessary evidence. In a desktop-and-mobile audit, shared checks such as titles, headings, canonicals, and broken links appear once unless returned evidence proves a material device-specific difference.

## Why this analysis matters

Search engines need to reach, understand, and load a page before they can confidently show it in search results. Problems such as a blocked page, a wrong canonical address, broken links, confusing redirects, missing page titles, or slow loading can make a useful page harder to find or unpleasant to use. A technical audit brings these hidden obstacles together in one place and separates urgent problems from minor improvements.

Fixing the reported issues can make it easier for search engines to discover the correct page, read its content, and present it to the right audience. Faster pages and clearer navigation can also improve the experience for visitors, which supports engagement and conversions. The audit does not guarantee a higher position—content quality, competition, links, and many other factors also matter—but it helps ensure that technical faults are not holding the page back.

## Requirements and inputs

- The official DataForSEO MCP server with the OnPage module enabled.
- Python 3 and filesystem write access.
- A DataForSEO credential `.env` file for task endpoints not exposed through MCP. The skill asks for the file path, never the credential values, when it cannot find the file in the project root.
- One absolute `http://` or `https://` page URL. A bare domain or relative path is insufficient.

Optional inputs include a locale and a report root. The default report root is `SEO/` below the current working directory. Optional content-parsing and screenshot calls require separate approval because they are billable escalations.

Desktop and mobile are selected by default. A request for desktop only or mobile only restricts all OnPage and Lighthouse calls to that device.

## Invocation examples

Directly by skill name:

```text
Use the seo-technical-page-audit skill to audit https://example.com/products/widget.
```

With an explicit locale:

```text
Audit https://example.de/produkte/widget for technical SEO with locale de-DE.
```

With a custom report location:

```text
Run a technical page audit for https://example.com/pricing and save the report under ./client-reports.
```

For one device only:

```text
Audit https://example.com/pricing for mobile only.
```

With a credential-file location supplied in advance:

```text
Use seo-technical-page-audit for https://example.com/. If direct task access is needed, use the credentials file at ~/.config/dataforseo/client.env.
```

If no absolute page URL is supplied, the skill pauses and asks for one before making billable requests.

## What to expect in the report

The first line is the local ISO date. By default, the file is saved as:

```text
SEO/<domain>/<YYYY-MM-DD>_Techical-Report_<safe-URL>.md
```

`Techical-Report` is intentionally preserved in the filename for compatibility. The report contains:

- Scope, selected devices, crawl/render contexts, and total DataForSEO cost.
- An executive summary and the provider-derived Technical Score for each selected device with its main drivers.
- A prioritized findings table followed by detailed P0–P3 findings.
- Indexability, canonical, robots, redirect, hreflang, and link analysis.
- Exact broken-link, redirect-chain, schema-field, and resource inventories when returned.
- Shared metadata, headings, content, and structured-data findings without device duplication.
- For dual-device audits, only material differences in viewport/mobile usability, responsive resources, JavaScript/rendering, critical paths, timing and Core Web Vitals, caching/service workers, and mobile-first-indexing parity.
- An ordered implementation plan and verification checklist.
- Methodology, endpoint call log, limitations, and official DataForSEO references.

Every finding is tied to returned evidence. Missing inventories, restricted pages, absent endpoint data, incomplete costs, or fallback-mode limitations are stated explicitly. The skill returns the absolute report path and a concise result summary after writing the file.
