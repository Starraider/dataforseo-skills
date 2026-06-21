# SEO Page Metadata Data Contract

Read this file before calling DataForSEO. Treat the active MCP input schema as authoritative when it differs from examples here.

## 1. Inputs and URL safety

- Require one absolute `http://` or `https://` page URL with a hostname.
- Reject embedded username/password credentials, control characters, unsupported schemes, and malformed URLs.
- Keep the supplied URL transiently. Remove only its fragment for DataForSEO calls because fragments are not sent in HTTP requests; preserve its query string for the page request. In the report Scope section, replace query and fragment contents with `[redacted]`.
- Normalize the project directory hostname to lowercase IDNA, remove a leading `www.`, trailing dot, and port, and replace IPv6 colons with hyphens.
- Resolve a relative report root against the current working directory. The default root is `<cwd>/SEO`.
- Use `scripts/metadata_support.py filename` for validation and deterministic paths. The readable filename excludes query and fragment text and always ends with an eight-character SHA-256 suffix so sanitized, truncated, or query-bearing URLs do not collide or expose query values.

## 2. Planned calls and request settings

The normal successful workflow makes exactly seven billable calls:

1. `on_page_instant_pages` once.
2. `on_page_content_parsing` once.
3. `dataforseo_labs_google_related_keywords` once for each of five approved seeds.

State this plan before calling. Use the validated request URL for both OnPage calls. Supply `accept_language` only when a user override or already-established content language supports it. Omit JavaScript rendering initially. Ask before retrying with `enable_javascript: true` because it can cost more.

Each Related Keywords call uses:

```json
{
  "keyword": "approved seed",
  "location_name": "selected country",
  "language_code": "selected language code",
  "depth": 2,
  "limit": 25,
  "order_by": ["keyword_data.keyword_info.search_volume,desc"]
}
```

Do not send `include_seed_keyword` unless the active MCP schema exposes it. Its REST default is `false`; if an exact seed row nevertheless appears, remove it during local normalization.

Do not retry, paginate, fan out, or add a resolver call without approval. When a DataForSEO Labs location/language resolver exists in the active MCP, use it for an uncertain pair. If it is absent, ask the user rather than bypassing MCP or guessing.

## 3. Response validation

For each MCP result:

1. Confirm transport/tool success.
2. Parse JSON from `CallToolResult.content[].text`; text beginning with `Error:` is failure.
3. Require provider `status_code == 20000`.
4. Require a non-empty `tasks` array and `tasks_error == 0` when present.
5. Require every task `status_code == 20000` and retain its `status_message`, `cost`, and returned counts.
6. Require result objects and expected item types. For OnPage, require `crawl_progress == "finished"` and a page HTTP status in the 200-299 range.
7. Classify Content Parsing evidence mode. Prefer `structured_main_topic` when `page_content.main_topic[]` contains qualifying headings or text. Classify `projection_degraded_text` when the MCP exposes only projected text or when `main_topic` is empty but usable `page_as_markdown` or equivalent projected text exists.
8. Treat redirect, `broken`, 4xx/5xx, unfinished crawl, missing result, and missing primary content as failures or evidence shortfalls, not empty successful data.

Retry only a transient timeout, throttling, or `5xxxx` provider failure, and only after approval. Never retry validation, authorization, access, balance, malformed-input, or cost-limit failures unchanged.

## 4. Current metadata audit

From the Instant Pages HTML item, capture these values when present:

- Resolved item URL and redirect `location`.
- Page HTTP status and `resource_type`.
- `meta.title`, `meta.description`, `meta.meta_keywords`, and `meta.canonical`.
- `meta.social_media_tags`, including available Open Graph and Twitter fields.
- Provider `title_length` and `description_length` when present.

Use these fields only to describe current implementation. They are not positive evidence for topic, intent, geography, seed selection, or suggested claims. A brand explicitly established in primary content may be used as an exclusion token. Metadata/domain tokens may be used only as clearly disclosed negative noise filters, never to add a topic.

## 5. Primary-content evidence

Preferred mode: use Content Parsing `page_content.main_topic[]` as the positive evidence set:

- Headings: non-empty `main_title` and `h_title`.
- Text: non-empty `primary_content[].text`.
- Language: an explicit `language` value associated with qualifying main-topic content.

Exclude `page_content.header`, `page_content.footer`, `secondary_topic`, all `secondary_content`, navigation lists, contact-only blocks, repeated calls to action, cookie text, legal text, and other boilerplate. Do not treat `page_as_markdown` as primary evidence when structured `main_topic` data is available; it can mix boilerplate with content.

Fallback mode: when the MCP projects only plain text or when `main_topic` is empty but `page_as_markdown` or equivalent projected text is present, classify the evidence mode as `projection_degraded_text`. Use `scripts/metadata_support.py extract-content` to apply conservative fallback extraction to that text. Treat the fallback output as lower confidence, keep the limitation explicit in the report, and never use it to infer unsupported claims or precise service geography.

Record short excerpts or concise paraphrases sufficient to justify the topic, intent, geography, and each seed. Do not copy large passages into the report.

Use `scripts/metadata_support.py extract-instant` and `extract-content` with provider JSON on stdin to apply these paths deterministically. Keep raw responses transient and outside the repository.

## 6. Evidence gate and recovery

A successful keyword workflow requires enough primary content to justify five distinct, non-brand seeds. Seeds should normally contain two to four words; longer geography-qualified phrases are allowed. Each seed needs an evidence note and must represent the page's actual offering or intent.

`projection_degraded_text` is not an automatic stop condition, but it raises the evidence bar. Continue only when the fallback text still supports five distinct seeds without relying on metadata, URL terms, or weak paraphrases. Otherwise stop before keyword calls and explain that the MCP projection degraded the content evidence.

If the page is broken, primary content is empty, or five distinct seeds cannot be justified:

- Stop before Related Keywords calls.
- Return a diagnostic with the failed gate and completed-call costs.
- Ask before one JavaScript-rendered retry when dynamic rendering is plausible.
- Do not pad the list with URL terms, metadata, unsupported synonyms, or generic navigation phrases.

## 7. Geography, market, and language

Resolve country and language separately.

Country precedence:

1. Explicit user country override.
2. Country unambiguously defined by primary content as the market, service/delivery area, or target audience.
3. Country unambiguously resolved from a primary-content city or region.
4. `United States`, disclosed as the default.

Language precedence:

1. Explicit user language override.
2. Language explicitly returned for qualifying main-topic content.
3. Strong low-risk textual signal from `projection_degraded_text`, disclosed as inferred.
4. `en`, disclosed as the default.

A footer address alone does not establish a market. User overrides win, but report any conflict with the content-defined service geography. Use the content language for suggestions even when the keyword-market override differs; disclose that distinction. In `projection_degraded_text` mode, do not promote weak geographic hints such as contact blocks or legacy office references into market facts. Confirm uncertain location/language support through an exposed MCP resolver or ask the user.

## 8. Related Keywords extraction

For each item under `tasks[].result[].items[]`, extract:

- Keyword: `keyword_data.keyword`.
- Search volume: `keyword_data.keyword_info.search_volume`.
- Organic KD: `keyword_data.keyword_properties.keyword_difficulty`.
- Ads competition numeric value: `keyword_data.keyword_info.competition`.
- Ads competition level: `keyword_data.keyword_info.competition_level`.
- CPC: `keyword_data.keyword_info.cpc`.
- Source seed: the seed used for that MCP call.

Preserve nulls. Zero is a real value and must not become null. Keep organic KD separate from paid Ads competition.

## 9. Normalization, relevance, and ranking

Normalize keyword display text with Unicode NFKC, collapsed whitespace, and trimming. Deduplicate using Unicode casefolded normalized text. Merge all seed provenance in sorted order.

Use `scripts/metadata_support.py normalize-batch` with a transient `{"calls": [{"seed": "...", "response": {...}}]}` object on stdin. After semantic relevance exclusions, pass the remaining `rows` to `scripts/metadata_support.py rank`. Do not commit the input or raw response.

When duplicate rows disagree, keep the first non-null metric from the approved seed-call order and record every conflicting metric/value. Do not average incompatible observations.

Exclude exact seed rows, brands, navigation phrases, unrelated intents, unsupported services/products/geographies, and malformed keywords. Record counts and reasons for every exclusion category. Relevance decisions must cite primary-content evidence.

For every relevant row with non-null search volume and KD, calculate:

```text
opportunity_proxy = search_volume / (keyword_difficulty + 10)
```

This is a derived prioritization proxy, not a DataForSEO metric and not proof that a keyword is low competition. DataForSEO KD is country-specific and logarithmic. Rank by descending proxy, descending volume, ascending KD, then normalized keyword. Select at most 20 and disclose a shortfall. Report raw volume and KD beside the proxy.

## 10. Metadata packages

Generate three internally coherent packages. Mark one as recommended. Each package contains:

- Primary target keyword and short rationale.
- Page title: editorial target 50-60 Unicode code points.
- Meta description: target 140-160.
- Open Graph title: target 55-65.
- Open Graph description: target 140-180.
- Twitter title: target 55-65.
- Twitter description: target 125-160.

Count Unicode code points with `scripts/metadata_support.py count`. Length ranges are editorial targets, not search-engine or social-platform display guarantees. Keep every statement truthful to primary content. Do not claim prices, awards, availability, guarantees, locations, features, or outcomes absent from the evidence.

Add one clearly labeled legacy meta keywords list per package. State that Google and Bing do not use the tag for rankings. Do not describe meta-keywords options as an SEO recommendation.

## 11. Cost and coverage

Prefer `tasks[].cost` and sum each task once. Use the envelope cost only when no task-level cost exists; never add both. Sum unrounded decimal values, then round once to two decimals and format with a decimal comma as `Total cost: x,xx USD`.

Use `scripts/metadata_support.py cost` with either one provider response or `{"responses": [response1, response2]}` on stdin to calculate the total deterministically.

Name calls with missing cost and mark the subtotal incomplete. Coverage must include the evidence mode, calls planned/completed, rows requested, returned, exact-seed exclusions, unique rows, metric-complete rows, relevance exclusions by reason, conflicts, and selected rows.

## 12. Report path and timestamp

Use local date `YYYY-MM-DD` and an ISO-8601 timestamp with timezone. Save:

```text
<root>/<domain>/<YYYY-MM-DD>_Page-Metadata_<safe-URL>.md
```

The helper caps the full filename at 140 characters, keeps the extension, always adds a deterministic collision hash, and returns a redacted URL for the report. Do not place raw customer responses, credentials, authorization data, or sensitive query values in the report or repository.

## Official references

- [OnPage Instant Pages](https://docs.dataforseo.com/v3/on_page/instant_pages/)
- [OnPage Content Parsing Live](https://docs.dataforseo.com/v3/on_page-content_parsing-live/)
- [Google Related Keywords Live](https://docs.dataforseo.com/v3/dataforseo_labs-google-related_keywords-live/)
- [Keyword Difficulty calculation](https://dataforseo.com/help-center/what-is-keyword-difficulty-and-how-is-it-calculated)
- [Meta keywords guidance](https://dataforseo.com/help-center/meta-keywords)
