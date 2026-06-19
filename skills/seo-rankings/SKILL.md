---
name: seo-rankings
description: "Use when checking a domain's live Google organic positions for a supplied keyword list, combining rankings with search volume, grouping keywords by ranking tier, prioritizing one action per keyword, or producing a detailed rankings Markdown report."
license: "(MIT AND CC-BY-SA-4.0). See LICENSE-MIT and LICENSE-CC-BY-SA-4.0"
compatibility: "Requires the official DataForSEO MCP server with the SERP and KEYWORDS_DATA modules enabled and filesystem write access."
---

# Live Google Organic Rankings

Follow the official [Live Advanced SERP](https://docs.dataforseo.com/v3/serp-se-type-live-advanced/) and [Google Ads Search Volume](https://docs.dataforseo.com/v3/keywords_data-google_ads-search_volume-live/) documentation.

## Input

1. Require a domain and non-empty keyword list. Ask for all missing required inputs and wait.
2. Default to location `United States`, language `en`, device `desktop`, and depth `100`. Accept `desktop` or `mobile` and depth 10–100; disclose scope.
3. Normalize the domain to a lowercase hostname without credentials, port, path, trailing dot, or leading `www.`. Reject malformed input. Trim and case-insensitively deduplicate keywords. Reject entries over 80 characters or 10 words.

## DataForSEO MCP workflow

The request authorizes one live rank call per unique keyword and one bulk volume call. Ask before retries or extras.

1. For every keyword, call `serp_organic_live_advanced` with `search_engine: "google"`, scope, and `depth`. Omit optional paid features.
2. Inspect only `type: "organic"`. Match normalized hostnames equal to the target or ending in `.` plus target. Select the lowest `rank_group` and its URL. Do not use `rank_absolute`, which includes unlike SERP elements.
3. Call `kw_data_google_ads_search_volume` once with all keywords and the same location/language. Merge `search_volume` case-insensitively. Ask to split lists over its 700-keyword limit.
4. Validate statuses. Never invent metrics; use `—` when missing. “Not ranking” means not found within depth, not proven absence from Google.

## Classification and actions

Assign exactly one tier and next action:

| Tier | Position | Action |
|---|---:|---|
| 🟢 **Winning** | 1–3 | Defend — monitor weekly |
| 🟡 **Page 1** | 4–10 | Push to top 3 — internal links + on-page polish |
| 🟠 **Close** | 11–30 | Re-optimize + build links |
| 🔴 **Long-haul** | 31–100 | Pivot or invest heavily |
| ⚫ **Not ranking** | none within depth | Decide: pursue or drop |

Order groups as above and rows by position, then descending volume. For the final highest-leverage action, choose the highest-volume keyword from the first populated tier in this order: Close, Page 1, Long-haul, Not ranking, Winning. Break ties by better position, then input order. State its keyword, position/tier, volume, URL, and action.

## Report

Use the requested report root or `<current-working-directory>/SEO`; create its domain child. Write `<report-root>/<domain>/<YYYY-MM-DD>_Rankings_<domain>.md`; default: `SEO/<domain>/<filename>`. Use local ISO date (example: `2026-06-19_Rankings_example.com.md`) as the first line.

Include scope/timestamp; summary; grouped `Keyword | Pos | Volume | URL | Action` table; tier counts; highest-leverage action; methodology; MCP calls/cost scope; coverage/limitations; and official links. Use thousands separators and target-relative URL paths. Return the absolute path and summary.
