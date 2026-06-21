---
name: dataforseo-skill
description: "Use when performing SEO analysis with the DataForSEO MCP, selecting or sequencing DataForSEO tools, interpreting their responses, estimating request scope, troubleshooting calls, or explaining the MCP and underlying API contracts."
compatibility: "Requires the official DataForSEO MCP server with the relevant modules enabled; filesystem access is optional unless the requested analysis must be saved."
---

# DataForSEO MCP SEO Analysis

Use the configured DataForSEO MCP as the evidence source for keyword, SERP, ranking, competitor, backlink, on-page, local, domain, content, merchant, or AI-visibility analysis.

## Workflow

1. Identify the decision the analysis must support, target domain/page/keywords, country or exact location, language, device, date range, and output format. Ask only for missing inputs that materially change billable calls.
2. Inspect the active DataForSEO tool list because enabled modules and names can differ by deployment. Search `references/mcp-tools.json` for the candidate tool. Treat the active input schema as authoritative when it differs from the snapshot.
3. Use the smallest sequence that answers the question. Read `references/seo-workflows.md` for proven call sequences. Resolve supported locations, languages, filters, models, or categories with the corresponding utility tool before guessing.
4. State the planned billable calls and limits when scope is large or ambiguous. Start with conservative `limit`/`depth` values. Do not paginate, fan out, or retry billable calls merely to make a report look complete.
5. Call the MCP tool with an arguments object matching its schema exactly. Never send credentials in tool arguments or bypass MCP for an SEO analysis.
6. Validate transport success and provider status. Parse JSON from `CallToolResult.content[].text`; treat text beginning with `Error:` as failure. Preserve nulls, distinguish zero from missing, record timestamps and returned coverage, and never invent unavailable metrics.
7. Analyze only comparable scopes. Normalize domains and keywords explicitly, retain source provenance, explain formulas, and separate provider metrics from derived scores.
8. Report every tool called, arguments that define scope, returned cost when exposed, limitations, excluded rows, and actionable conclusions. Sum unrounded returned costs before formatting.

## Safety and recovery

- Authentication, raw HTTP, response envelopes, errors, rate limits, pagination, batching, callbacks, encoding, SDKs, and retry rules are in `references/protocol-and-rest.md`.
- Retry only transient `5xxxx`, timeout, or throttling failures; use exponential backoff with jitter and cap attempts. Ask before a retry that can incur another charge.
- Do not retry validation, authorization, balance, access, malformed-input, or cost-limit failures unchanged.
- Do not claim that MCP exposes standard-task, upload, webhook, or export features when the live tool schema does not expose them.

## Reference routing

- Run `python3 scripts/lookup_tool.py <tool-name>` to inspect one of the 83 captured tool contracts without loading the full catalog.
- Read `references/seo-workflows.md` for common analyses and parsed-output examples.
- Read `references/protocol-and-rest.md` only for integration or troubleshooting work.
- If `dataforseo_xmpl_v3_postman.json` is available, use `scripts/extract_postman_example.py` to inspect its request and response example for a mapped REST URL. Treat it as a dated example, not the current schema authority.
