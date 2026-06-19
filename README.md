# DataForSEO Skills

## What this skill solves

This repository is intended to grow into a collection of skills that perform SEO analyses and generate corresponding SEO reports. Each analysis and reporting skill uses the DataForSEO MCP server and follows the official [DataForSEO API documentation](https://docs.dataforseo.com/v3/) and [DataForSEO White Papers and knowledge base](https://dataforseo.com/knowledgebase).

## Use when

Use these skills to audit one page for technical SEO, identify true Google organic competitors, research and score keyword opportunities, or check live Google rankings for a supplied keyword list.

## Expected outputs

- A prioritized technical SEO report with a provider-derived Technical Score.
- A competitor report with up to 20 discovered domains, detailed top-five comparisons, and a 0-100 Competitive Score.
- A keyword analysis with intent groups, top-20 opportunities, and a reproducible 0-100 Keyword Score.
- A live rankings report with search volume, tier, and one prioritized action per keyword.

## Context requirements

Configure the official DataForSEO MCP server and credentials securely. Every analysis requires a website project domain; page URLs supply it implicitly through their hostname. Keyword research also requires a seed or uses the project domain as its analysis target. Rank checking requires a keyword list. Filesystem write access is required for Markdown reports.

## Example prompts

```text
Audit https://example.com/products/widget for technical SEO and save the report in the default location.
Identify the true organic SEO competitors for example.com and quantify the keyword and traffic gap.
Research the seed keyword electric bikes for example.com, score the best opportunities, and save a detailed report.
Check example.com rankings for seo audit tool, keyword research, and ai seo, then prioritize the next actions.
```

## Available skills

### `seo-technical-page-audit`

Audits one specific page through the official DataForSEO MCP OnPage tools. It checks availability, indexability, redirects, broken-link and resource signals, metadata, headings, canonicalization, structured-data gaps, page speed, Core Web Vitals, and related technical SEO issues. It returns the DataForSEO-derived Technical Score from 0 to 100, prioritizes fixes from P0 to P3, and writes a detailed dated Markdown report under the normalized project domain, using `SEO/<domain>/` by default.

The page URL supplies the project domain. If the prompt does not contain a URL or separate domain, the skill asks for the domain; it always asks for the URL when that is absent, before making billable DataForSEO requests.

Example prompt:

```text
Audit https://example.com/products/widget for technical SEO, prioritize the fixes, and save the detailed Markdown report in the default location.
```

### `seo-competitor-gap-analysis`

Finds up to 20 true organic-search competitors through DataForSEO Labs, ranks them by SERP keyword overlap, and analyzes the top five for shared and unique keywords, average position gaps, defensive wins, traffic estimates, and strategic grouping. It calculates the requested 0-100 Competitive Score and writes a detailed dated Markdown report under the normalized project domain, using `SEO/<domain>/` by default.

If the prompt does not contain a domain, the skill asks for one before making billable DataForSEO requests.

Example prompt:

```text
Identify the true SEO competitors for example.com, quantify the gap, and save the detailed report in the default location.
```

### `seo-keyword-research`

Researches a seed keyword through up to 200 related terms and 100 long-tail suggestions, or finds up to 100 organic keywords for which a domain already ranks. It reports search volume, CPC, Ads competition, keyword difficulty, and intent; surfaces the top 20 by volume-to-difficulty opportunity; calculates a transparent 0-100 Keyword Score; and writes a detailed dated Markdown report under the normalized project domain, using `SEO/<domain>/` by default.

The skill always requires a project domain and asks for it before making billable DataForSEO requests when it is absent, including seed-based research.

Example prompt:

```text
Research electric bikes for example.com, group the keywords by intent, score the top opportunities, and save the report in the default location.
```

### `seo-rankings`

Checks live Google organic positions for a supplied domain and keyword list through DataForSEO MCP, adds search volume, and groups each keyword as Winning, Page 1, Close, Long-haul, or Not ranking. It assigns one next action per keyword, selects the single highest-leverage action overall, and writes a detailed dated Markdown report under the normalized project domain, using `SEO/<domain>/` by default.

If the prompt omits the domain or keyword list, the skill asks for all missing required inputs before making billable DataForSEO requests. Location, language, device, and depth default to United States, `en`, desktop, and 100.

Example prompt:

```text
Check example.com rankings for seo audit tool, keyword research, and ai seo, then save the detailed report in the default location.
```

## Related skills

- `seo-technical-page-audit`: single-page technical SEO analysis and Markdown reporting.
- `seo-competitor-gap-analysis`: organic competitor discovery, keyword-gap analysis, Competitive Score, and Markdown reporting.
- `seo-keyword-research`: seed- and domain-based keyword discovery, intent grouping, opportunity scoring, and Markdown reporting.
- `seo-rankings`: live Google organic rank checking, search-volume context, tiered actions, and Markdown reporting.

## Installation

### Prerequisites

Before using the SEO analysis and reporting skills:

- Install and configure the DataForSEO MCP server in your Agent Skills-compatible client.
- Set up an appropriate [DataForSEO account](https://app.dataforseo.com/register) with access to the APIs required by the selected skill.
- Provide credentials through the MCP server's secure configuration. Do not store credentials in this repository.

Then browse the marketplace and install the skill needed for your workflow.

### Agent Skills-compatible clients

```bash
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-technical-page-audit
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-competitor-gap-analysis
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-keyword-research
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-rankings
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

- `agents/*.yaml` provides OpenAI-facing discovery metadata for each reporting skill.
- All skills keep their runtime instructions in `SKILL.md`; all reporting skills include non-live evaluation cases.
- GitHub Pages should remain disabled because the README and marketplace entry are sufficient.
- Proposed GitHub description: `Agent skills for DataForSEO technical audits, competitor-gap reports, keyword research, and live rank checking.`
- Proposed GitHub topics: `agent-skill`, `dataforseo`, `seo`, `technical-seo`, `competitor-analysis`, `keyword-gap`, `keyword-research`, `rank-tracking`.

Developed and maintained by [Sven Kalbhenn](https://www.skom.de/).
