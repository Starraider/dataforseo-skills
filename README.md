# DataForSEO Skills

## What this skill solves

This collection of AI skills provides general DataForSEO MCP guidance plus practical SEO analysis and reporting tools as a cost-effective alternative to subscription services such as Semrush or Ahrefs. It is particularly useful for small businesses and independent professionals who need professional SEO data without committing to another recurring subscription. Instead, the skills use DataForSEO's pay-what-you-use model, so costs are tied to the analyses and API data actually requested.

Each analysis and reporting skill uses the DataForSEO MCP server and follows the official [DataForSEO API documentation](https://docs.dataforseo.com/v3/) and [DataForSEO White Papers and knowledge base](https://dataforseo.com/knowledgebase).

## Why DataForSEO

[DataForSEO](https://dataforseo.com/?aff=292583) provides extensive search, keyword, competitor, domain, business, and on-page databases together with a broad range of API functions for retrieving and combining that information. These capabilities make it possible to build focused SEO workflows for technical audits, keyword research, competitor analysis, content planning, and rank tracking while paying only for the API requests used. The result is access to valuable SEO intelligence and automation without requiring a full SaaS subscription.

Simpler crawling tools such as Screaming Frog or On-Page-Crawler are useful for inspecting a website's own pages and technical signals, but they do not provide the same breadth of external search-market data. In particular, a crawler alone cannot supply DataForSEO's keyword volumes, live search results and rankings, competitor visibility, estimated traffic, keyword gaps, or related market intelligence. DataForSEO therefore complements page crawling with the broader datasets needed to understand how a website performs in search and where its best opportunities lie.

> **Please Support this project:** When creating a DataForSEO account, please register through my [DataForSEO affiliate link](https://dataforseo.com/?aff=292583). Using this link supports my continued work on these skills at no additional cost or disadvantage to you; your account, pricing, and access remain the same.

## Use when

Use these skills to select and troubleshoot DataForSEO MCP tools, perform a custom evidence-based SEO analysis, audit one page for technical SEO, identify true Google organic competitors, research and score keyword opportunities, optimize supplied prose around low-difficulty keywords, generate evidence-based page and social metadata, assess topical authority and content gaps, or check live Google rankings for a supplied keyword list.

## Expected outputs

- A scoped, cost-aware DataForSEO MCP call plan or custom SEO analysis with validated evidence, coverage, and limitations.
- A prioritized technical SEO report with a provider-derived Technical Score.
- A competitor report with up to 20 discovered domains, detailed top-five comparisons, and a 0-100 Competitive Score.
- A keyword analysis with intent groups, top-20 opportunities, and a reproducible 0-100 Keyword Score.
- A supplied-text optimization report with up to 20 low-hanging-fruit keywords and three distinct revision approaches.
- A page-metadata report with five primary-content-derived seeds, explicit market/language provenance, up to 20 ranked keyword opportunities, and three coherent search and social metadata packages with one recommendation.
- A live rankings report with search volume, tier, and one prioritized action per keyword.
- A topical-authority report with a 0-100 Content Score, cluster gaps, and five prioritized article briefs.
- A per-call DataForSEO cost log and summed `Total cost: x,xx USD` value in every report's Scope section.

## Context requirements

Configure the official DataForSEO MCP server and credentials securely. Technical page audits also require Python 3 and a `.env` credential file so the skill can call task endpoints missing from MCP. The helper looks in the project root first and asks for the file path when it is absent. Page-metadata analysis requires Python 3 for deterministic response normalization and report-path generation. Domain- and page-based analyses require a website project domain or URL. Keyword research also requires a seed or uses the project domain as its analysis target. Text keyword optimization requires complete supplied prose and one to three seeds, but no domain. Page-metadata analysis requires one absolute HTTP(S) page URL. Rank checking requires a keyword list. Content suggestions optionally accept up to five competitor domains and discover them when omitted. Filesystem write access is required for Markdown reports.

## Example prompts

See the individual skill READMEs for invocation examples.

## Available skills

Each skill below has a dedicated README with the full behavior, invocation examples, and report expectations:

- [seo-technical-page-audit](skills/seo-technical-page-audit/README.md)
- [seo-competitor-gap-analysis](skills/seo-competitor-gap-analysis/README.md)
- [seo-keyword-research](skills/seo-keyword-research/README.md)
- [seo-rankings](skills/seo-rankings/README.md)
- [seo-content-suggestions](skills/seo-content-suggestions/README.md)
- [seo-text-keyword-optimization](skills/seo-text-keyword-optimization/README.md)
- [seo-page-metadata](skills/seo-page-metadata/README.md)
- [dataforseo-skill](skills/dataforseo-skill/README.md)

### `dataforseo-skill`

Selects, sequences, calls, validates, and troubleshoots DataForSEO MCP tools for custom SEO analyses. It includes a captured catalog of 83 exposed tools with exact callable declarations and underlying REST mappings, plus protocol, authentication, response, error, rate-limit, pagination, batching, callback, SDK, and workflow references.

Detailed reference: [skills/dataforseo-skill/README.md](skills/dataforseo-skill/README.md)

The active MCP `tools/list` and input schema remain authoritative because enabled modules and deployed tool versions can differ from the captured catalog.

### `seo-technical-page-audit`

Audits one specific page through DataForSEO MCP and a direct REST bridge for task endpoints that MCP does not expose. It runs a one-page crawl with sitewide checks enabled, then collects page, link, redirect, non-indexable, resource, schema, waterfall, and Lighthouse evidence to produce a fix-ready Markdown report. If direct task access fails, it falls back to MCP Instant Pages plus Lighthouse. The report returns the DataForSEO-derived Technical Score from 0 to 100, lists exact affected URLs or assets where available, prioritizes fixes from P0 to P3, and writes a detailed dated Markdown report under the normalized project domain, using `SEO/<domain>/` by default.

Detailed reference: [skills/seo-technical-page-audit/README.md](skills/seo-technical-page-audit/README.md)

The page URL supplies the project domain. If the prompt does not contain a URL or separate domain, the skill asks for the domain; it always asks for the URL when that is absent, before making billable DataForSEO requests.

### `seo-competitor-gap-analysis`

Finds up to 20 true organic-search competitors through DataForSEO Labs, ranks them by SERP keyword overlap, and analyzes the top five for shared and unique keywords, average position gaps, defensive wins, traffic estimates, and strategic grouping. It calculates the requested 0-100 Competitive Score and writes a detailed dated Markdown report under the normalized project domain, using `SEO/<domain>/` by default.

Detailed reference: [skills/seo-competitor-gap-analysis/README.md](skills/seo-competitor-gap-analysis/README.md)

If the prompt does not contain a domain, the skill asks for one before making billable DataForSEO requests.

### `seo-keyword-research`

Researches a seed keyword through up to 200 related terms and 100 long-tail suggestions, or finds up to 100 organic keywords for which a domain already ranks. It reports search volume, CPC, Ads competition, keyword difficulty, and intent; surfaces the top 20 by volume-to-difficulty opportunity; calculates a transparent 0-100 Keyword Score; and writes a detailed dated Markdown report under the normalized project domain, using `SEO/<domain>/` by default.

Detailed reference: [skills/seo-keyword-research/README.md](skills/seo-keyword-research/README.md)

The skill always requires a project domain and asks for it before making billable DataForSEO requests when it is absent, including seed-based research.

### `seo-rankings`

Checks live Google organic positions for a supplied domain and keyword list through DataForSEO MCP, adds search volume, and groups each keyword as Winning, Page 1, Close, Long-haul, or Not ranking. It assigns one next action per keyword, selects the single highest-leverage action overall, and writes a detailed dated Markdown report under the normalized project domain, using `SEO/<domain>/` by default.

Detailed reference: [skills/seo-rankings/README.md](skills/seo-rankings/README.md)

If the prompt omits the domain or keyword list, the skill asks for all missing required inputs before making billable DataForSEO requests. Location, language, device, and depth default to United States, `en`, desktop, and 100.

### `seo-content-suggestions`

Clusters up to 200 keywords for which a domain ranks into 8-15 topical groups, discovers or accepts up to five competitors, and uses DataForSEO Labs keyword gaps to classify each cluster as Strong, Building, Weak, or Missing. It calculates a reproducible 0-100 Content Score and recommends five specific commercial or transactional articles using search volume, keyword difficulty, intent, and competitor authority. The detailed dated Markdown report is saved under the normalized project domain, using `SEO/<domain>/` by default.

Detailed reference: [skills/seo-content-suggestions/README.md](skills/seo-content-suggestions/README.md)

If the prompt does not contain a domain, the skill asks for one before making billable DataForSEO requests.

### `seo-text-keyword-optimization`

Accepts complete supplied prose and one to three seed keywords, retrieves up to 50 related keywords per seed through DataForSEO Labs, deduplicates and relevance-filters the combined pool, and ranks up to 20 low-hanging-fruit terms using search volume and organic keyword difficulty. It then proposes three materially different optimization approaches with concrete keyword-to-text mappings and recommends one. The detailed dated Markdown report is saved under `SEO/text-keyword-optimization/` by default.

Detailed reference: [skills/seo-text-keyword-optimization/README.md](skills/seo-text-keyword-optimization/README.md)

The skill asks for missing text or seeds before making billable calls. It defaults to United States/English only when the supplied language does not conflict with that scope.

### `seo-page-metadata`

Analyzes one exact page with DataForSEO OnPage, derives five evidence-backed seed keywords from qualifying primary content, and requests up to 25 related keywords for each seed. It preserves nulls and provenance, records conflicts and exclusions, and ranks up to 20 complete relevant rows with a transparent volume-to-difficulty proxy. The report recommends one of three coherent Page Title, Meta Description, Open Graph, and Twitter Card packages with Unicode code-point counts. Legacy meta keywords are included only when explicitly requested. The report is saved under the normalized project domain, using `SEO/<domain>/` by default.

Detailed reference: [skills/seo-page-metadata/README.md](skills/seo-page-metadata/README.md)

If the prompt does not contain an absolute HTTP(S) page URL, the skill asks for one before making billable DataForSEO requests.

Every generated report records each DataForSEO call's response cost and shows the summed value in its Scope section as `Total cost: x,xx USD`.

## Related skills

- `dataforseo-skill`: general DataForSEO MCP tool selection, sequencing, validation, protocol guidance, and troubleshooting.
- `seo-technical-page-audit`: task-based single-page technical SEO analysis and fix-ready Markdown reporting.
- `seo-competitor-gap-analysis`: organic competitor discovery, keyword-gap analysis, Competitive Score, and Markdown reporting.
- `seo-keyword-research`: seed- and domain-based keyword discovery, intent grouping, opportunity scoring, and Markdown reporting.
- `seo-rankings`: live Google organic rank checking, search-volume context, tiered actions, and Markdown reporting.
- `seo-content-suggestions`: topical clustering, competitor content gaps, Content Score, and prioritized article briefs.
- `seo-text-keyword-optimization`: supplied-text keyword discovery, low-difficulty prioritization, and three concrete revision approaches.
- `seo-page-metadata`: primary-topic extraction, keyword-opportunity ranking, and coherent search/social metadata packages.

## Installation

### Prerequisites

Before using the SEO analysis and reporting skills:

- Register for a [DataForSEO account](https://app.dataforseo.com/?aff=292583).
- Install and configure the [DataForSEO MCP server](https://dataforseo.com/model-context-protocol) in your Agent Skills-compatible client.
- Provide credentials through the MCP server's secure configuration.
- Provide a git-ignored `.env` containing `DATAFORSEO_USERNAME` and `DATAFORSEO_PASSWORD` for the technical audit's direct task API bridge; `DATAFORSEO_LOGIN` is accepted as a username alias.

Then install the skills needed for your SEO workflow.

### Agent Skills-compatible clients

```bash
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-technical-page-audit
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-competitor-gap-analysis
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-keyword-research
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-rankings
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-content-suggestions
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-text-keyword-optimization
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-page-metadata
npx skills add https://github.com/Starraider/dataforseo-skills --skill dataforseo-skill
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
- Proposed GitHub description: `Agent skills for DataForSEO MCP analysis, technical audits, competitor gaps, keyword research, text optimization, page metadata, topical authority, and live rank checking.`
- Proposed GitHub topics: `agent-skill`, `dataforseo`, `mcp`, `seo`, `technical-seo`, `competitor-analysis`, `keyword-gap`, `keyword-research`, `content-optimization`, `page-metadata`, `topical-authority`, `content-gap`, `rank-tracking`.

Developed and maintained by [Sven Kalbhenn](https://www.skom.de/).
