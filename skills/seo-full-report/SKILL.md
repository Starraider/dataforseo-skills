---
name: seo-full-report
description: "Use when consolidating dated SEO reports for one domain into a concise full SEO report, prioritizing critical next actions, or surfacing cross-analysis ranking opportunities from files under SEO/<domain>/ with a current DataForSEO MCP validation snapshot."
compatibility: "Requires the official DataForSEO MCP server with the DATAFORSEO_LABS module enabled, Python 3, and filesystem read/write access."
---

# SEO Full Report

Combine the selected local reports into one decision-oriented report. Use DataForSEO MCP only for the bounded current snapshot; preserve the selected files as the evidence for their stated dates.

Read [references/report-contract.md](references/report-contract.md) before analysis and follow [templates/report-template.md](templates/report-template.md) for output.

## Inputs

Require a domain and either one ISO date (`YYYY-MM-DD`) or an inclusive ISO date range. Ask for every missing or ambiguous value together and wait. Accept an optional report root; default to `SEO/`.

Normalize the domain to a lowercase hostname without `www.`, credentials, port, path, query, fragment, or trailing dot. Do not invent dates.

## Workflow

1. Resolve `scripts/select_reports.py` relative to this skill, but run it with the user's working directory unchanged so `SEO/` resolves correctly. Pass the domain, date selection, and report root. It selects regular files whose names begin with an in-range ISO date and excludes earlier Full SEO Reports to prevent recursive synthesis.
2. If the directory is absent or no file matches, report the checked path and selection, then stop without a DataForSEO call or output report.
3. Read every selected file. Record unreadable files explicitly. Build a source inventory and evidence ledger before drawing conclusions.
4. Deduplicate overlapping findings and metrics. Compare values only when market, device, scope, metric definition, and coverage align. Preserve contradictions and limitations instead of averaging them away.
5. Run the two-call DataForSEO MCP validation workflow in the contract. Keep its current snapshot separate from the date-scoped source evidence. Do not retry or add paid calls without approval.
6. Rank recommendations by severity, likely organic impact, evidence strength, effort, and dependency. Lead with no more than five immediate actions and highlight unusually attractive ranking opportunities.
7. Write the report using the template. Every recommendation needs an owner, concrete implementation steps, success measure, timing, and source references.
8. Save under `<root>/<domain>/` with the filename defined in the contract. Return the absolute path and the three most urgent actions.

## Guardrails

- Do not claim a causal relationship, complete keyword coverage, or guaranteed ranking gain.
- Do not sum ETV, search volume, keyword counts, scores, or costs across overlapping reports.
- Label all synthesis judgments as analyst prioritization and all current MCP values with their capture timestamp.
- Validate provider status, preserve nulls, log returned coverage and cost, and distinguish zero from missing.
