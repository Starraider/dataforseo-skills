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
- Crawl context: `[task-based OnPage crawl or fallback live audit]`
- Render context: `[desktop preset, JS enabled, Lighthouse context]`
- Total cost: `[x,xx USD]`

## Executive Summary

[2-5 sentences on the page state, the highest-risk issues, and the overall repair priority.]

## Technical Score

- Technical Score: `[0-100 or 0 (audit incomplete)]`
- Score Drivers: `[main issues likely depressing the score]`

## Prioritized Findings

| Priority | Issue | Evidence | Fix | Owner | Effort | Validation |
| --- | --- | --- | --- | --- | --- | --- |
| P0/P1/P2/P3 | [issue] | [short evidence] | [short fix] | [team] | [S/M/L] | [check] |

## P0 Findings

<!-- Omit this section if there are no P0 issues. Repeat the block as needed. -->

### [P0] [Issue Name]

- Evidence: [exact values, URLs, assets, or a clear statement that only aggregate evidence was returned]
- Impact: [why this blocks crawling, indexing, rendering, or conversion]
- Fix: [concrete action]
- Owner: [engineering / SEO / content / ops]
- Effort: [S/M/L]
- Validation: [how to confirm the fix]

## P1 Findings

### [P1] [Issue Name]

- Evidence: [details]
- Impact: [details]
- Fix: [details]
- Owner: [details]
- Effort: [details]
- Validation: [details]

## P2 Findings

### [P2] [Issue Name]

- Evidence: [details]
- Impact: [details]
- Fix: [details]
- Owner: [details]
- Effort: [details]
- Validation: [details]

## P3 Findings

### [P3] [Issue Name]

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

- TTFB and waterfall summary: [summary]
- Lighthouse summary: [performance, SEO, accessibility, best practices]
- Core Web Vitals summary: [LCP, CLS, FCP, INP/FID-related evidence]

### Top Resource Offenders

| Asset | Type | Problem | Evidence | Recommended Fix |
| --- | --- | --- | --- | --- |
| [URL] | [script/image/css] | [large/uncached/broken/render-blocking] | [metric] | [fix] |

## Implementation Plan

1. [Immediate fix]
2. [Next fix]
3. [Follow-up verification or optimization]

## Verification Checklist

- [ ] Re-run the same DataForSEO audit after deployment.
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
