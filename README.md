# DataForSEO Skills

This repository is intended to grow into a collection of skills that perform SEO analyses and generate corresponding SEO reports. Each analysis and reporting skill uses the DataForSEO MCP server and follows the official [DataForSEO API documentation](https://docs.dataforseo.com/v3/) and [DataForSEO White Papers and knowledge base](https://dataforseo.com/knowledgebase).

## Available skills

### `dataforseo-api`

Plans, implements, reviews, and troubleshoots DataForSEO API integrations. It covers endpoint selection, live and task-based request lifecycles, response validation, retries, rate limits, cost controls, and credential safety.

Example prompt:

```text
Review this DataForSEO integration for accidental billable retries, leaked credentials, and incomplete task-state handling.
```

### `technical-seo-page-audit`

Audits one specific page through the official DataForSEO MCP OnPage tools. It checks availability, indexability, redirects, broken-link and resource signals, metadata, headings, canonicalization, structured-data gaps, page speed, Core Web Vitals, and related technical SEO issues. It returns the DataForSEO-derived Technical Score from 0 to 100, prioritizes fixes from P0 to P3, and writes a detailed dated Markdown report to the requested directory or `/SEO/` by default.

If the prompt does not contain a URL, the skill asks for one before making billable DataForSEO requests.

Example prompt:

```text
Audit https://example.com/products/widget for technical SEO, prioritize the fixes, and save the detailed Markdown report in the default location.
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

Then browse the marketplace and install `dataforseo-api` or `technical-seo-page-audit`.

### Agent Skills-compatible clients

```bash
npx skills add https://github.com/Starraider/dataforseo-skills --skill dataforseo-api
npx skills add https://github.com/Starraider/dataforseo-skills --skill technical-seo-page-audit
```

### Composer

```bash
composer require Starraider/dataforseo-skills
```

### Git clone

```bash
git clone https://github.com/Starraider/dataforseo-skills.git
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Changes to discovery fields must document why an override is intentional.

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

Developed and maintained by [Sven Kalbhenn](https://www.skom.de/).
