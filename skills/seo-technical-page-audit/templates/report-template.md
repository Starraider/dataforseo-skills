<!--
Use this as a flexible scaffold, not a rigid form.
Delete sections that add no value.
When exact inventories are unavailable, say so explicitly instead of faking precision.
-->

[YYYY-MM-DD]

# Technical SEO Audit: [Page or Title]

## Scope

- URL: `[absolute page URL]`
- Domain: `[normalized domain]`
- Devices: `[desktop and mobile / desktop only / mobile only]`
- Crawl context: `[task-based OnPage crawl or fallback live audit]`
- Render context: `[selected browser preset(s), JS enabled, matching Lighthouse contexts]`
- Total cost: `[x,xx USD]`

## Executive Summary

[2-5 sentences on the page state, the highest-risk issues, and the overall repair priority.]

## Technical Score

| Device | Technical Score | Score Drivers |
| --- | ---: | --- |
| Desktop | `[0-100 or 0 (audit incomplete)]` | `[drivers]` |
| Mobile | `[0-100 or 0 (audit incomplete)]` | `[drivers]` |

<!-- Keep only selected devices. Never average or blend device scores. -->

## Prioritized Findings

| Priority | Context | Issue | Evidence | Fix | Owner | Effort | Validation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P0/P1/P2/P3 | [shared/desktop/mobile/device delta] | [issue] | [short evidence] | [short fix] | [team] | [S/M/L] | [check] |

## P0 Findings

<!-- Omit this section if there are no P0 issues. Repeat the block as needed. -->

### [P0] [Issue Name]

- Context: [shared / desktop / mobile / device delta]
- Evidence: [exact values, URLs, assets, or a clear statement that only aggregate evidence was returned]
- Impact: [why this blocks crawling, indexing, rendering, or conversion]
- Fix: [concrete action]
- Owner: [engineering / SEO / content / ops]
- Effort: [S/M/L]
- Validation: [how to confirm the fix]

## P1 Findings

### [P1] [Issue Name]

- Context: [details]
- Evidence: [details]
- Impact: [details]
- Fix: [details]
- Owner: [details]
- Effort: [details]
- Validation: [details]

## P2 Findings

### [P2] [Issue Name]

- Context: [details]
- Evidence: [details]
- Impact: [details]
- Fix: [details]
- Owner: [details]
- Effort: [details]
- Validation: [details]

## P3 Findings

### [P3] [Issue Name]

- Context: [details]
- Evidence: [details]
- Impact: [details]
- Fix: [details]
- Owner: [details]
- Effort: [details]
- Validation: [details]

## Indexability and Canonicals

- Final status: `[status code]`
- Indexability state: `[indexable / blocked / uncertain]`
- Robots directives: `[meta robots / x-robots / robots.txt evidence]`
- Canonical state: `[self-canonical / points elsewhere / missing / conflicting]`
- Notes: [important nuance]

## Redirects and Links

- Redirect summary: [summary]
- Hreflang summary: [summary]
- Link conflicts: [summary]

### Broken Link Inventory

<!-- Keep only if exact URLs are returned. -->

| Source | Target | Status | Type | Notes |
| --- | --- | --- | --- | --- |
| [URL] | [URL] | [404/500/etc.] | [internal/external] | [note] |

### Redirect Chain Inventory

<!-- Keep only if explicit hops are returned. -->

| Start URL | Hop 1 | Hop 2 | Final URL | Notes |
| --- | --- | --- | --- | --- |
| [URL] | [URL] | [URL] | [URL] | [note] |

## Metadata and Content

- Title: `[value and assessment]`
- Meta description: `[value and assessment]`
- H1 and heading structure: `[assessment]`
- Content ratio and relevance: `[assessment]`
- Special notes: [duplicate tags, missing alt/title, boilerplate, readability, etc.]

## Schema

- Schema summary: `[present / absent / invalid / mixed]`
- Detected types: `[types]`

### Schema Field Findings

| Type | Field | Issue | Recommended Fix |
| --- | --- | --- | --- |
| [schema type] | [field] | [missing/invalid/conflicting] | [fix] |

## Resources and Performance

- Shared resource summary: [facts that do not vary by device]

### Top Resource Offenders

| Context | Asset | Type | Problem | Evidence | Recommended Fix |
| --- | --- | --- | --- | --- | --- |
| [shared/desktop/mobile] | [URL] | [script/image/css] | [large/uncached/broken/render-blocking] | [metric] | [fix] |

## Desktop–Mobile Differences

<!-- Include only when both devices were requested. Omit rows without a meaningful difference. Do not duplicate shared SEO checks here. -->

| Area | Desktop Evidence | Mobile Evidence | Material Difference / Action |
| --- | --- | --- | --- |
| Viewport, scaling, touch, fonts | [evidence] | [evidence] | [delta and fix] |
| Resource selection and critical path | [evidence] | [evidence] | [delta and fix] |
| Responsive images | [evidence] | [evidence] | [delta and fix] |
| JavaScript/rendered-content parity | [evidence] | [evidence] | [delta and fix] |
| LCP/CLS/FCP/TBT/Speed Index | [evidence] | [evidence] | [delta and fix] |
| Network, caching, service worker | [evidence] | [evidence] | [delta and fix] |
| Mobile-first indexing | [evidence] | [evidence] | [evidence-backed risk or no material delta] |

## Selected-Device Performance

<!-- For a single-device audit, use this section instead of Desktop–Mobile Differences. -->

- TTFB and waterfall summary: [summary]
- Lighthouse summary: [performance, SEO, accessibility, best practices]
- Core Web Vitals summary: [LCP, CLS, FCP, TBT/interaction-related evidence]

## Implementation Plan

1. [Immediate fix]
2. [Next fix]
3. [Follow-up verification or optimization]

## Verification Checklist

- [ ] Re-run the same DataForSEO audit after deployment.
- [ ] Re-run only the originally selected device context(s).
- [ ] Confirm status, indexability, and canonical behavior.
- [ ] Confirm affected links or assets no longer fail.
- [ ] Confirm performance regressions are removed or improved.
- [ ] Confirm schema validates cleanly where applicable.

## Methodology and Call Log

| Endpoint | Purpose | Cost (USD) | Notes |
| --- | --- | --- | --- |
| [endpoint] | [purpose] | [cost] | [note] |

## Limitations

- [missing endpoint, incomplete evidence, auth/cookie restrictions, or other caveat]

## Official References

- [DataForSEO endpoint or help-center article]
