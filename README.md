# DataForSEO Skills

Agent skills for building DataForSEO API integrations and producing evidence-based SEO analyses and reports with explicit endpoint verification, credential safety, and cost controls.

This repository is intended to grow into a collection of skills that perform SEO analyses and generate corresponding SEO reports. Each analysis and reporting skill uses the DataForSEO MCP server and follows the official [DataForSEO API documentation](https://docs.dataforseo.com/v3/) and [DataForSEO White Papers and knowledge base](https://dataforseo.com/knowledgebase).

Use these skills when an agent must select a DataForSEO endpoint, implement or review an integration, troubleshoot provider responses, or turn current OnPage evidence into a technical SEO report. The repository ships `dataforseo-api` for integration work and `technical-seo-page-audit` for single-URL audits and prioritized Markdown reports.

Install through the Netresearch marketplace with `/plugin marketplace add netresearch/claude-code-marketplace`, or use one of the direct installation methods below.

## What this skill solves

- Selects and verifies DataForSEO API workflows against current official documentation.
- Handles live and task-based request lifecycles, provider errors, retries, and normalization.
- Keeps credentials out of source control and makes billable activity explicit.
- Audits one page for availability, indexability, redirects, links, metadata, schema signals, and performance.
- Produces a provider-derived Technical Score and a dated Markdown report with P0-P3 fixes.

## Use when

- Implementing a DataForSEO client, connector, job, or data pipeline.
- Reviewing endpoint choice, task polling, pagination, rate limiting, or error handling.
- Diagnosing unexpected DataForSEO responses, empty results, or failed tasks.
- Auditing a specific URL for technical SEO defects and implementation priorities.
- Generating a detailed technical SEO page report with the DataForSEO MCP server.

## Expected outputs

- A documented endpoint and request strategy with assumptions and request volume.
- Integration code and sanitized tests when file changes are requested.
- A troubleshooting report or operational runbook for existing integrations.
- A dated technical SEO Markdown report with a 0-100 Technical Score and evidence-backed fixes.

## Context requirements

- The desired dataset, targets, locations, languages, freshness, and output format.
- The host language, framework, and existing integration code when applicable.
- DataForSEO credentials only for explicitly authorized live requests, supplied via environment variables.
- For page audits, an absolute HTTP(S) page URL and filesystem write access.

## Example prompts

```text
Implement a Python client for our DataForSEO task-based workflow with bounded polling and normalized errors.
Review this DataForSEO integration for accidental billable retries, leaked credentials, and incomplete task-state handling.
Diagnose why these successful HTTP responses contain no usable results and propose tests with sanitized fixtures.
Audit https://example.com/products/widget for technical SEO and save the detailed Markdown report in the default location.
Check this page for indexability, broken-link signals, redirects, missing metadata, schema gaps, and performance problems.
```

## Related skills

- `dataforseo-api`: integration design, implementation, review, and troubleshooting.
- `technical-seo-page-audit`: single-page technical SEO analysis and Markdown reporting.

## Installation

### Prerequisites

Before using the SEO analysis and reporting skills:

- Install and configure the DataForSEO MCP server in your Agent Skills-compatible client.
- Set up an appropriate [DataForSEO account](https://app.dataforseo.com/register) with access to the APIs required by the selected skill.
- Provide credentials through the MCP server's secure configuration. Do not store credentials in this repository.

### Marketplace (recommended)

```bash
/plugin marketplace add netresearch/claude-code-marketplace
```

Then browse the marketplace and install `dataforseo-api` or `technical-seo-page-audit`.

### Agent Skills-compatible clients

```bash
npx skills add https://github.com/netresearch/dataforseo-skills --skill dataforseo-api
npx skills add https://github.com/netresearch/dataforseo-skills --skill technical-seo-page-audit
```

### Composer

```bash
composer require netresearch/dataforseo-skills
```

### Git clone

```bash
git clone https://github.com/netresearch/dataforseo-skills.git
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Changes to discovery fields must also update the corresponding Netresearch marketplace entry, or document why an override is intentional.

## License

Code, scripts, workflows, and configuration are licensed under [MIT](LICENSE-MIT). Skill definitions and documentation are licensed under [CC BY-SA 4.0](LICENSE-CC-BY-SA-4.0).

## Classification

| Field | Value |
| --- | --- |
| Action level | `runs_commands` |
| Risk level | `medium` |

## Repository extras

- `agents/openai.yaml` provides OpenAI-facing discovery metadata.
- Both skills keep their runtime instructions in `SKILL.md`; the page-audit skill also includes non-live evaluation cases.
- GitHub Pages should remain disabled because the README and marketplace entry are sufficient.
- Proposed GitHub description: `Agent skills for DataForSEO API integrations and evidence-based technical SEO audits and reports.`
- Proposed GitHub topics: `agent-skill`, `dataforseo`, `seo`, `api-integration`, `data-pipeline`.

Developed and maintained by [Netresearch DTT GmbH](https://www.netresearch.de/).
