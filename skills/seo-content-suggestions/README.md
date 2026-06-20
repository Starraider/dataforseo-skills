# SEO Content Suggestions

`seo-content-suggestions` measures a domain's topical search coverage, compares it with organic competitors, calculates a 0–100 Content Score, and recommends the five content pieces most likely to close meaningful gaps.

## What the skill does

The skill:

1. Retrieves up to 200 organic keywords for which the target domain ranks, ordered by search volume.
2. Uses up to five supplied competitors or discovers five organic competitors based on keyword intersections and estimated organic traffic.
3. Retrieves up to 200 competitor-only keywords per competitor and deduplicates them while preserving competitor coverage.
4. Clusters target and gap keywords by normalized stems, head terms, meaning, intent, and audience, aiming for 8–15 useful topic groups.
5. Classifies each cluster in this order:
   - **Missing:** competitors rank but the target does not.
   - **Strong:** at least five target keywords rank in positions 1–10 and their summed ETV exceeds 100 per month.
   - **Building:** at least one target keyword ranks in positions 1–30, without meeting the Strong threshold.
   - **Weak:** all target positions are worse than 30.
6. Calculates a reproducible Content Score from the share of Strong clusters, the absence of Missing clusters, and average position among the highest-volume quartile of target keywords.
7. Selects five content moves from Missing and Building clusters, prioritizing commercial or transactional keywords with volume above 200 and difficulty below the top competitor's domain-rank benchmark. Relaxed conditions are labeled when fewer than five candidates qualify.

## Why this analysis matters

Search engines are more likely to understand and trust a website when it answers a subject thoroughly and usefully, not just in one isolated article. This analysis shows which parts of a topic the site already covers well, which parts are beginning to perform, and which questions competitors answer while the site remains absent. It turns a large keyword list into understandable themes, so even non-specialists can see where the content is strong or incomplete.

The recommendations help decide what to publish next and which existing topic areas deserve more support. Filling a genuine gap can make the site relevant to more searches, while strengthening a developing topic can help related pages compete more effectively. Over time, a connected set of useful pages can improve visibility and rankings for a broader range of searches. The result still depends on content quality, site authority, competition, and implementation, so the suggestions are priorities rather than ranking guarantees.

## Requirements and inputs

- The official DataForSEO MCP server with the DataForSEO Labs module enabled.
- Filesystem write access.
- A target domain or HTTP(S) URL.

Optional inputs include up to five competitor domains, country, language, and report root. Defaults are automatic competitor discovery, United States, `en`, and `SEO/` below the current working directory. Retries, pagination, and additional calls require approval.

## Invocation examples

Directly by skill name:

```text
Use the seo-content-suggestions skill to analyze example.com and recommend its next five articles.
```

With named competitors:

```text
Analyze the content gaps of example.com against competitor-one.com, competitor-two.com, and competitor-three.com.
```

With a market override:

```text
Assess example.co.uk topical authority in the United Kingdom using English search data and propose five high-leverage content briefs.
```

With a custom report location:

```text
Run seo-content-suggestions for https://www.example.com, identify missing and building topics, and save the report under ./strategy/content.
```

If the target domain is absent or malformed, the skill asks for a valid domain before making billable requests.

## What to expect in the report

The report starts with the local ISO date and is saved by default as:

```text
SEO/<domain>/<YYYY-MM-DD>_Content-Suggestions_<domain>.md
```

It contains:

- Scope, market assumptions, timestamp, and total DataForSEO cost.
- An executive summary and Content Score with its component inputs.
- The selected organic competitors and the evidence used to select them.
- A topic-cluster matrix with status, keyword count, best and average position, top-10 count, ETV, volume, ranking URLs, and competitor coverage where available.
- Detailed gap analysis and five prioritized content moves.
- For each proposed article: title, primary and related keywords, intent, volume, difficulty, benchmark, cluster status, rationale, and estimated word count.
- Methodology, endpoint call log, coverage, limitations, and sampling notes.

Keyword and competitor calls are deliberately capped, so the report describes sampled coverage rather than claiming a complete market inventory. If clustering or position data is insufficient, the Content Score is reported as unavailable. After writing the report, the skill returns its absolute path and a concise summary.
