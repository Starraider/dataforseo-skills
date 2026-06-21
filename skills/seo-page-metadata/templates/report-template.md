# YYYY-MM-DD Page Metadata Report: `<redacted report URL>`

## Executive summary

- Recommended package: **[A/B/C]**
- Primary target keyword: **[keyword]**
- Keyword coverage: **[selected] of [unique relevant] eligible rows selected**
- Main limitation: [none or concise limitation]

## Scope

| Field | Value |
| --- | --- |
| Supplied URL | `[supplied URL with query/fragment contents redacted]` |
| Request URL | `[validated URL without fragment]` |
| Resolved page URL | `[returned URL or null]` |
| Project domain | `[normalized domain]` |
| Country | `[country]` |
| Country source | `[user / primary content / default]` |
| Language | `[language code]` |
| Language source | `[user / primary content / default]` |
| Content service geography | `[value or not established]` |
| Captured at | `[ISO-8601 timestamp with timezone]` |
| Planned calls | `7 (2 OnPage + 5 Related Keywords)` |
| Completed calls | `[count]` |
| Total cost | `x,xx USD [or incomplete subtotal]` |

State any conflict between user market settings and primary-content geography. State that existing metadata, the URL, domain, path, canonical, and TLD were excluded from positive topic and seed derivation.

## Current metadata audit

| Field | Current value | Count/status |
| --- | --- | --- |
| HTTP status / resource type | [value] | [status] |
| Page title | [value or null] | [count] |
| Meta description | [value or null] | [count] |
| Canonical | [value or null] | — |
| Meta keywords | [value or null] | Legacy field |
| Open Graph title | [value or null] | [count] |
| Open Graph description | [value or null] | [count] |
| Twitter card | [value or null] | — |
| Twitter title | [value or null] | [count] |
| Twitter description | [value or null] | [count] |

## Primary-content evidence

### Topic and intent

[Concise evidence-backed finding with short excerpts or paraphrases.]

### Geography and language

[Evidence, rejected boilerplate geography, market choice, language choice, and conflicts.]

## Seed keywords

| # | Seed | Primary-content evidence | Geography rationale |
| ---: | --- | --- | --- |
| 1 | [seed] | [evidence] | [rationale] |
| 2 | [seed] | [evidence] | [rationale] |
| 3 | [seed] | [evidence] | [rationale] |
| 4 | [seed] | [evidence] | [rationale] |
| 5 | [seed] | [evidence] | [rationale] |

## Keyword coverage

| Measure | Count |
| --- | ---: |
| Requested maximum | 125 |
| Returned rows | [count] |
| Exact-seed rows removed | [count] |
| Unique normalized rows | [count] |
| Rows with volume and KD | [count] |
| Relevance exclusions | [count] |
| Metric conflicts | [count] |
| Selected opportunities | [0-20] |

List each exclusion reason and count. Explain any shortfall below 20.

## Ranked keyword opportunities

`opportunity_proxy = search_volume / (keyword_difficulty + 10)`

The proxy is analyst-derived, not supplied by DataForSEO, and does not guarantee low competition. Organic KD is distinct from paid Ads competition.

| # | Keyword | Volume | Organic KD | Ads competition | CPC (USD) | Opportunity proxy | Source seeds |
| ---: | --- | ---: | ---: | --- | ---: | ---: | --- |
| 1 | [keyword] | [value] | [value] | [value/level] | [value] | [value] | [seeds] |

## Metadata packages

Length ranges below are editorial targets, not display guarantees. Counts are Unicode code points.

### Package A — Recommended

- Target keyword: **[keyword]**
- Rationale: [why this package best matches evidence and intent]
- Page title ([count]): `[text]`
- Meta description ([count]): `[text]`
- Open Graph title ([count]): `[text]`
- Open Graph description ([count]): `[text]`
- Twitter title ([count]): `[text]`
- Twitter description ([count]): `[text]`
- [Omit unless explicitly requested] Legacy meta keywords: `[list]`

### Package B

[Use the same fields and a coherent alternative angle.]

### Package C

[Use the same fields and a coherent alternative angle.]

## Implementation guidance

1. [Highest-priority action.]
2. [Validation or deployment guidance.]
3. [Measurement guidance.]

## Limitations

- [Coverage, missing metrics, evidence constraints, rendering, or market limitations.]
- Search volume and KD reflect the selected DataForSEO country/language scope.
- [Include only when legacy meta keywords were requested] Google and Bing do not use meta keywords for rankings; any included list is legacy-only.

## Call log

| # | Tool | Scope-defining arguments | Provider/task status | Returned | Cost (USD) | Limitation |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 1 | `on_page_instant_pages` | [URL and rendering settings] | [status] | [count] | [cost/null] | [text] |

Name every call with a missing cost and label the total incomplete.

## Method and official references

- Normalization: Unicode NFKC, collapsed whitespace, casefolded deduplication, merged seed provenance.
- Evidence boundary: only qualifying Content Parsing main-topic headings and primary text support topic, intent, geography, seeds, and claims.
- [OnPage Instant Pages](https://docs.dataforseo.com/v3/on_page/instant_pages/)
- [OnPage Content Parsing Live](https://docs.dataforseo.com/v3/on_page-content_parsing-live/)
- [Google Related Keywords Live](https://docs.dataforseo.com/v3/dataforseo_labs-google-related_keywords-live/)
- [Keyword Difficulty calculation](https://dataforseo.com/help-center/what-is-keyword-difficulty-and-how-is-it-calculated)
- [Meta keywords guidance](https://dataforseo.com/help-center/meta-keywords)
