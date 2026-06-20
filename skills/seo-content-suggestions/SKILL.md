---
name: seo-content-suggestions
description: "Use when analyzing topical authority, clustering a domain's ranked keywords, finding strong, building, weak, and missing topics against organic competitors, calculating a 0-100 Content Score, or recommending five articles with DataForSEO MCP evidence."
license: "(MIT AND CC-BY-SA-4.0). See LICENSE-MIT and LICENSE-CC-BY-SA-4.0"
compatibility: "Requires the official DataForSEO MCP server with the DATAFORSEO_LABS module enabled and filesystem write access."
---

# SEO Content Suggestions

Use [Ranked Keywords](https://docs.dataforseo.com/v3/dataforseo_labs-google-ranked_keywords-live/), [Competitors Domain](https://docs.dataforseo.com/v3/dataforseo_labs-google-competitors_domain-live/), and [Domain Intersection](https://docs.dataforseo.com/v3/dataforseo_labs-google-domain_intersection-live/).

## Input and scope

Require a target domain; if absent, ask and wait. Normalize a hostname or HTTP(S) URL to lowercase without credentials, port, suffix, trailing dot, or leading `www.`; reject malformed input. Accept up to five competitors. Default to `United States`/`en`; disclose assumptions. Use Google organic and `ignore_synonyms: true`. Ask before retries, pagination, or extra calls.

## DataForSEO MCP workflow

1. Call `dataforseo_labs_google_ranked_keywords` for the target with `limit: 200`, organic items, descending volume. Retain keyword, `rank_group`, URL, ETV, volume, difficulty, and intent.
2. If competitors are absent, call `dataforseo_labs_google_competitors_domain`. Exclude the target and top domains; retain five by intersections, then organic ETV.
3. Implement `content_gap --you <domain> --competitors <c1> ...` pairwise: per competitor call `dataforseo_labs_google_domain_intersection` with `target1: competitor`, `target2: target`, `intersections: false`, organic items, and `limit: 200`. Deduplicate keywords but retain ranking competitors.
4. Call ranked keywords with `limit: 200` for the first supplied or top discovered competitor. Its median non-null `rank_info.main_domain_rank` is the benchmark.
5. Validate statuses; never invent metrics. Report counts and sampling limits.

## Clusters and status

Normalize case and punctuation, singularize, then group by stems, head terms, and meaning. Merge thin synonyms; split different intent or audience. Aim for 8-15 clusters.

Classify the union of target and gap clusters in order:

- **Missing:** competitors rank; target does not.
- **Strong:** at least five target keywords rank 1-10 and summed ETV exceeds 100/month.
- **Building:** a target keyword ranks 1-30 but the cluster is not Strong. Flag top-10 clusters that missed a Strong threshold.
- **Weak:** every target position exceeds 30.

Report keyword count, best/average position, top-10 count, ETV, volume, URLs, competitor coverage, and status per cluster.

## Content Score

`total_clusters` includes all clusters. From the top `ceil(n/4)` target keywords by volume calculate:

`avg_position_top_quartile_score = clamp((100 - mean_rank_group) / 99, 0, 1)`

`content_score = round(50 * strong_clusters/total_clusters + 25 * (1 - missing_clusters/total_clusters) + 25 * avg_position_top_quartile_score)`

If clusters or positions are absent, report unavailable instead of dividing by zero.

## Five content moves

Select articles from Missing and Building clusters. Prioritize commercial or transactional keywords with volume above 200 and difficulty below the benchmark; break ties by volume, lower difficulty, then related-term breadth. If fewer than five qualify, use nearest candidates and label relaxed conditions.

Provide title, target keyword, related keywords, intent, volume, difficulty, benchmark, status, rationale, and an editorial word-count estimate.

## Report

Write Markdown with scope, summary, score inputs, competitors, cluster matrix, briefs, gaps, limitations, content moves and call log. Start with the local ISO date.

Use the requested root or `SEO/`; create `<root>/<domain>/`. Save as `<YYYY-MM-DD>_Content-Suggestions_<domain>.md`, for example `2026-06-19_Content-Suggestions_example.com.md`.
