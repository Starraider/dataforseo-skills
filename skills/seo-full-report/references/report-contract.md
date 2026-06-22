# SEO full report contract

## Official sources

- [DataForSEO Labs Google Domain Rank Overview](https://docs.dataforseo.com/v3/dataforseo_labs/google/domain_rank_overview/live/)
- [DataForSEO Labs Google Ranked Keywords](https://docs.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live/)
- [DataForSEO knowledge base](https://dataforseo.com/knowledgebase)

Treat the active MCP schemas as authoritative when they differ from examples or documentation snapshots.

## File selection

Require `domain` plus either `date` or both `start_date` and `end_date`, all in ISO `YYYY-MM-DD`. The range is inclusive. Default `report_root` to `SEO/` relative to the working directory.

Run one of:

```text
python3 <skill-directory>/scripts/select_reports.py DOMAIN --date YYYY-MM-DD --root SEO
python3 <skill-directory>/scripts/select_reports.py DOMAIN --start-date YYYY-MM-DD --end-date YYYY-MM-DD --root SEO
```

Keep the user's working directory unchanged; relative report roots resolve from there, not from the skill directory.

Use the script's JSON manifest as the authoritative selection. It selects regular files directly inside `<root>/<domain>/` whose basenames start with an in-range valid ISO date. Earlier files containing `_Full-SEO-Report_` are excluded unless the user explicitly requests their inclusion; this prevents double counting and recursive summaries. Read every selected file with an appropriate available reader. List unsupported or unreadable files in the inventory and lower confidence rather than silently omitting them.

If the directory is missing, the dates are invalid, or the selection is empty, stop before billable calls and do not create a report.

## Evidence ledger

Assign every source an ID (`S1`, `S2`, ...). For each source record filename, report date/type, analyzed URL or domain, market, language, device, capture time, sample limits, scores, costs, and major limitations. Extract findings into a ledger with:

- source ID and exact section or table;
- affected keyword, page, template, or site area;
- provider metric versus source-derived score or judgment;
- severity or opportunity, stated action, and evidence limits.

Normalize exact domains, URLs, and case-insensitive keywords for matching, but preserve original labels in citations. Merge duplicated findings only when they concern the same entity and scope. For aligned observations, prefer the newest as current within the selected period and retain the older value as change evidence. Keep different markets, languages, devices, pages, and sampling depths separate. Never average conflicting scores or treat capped result sets as total coverage.

## Current DataForSEO validation

After the source ledger exists, infer `location_name` and `language_code` only when the selected reports establish one clear primary market. Otherwise omit these optional fields and state that the snapshot spans the provider's available markets. Do not ask for extra market input solely for this bounded validation.

Make exactly these calls unless one fails:

1. `dataforseo_labs_google_domain_rank_overview` with `target`, `ignore_synonyms: true`, and the established market fields when available. Retain organic ETV, keyword count, position buckets, new/up/down/lost counts, update context, returned scope, and cost.
2. `dataforseo_labs_google_ranked_keywords` with the same scope, `target`, `item_types: ["organic"]`, `limit: 100`, positions 4-20, positive search volume, and search volume descending. Retain keyword, ranking URL, `rank_group`, ETV, search volume, difficulty, intent, returned/total counts, update context, and cost.

The second call's filter is:

```json
[
  ["ranked_serp_element.serp_item.rank_group", ">=", 4],
  "and",
  ["ranked_serp_element.serp_item.rank_group", "<=", 20],
  "and",
  ["keyword_data.keyword_info.search_volume", ">", 0]
]
```

Use `order_by: ["keyword_data.keyword_info.search_volume,desc"]`. Validate transport and provider/task status before analysis. If the first call fails, log it and stop further paid calls; still finish the source-based report with a prominent live-validation limitation. Never retry without approval.

Present this evidence as a **current validation snapshot**, timestamped separately from the selected source period. It may confirm, contradict, or add context, but it must not rewrite historical observations.

## Prioritization

Create one deduplicated backlog. Assign priority through explicit analyst judgment:

- **P0:** indexing, crawlability, availability, security, or deindexation blockers.
- **P1:** high-confidence work likely to protect or improve meaningful visibility in 0-30 days, including positions 4-20, severe decay, cannibalization, and high-value technical defects.
- **P2:** useful 31-60 day content, internal-link, metadata, schema, or page-format work.
- **P3:** longer-term experiments, monitoring, and low-confidence ideas.

Within each tier, order by likely organic/business impact, evidence strength, effort, and dependencies. Mark this ordering **Analyst prioritization — not a DataForSEO metric**. Do not invent numeric impact. A ranking opportunity is especially interesting when multiple selected reports corroborate it, the live snapshot shows rank 4-20 with meaningful demand, or the work improves one page across several keywords. Name evidence gaps and external dependencies.

Every top action must include: affected URL/template, why now, owner role, ordered implementation steps, effort (`S`, `M`, or `L` with a plain-language definition), dependency, completion check, KPI, and source IDs.

## Output and filename

Follow the report template and keep the executive layer concise. Detailed evidence belongs after the action plan.

- Single date: `<today>_Full-SEO-Report_<domain>_<date>.md`
- Date range: `<today>_Full-SEO-Report_<domain>_<start>_to_<end>.md`

Use the local ISO date for `<today>`. Save under `<root>/<domain>/`, begin the file with that same date, and return its absolute path.

For each MCP call log endpoint, scope-defining arguments, status, returned coverage, cost, and timestamp. Sum unrounded returned costs and format the result to two decimal places. If any cost is absent, state that the subtotal is incomplete and identify the call.
