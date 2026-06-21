# SERP optimization data contract

Read this contract before making DataForSEO MCP calls or scoring opportunities.

## Input and normalization

- Require a hostname or HTTP(S) URL. Reject credentials, non-HTTP schemes, ports, malformed labels, and IP literals. Normalize the project domain to lowercase, remove a leading `www.`, path, query, fragment, and trailing dot.
- Accept country, language code, device (`desktop` or `mobile`), exact Google location, and report root. Defaults are United States, `en`, desktop, and `<cwd>/SEO`.
- An exact location is optional but materially affects local results. If local-pack analysis matters and only a country was supplied, disclose that country-level results may not represent a city SERP.
- Resolve relative report roots against the current working directory. Never put query strings, fragments, credentials, or path traversal in report paths.

## Official endpoint references

- [DataForSEO Labs Ranked Keywords](https://docs.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live/)
- [Google Organic Advanced Live SERP](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/)
- [OnPage Content Parsing Live](https://docs.dataforseo.com/v3/on_page/content_parsing/live/)

Treat the active MCP schema as authoritative. Never bypass MCP, send credentials in arguments, or request parameters the active tool does not expose.

## Discovery request and fields

Use one `dataforseo_labs_google_ranked_keywords` request with:

- normalized domain target;
- selected country and language;
- `item_types: ["organic"]`;
- `limit: 200`;
- a filter for `ranked_serp_element.serp_item.rank_group <= 20`;
- descending `keyword_data.keyword_info.search_volume` order.

Retain:

- `keyword_data.keyword`, `keyword_info.search_volume`, `keyword_properties.keyword_difficulty`, and `search_intent_info.main_intent`;
- `keyword_data.serp_info.serp_item_types`, result timestamps, and check URL when exposed;
- `ranked_serp_element.serp_item` URL, domain, `rank_group`, and `rank_absolute`.

The feature inventory identifies features observed in the stored SERP; it does not identify every owner. The live call confirms presence, prominence, owners, and formats. Do not treat a Labs snapshot as live.

Candidate feature types include `featured_snippet`, `answer_box`, `people_also_ask`, `video`, `short_videos`, `images`, `image`, `local_pack`, `local_services`, `map`, `shopping`, `popular_products`, `product_considerations`, `refine_products`, `recipes`, `top_stories`, `discussions_and_forums`, `courses`, and other non-organic types exposed by the response. Keep unfamiliar types and describe them; do not silently remap them.

## Shortlist and live calls

Build a candidate list of at most ten keywords. Favor positions 1-20, non-null demand, clear intent-feature fit, and prominent or commercially meaningful features. This is a proposal, not the final priority order.

Before fan-out, state:

- proposed keywords and feature types;
- one live SERP call per keyword;
- anticipated Content Parsing calls after deduplication;
- that extra PAA click depth, retries, pagination, and JavaScript can change cost.

Wait for approval unless the user's prompt already names or explicitly approves a bounded shortlist.

Use `serp_organic_live_advanced` with exact keyword, `search_engine: "google"`, selected language/location/device, `depth: 100`, and `max_crawl_pages: 1`. Set `people_also_ask_click_depth: 1` only when PAA is in scope. Do not infer an absent feature from an empty or failed task.

For every returned feature retain type, `rank_group`, `rank_absolute`, page, position, title, domain, URL, nested item domains/URLs, and the provider timestamp where exposed. Distinguish:

- a direct owner URL;
- multiple nested owners;
- a Google-controlled or entity feature with no attributable page;
- an owner not exposed by the response.

The target's position means its live organic `rank_group` and `rank_absolute`. If absent within returned depth, report `not found within depth 100`; never convert absence to position 101.

## Parsing and comparison

Parse each distinct target URL and up to two distinct representative winning URLs per keyword. Prefer direct feature owners, then the closest format exemplar. Deduplicate URLs across keywords. Keep redirect/final-URL evidence when exposed.

Compare only qualifying `page_content.main_topic` headings, text, lists, tables, images, and video-related evidence. Exclude navigation, footer, cookie, and unrelated boilerplate. If the MCP projects unstructured content, disclose degraded evidence and avoid exact structural claims not supported by the projection.

Infer and label page formats such as guide, definition, listicle, comparison, table/reference, product, category, local landing page, tool, recipe, news article, forum, or video page. Do not present these labels as provider fields.

## Attainability classifications

Assign exactly one:

- **Owned:** the target currently owns the analyzed feature.
- **High:** target ranks 1-5, intent and page type fit, the winner's format is reproducible, and no major external dependency blocks eligibility.
- **Medium:** target ranks 6-10 or has one material format/coverage gap that can be corrected on-page.
- **Low:** target ranks 11-20, the page type or intent conflicts, multiple material gaps exist, or results are dominated by formats the target cannot credibly reproduce.
- **External dependency:** eligibility primarily depends on a Business Profile, merchant/product feed, inventory, reviews, platform participation, or another system outside the page.
- **Stale/absent:** the discovery snapshot listed the feature but the successful live SERP did not. Do not score it as a current opportunity.

Explain overrides. These are analyst classifications, not DataForSEO metrics or ranking guarantees.

## Priority score

Score current, non-owned features only when all four inputs are available:

```text
proximity = 100 * (21 - target_rank_group) / 20
volume = 100 * ln(1 + search_volume) / ln(1 + max_shortlist_volume)
intent_fit = 100 for strong fit, 60 for partial fit, 20 for mismatch
prominence = 100 * (21 - min(feature_rank_absolute, 21)) / 20
priority = round(0.35*proximity + 0.30*volume + 0.20*intent_fit + 0.15*prominence)
```

Use the maximum non-null search volume among successfully analyzed shortlist rows. When it is zero, set every complete row's volume component to zero. Explain intent-fit judgments. If volume, rank, or feature position is missing, report priority as unavailable; do not impute it. Group scores as P1 (75-100), P2 (50-74), P3 (25-49), or P4 (0-24).

## Recommendation rules

Every recommendation must identify its live evidence and specify:

- exact target URL and insertion/replacement point;
- a proposed H2/H3 and answer-block purpose;
- paragraph, ordered/unordered list, or table structure based on current winners;
- table columns or list-step labels where applicable;
- original image, alt/caption, thumbnail, embed, transcript, or video placement requirements when relevant;
- supporting PAA questions that were actually returned;
- structured data only when the page's visible content and entity type are eligible;
- external requirements for local and commerce features.

Do not recommend FAQ markup merely because PAA exists. Do not invent review ratings, prices, availability, local addresses, authorship, dates, or schema properties. State that structured data establishes eligibility at most and does not guarantee display.

## Validation, cost, and failures

For every MCP response validate transport content, top-level status, task status, and non-null result before parsing. Preserve null versus zero and record returned counts, timestamps, and sampling limits.

Log tool, scope-defining arguments, status, item count, returned cost, and limitations. Sum unrounded returned costs and format `Total cost: x,xx USD`. When any cost is missing, label the subtotal incomplete and name the calls.

Ask before every retry, additional keyword, extra winner page, pagination request, PAA depth increase, or JavaScript-rendered parsing call. On partial failure, complete only defensible rows and report coverage; do not fabricate a complete matrix.
