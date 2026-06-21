# DataForSEO MCP SEO Analysis

`dataforseo-skill` is the general-purpose companion for selecting, calling, sequencing, and troubleshooting the official DataForSEO MCP tools in SEO work. It complements the repository's opinionated reporting skills with a catalog-driven workflow for analyses that do not yet have a dedicated skill.

## What the skill does

- Inventories the 83 DataForSEO MCP tools exposed in the captured 2026-06-21 session.
- Preserves each exact callable name and live tool declaration, including required and optional parameters, types, accepted values, defaults, limits, and validation notes.
- Maps tools to the underlying official DataForSEO REST method and path while keeping MCP and REST contracts separate.
- Guides cost-aware tool selection, response validation, pagination, batching, retries, and evidence-backed SEO conclusions.
- Documents authentication, raw MCP syntax, REST envelopes, error handling, rate limits, callbacks, encoding, clients, and troubleshooting.
- Provides exact call sequences for keyword difficulty, live SERP, backlink, local search, ranking history, competitor-gap, and single-page audit workflows.

## Requirements

- The official DataForSEO MCP server with relevant modules enabled.
- DataForSEO credentials configured securely in the MCP host or an authorized remote connector.
- A clear SEO objective plus the target domain, URL, keywords, or entity required by the selected tool.
- Market/language/device/date inputs when those affect the result.

The skill always uses MCP for SEO analysis. Raw HTTP examples exist for integration and troubleshooting, not as a substitute for the configured MCP.

## Examples

```text
Use DataForSEO MCP to compare the organic keyword footprint of example.com and competitor.com in the United States, and explain every call before you make it.
```

```text
Get a live mobile Google SERP snapshot for three keywords in Austin and summarize organic and local-pack visibility.
```

```text
Extract a one-link-per-domain backlink sample for example.com, report coverage, and identify the strongest referring domains.
```

```text
Explain why my DataForSEO MCP call returns 40209 and give me a safe concurrency and retry plan.
```

## References

- `references/mcp-tools.json`: searchable 83-tool catalog and REST mappings.
- `references/seo-workflows.md`: common SEO call sequences and normalized parsed outputs.
- `references/protocol-and-rest.md`: authentication, protocol, response, rate-limit, batching, callback, SDK, and troubleshooting details.
- `scripts/lookup_tool.py`: print one tool contract.
- `scripts/extract_postman_example.py`: extract a dated exact request/response example from the supplied 30 MB Postman collection.

The tool catalog records the official MCP source revision used for REST mapping. Always prefer `tools/list`, the active input schema, and current official DataForSEO documentation when the deployment differs.
