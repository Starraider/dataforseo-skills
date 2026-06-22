# DataForSEO Skills

## What this skill solves

This skill collection turns professional search data into clear, practical SEO recommendations. It helps businesses, consultants, and agencies understand how a website performs, find opportunities for growth, and decide what to improve next—from technical issues and keyword gaps to rankings, content, competitors, and international markets. Each skill follows a focused workflow and produces an actionable report, making reliable SEO analysis easier to run, repeat, and share.

The goal is to provide the insight of established SEO platforms without requiring another expensive monthly subscription. The skills use DataForSEO's pay-as-you-go data, so you pay only for the API requests needed for each analysis. An individual SEO analysis typically costs just a few cents, and many cost less than one cent, depending on the data and endpoints used.

To use this collection, you need an active DataForSEO account and should install and configure the DataForSEO MCP server. Analysis and reporting skills use DataForSEO through that server or a documented direct API helper and follow the official [DataForSEO API documentation](https://docs.dataforseo.com/v3/).

## Why DataForSEO

[DataForSEO](https://dataforseo.com/?aff=292583) provides extensive search, keyword, competitor, domain, business, and on-page databases together with a broad range of API functions for retrieving and combining that information. These capabilities make it possible to build focused SEO workflows for technical audits, keyword research, competitor analysis, content planning, and rank tracking while paying only for the API requests used. The result is access to valuable SEO intelligence and automation without requiring a full SaaS subscription.

Simpler crawling tools such as Screaming Frog or On-Page-Crawler are useful for inspecting a website's own pages and technical signals, but they do not provide the same breadth of external search-market data. In particular, a crawler alone cannot supply DataForSEO's keyword volumes, live search results and rankings, competitor visibility, estimated traffic, keyword gaps, or related market intelligence. DataForSEO therefore complements page crawling with the broader datasets needed to understand how a website performs in search and where its best opportunities lie.

> **Please Support this project:** When creating a DataForSEO account, please register through my [DataForSEO affiliate link](https://dataforseo.com/?aff=292583). Using this link supports my continued work on these skills at no additional cost or disadvantage to you; your account, pricing, and access remain the same.

## Use when

Use this collection when you want reliable answers to practical SEO questions without manually gathering and interpreting data from multiple sources. The skills can help you:

- understand how well a website or individual page performs in Google;
- find technical problems that may prevent a page from ranking well;
- discover valuable keywords, realistic growth opportunities, and the competitors already winning those searches;
- decide what content to create, improve, combine, or remove;
- improve existing copy, page titles, descriptions, social previews, and page structure;
- identify pages competing against each other for the same searches and strengthen internal links;
- track current rankings, spot meaningful gains or losses, and estimate the traffic better rankings could generate;
- compare opportunities in different countries and languages; or
- plan a custom SEO analysis and choose the right DataForSEO tools when no ready-made workflow fits the question.

## Expected outputs

Each skill turns DataForSEO data into a report designed to support a decision—not a dump of technical metrics. Depending on the analysis you choose, you will receive:

- **A clear summary of what matters most:** the main findings, the strongest opportunities, and a prioritized list of recommended next steps.
- **A consolidated full SEO plan:** date-selected reports for one domain can be reconciled into one short action plan with owners, implementation steps, KPIs, and particularly attractive ranking opportunities.
- **A practical website health check:** technical problems explained by importance, with affected pages or resources where available and a DataForSEO-derived Technical Score for quick orientation.
- **A clearer view of the search market:** the competitors attracting the same audience, the keywords they rank for, and the gaps your website can realistically target. Competitor, keyword, and content scores make large result sets easier to compare.
- **An actionable content plan:** topics worth creating, pages that need refreshing, and guidance for improving copy, metadata, social previews, and eligibility for prominent Google result features. Where several pages target the same search, the report explains which page should lead and whether the others should be combined, redirected, or made more distinct.
- **Ranking and growth guidance:** current Google positions, important changes over time, terms close to page one, and the best action for each keyword. Forecasts show conservative, expected, and ambitious traffic scenarios so potential gains are easier to evaluate.
- **International expansion guidance:** a comparison of countries and languages, including local demand, competitor strength, translation risks, recommended launch order, and suitable URL structures.
- **Evidence you can review:** the market, language, assumptions, coverage, limitations, and supporting DataForSEO results used for the recommendations.
- **Transparent usage costs:** every report records the cost of each DataForSEO request and shows the total in its Scope section.

## Context requirements

Before using these skills, you need a [DataForSEO account](https://dataforseo.com/?aff=292583) and the official DataForSEO MCP server must be installed and connected to it. Your account must have a positive balance so the skills can request data. A few dollars is usually enough to get started and run several typical analyses, although the exact cost depends on the amount and type of data requested.

Most skills need only a few details from you. Website analyses require a domain or page URL, while ranking checks also need a keyword list. Keyword research needs either a topic to explore or a domain whose existing keywords should be analyzed. International analysis requires the website's current language and at least two country-and-language markets to compare. Growth forecasts also need a target country, language, and forecast period. Full SEO reports require a domain plus one date or an inclusive date range and use the matching date-prefixed files already stored under the domain's report folder. Text optimization is the main exception: it needs the complete text and one to three starting keywords, but no website domain. The skills ask for any essential information that is missing before making chargeable requests.

For the most detailed results, the `seo-technical-page-audit` skill uses Python 3 to run a helper that accesses DataForSEO OnPage task endpoints not currently available through the MCP server. This provides richer crawl evidence and device-specific technical data. The audit can still run without Python 3 by using the available MCP tools, but the resulting report will contain less detailed data. Full-detail mode also needs DataForSEO credentials stored securely in a `.env` file; the skill asks only for the file's location when it cannot find one in the project folder.

The `seo-ranking-watchlist` skill uses Python 3 for its preferred direct API helper, which reduces large DataForSEO responses locally and safely stages resumable ranking checks before updating the watchlist. If Python 3, the helper, or local API credentials are unavailable before a direct request starts, the skill falls back to the DataForSEO MCP server and limits new keyword discovery to the first 20 keywords instead of 100; explicit and previously saved keywords are still preserved.

The `seo-page-metadata` skill also requires Python 3. It uses a local helper to validate the supplied page URL, normalize the returned content, safely extract fallback page text when needed, and generate a consistent report path. All reporting skills require permission to save Markdown files, while the ranking watchlist additionally needs permission to maintain its local history file.

## Example prompts

See the individual skill READMEs for invocation examples.

## Available skills

Choose the skill that matches the SEO question you want to answer. Each skill saves a corresponding report. For requirements, examples, and full report contents, see the README linked with each description.

- **`dataforseo-skill`** — Creates a custom, evidence-based SEO analysis when none of the specialized skills fits your question. This is useful for investigating a specific website challenge or opportunity with reliable search data. [More details in the skill README](skills/dataforseo-skill/README.md).

- **`seo-technical-page-audit`** — Checks one webpage for problems that could make it harder for search engines or visitors to use. This helps you focus first on the fixes most likely to improve the page's search performance. [More details in the skill README](skills/seo-technical-page-audit/README.md).

- **`seo-competitor-gap-analysis`** — Shows which websites compete with yours in Google and where they attract search traffic that you do not. This reveals realistic opportunities to strengthen your website and win more relevant visitors. [More details in the skill README](skills/seo-competitor-gap-analysis/README.md).

- **`seo-keyword-research`** — Finds the words and questions people use when searching for your products, services, or topics. This helps you choose subjects with genuine demand and create content your audience is more likely to discover. [More details in the skill README](skills/seo-keyword-research/README.md).

- **`seo-rankings`** — Checks where your website currently appears in Google for the keywords that matter to you. This makes it easier to see what is performing well, what needs attention, and where improvement is most achievable. [More details in the skill README](skills/seo-rankings/README.md).

- **`seo-ranking-watchlist`** — Monitors important Google rankings over time and highlights meaningful gains, losses, and keywords close to the first page. This helps you react quickly to declining visibility and recognize promising opportunities. [More details in the skill README](skills/seo-ranking-watchlist/README.md).

- **`seo-content-suggestions`** — Identifies subjects your website covers well, topics it is missing, and useful new article ideas. This helps build a more complete content offering that can attract the right audience and strengthen your authority in search. [More details in the skill README](skills/seo-content-suggestions/README.md).

- **`seo-content-decay-refresh`** — Finds existing pages that are losing search visibility and recommends whether to update, combine, redirect, or leave them unchanged. This helps recover value from content you already own instead of always creating something new. [More details in the skill README](skills/seo-content-decay-refresh/README.md).

- **`seo-cannibalization-internal-linking`** — Finds pages on your website that compete with each other for the same searches and identifies opportunities to connect related content more effectively. This helps search engines understand which pages are most important and can concentrate ranking strength in the right places. [More details in the skill README](skills/seo-cannibalization-internal-linking/README.md).

- **`seo-text-keyword-optimization`** — Reviews supplied text and suggests relevant search terms and practical ways to improve the wording. This helps the content match what potential visitors are looking for while preserving its purpose and readability. [More details in the skill README](skills/seo-text-keyword-optimization/README.md).

- **`seo-page-metadata`** — Recommends stronger page titles, search descriptions, and social-sharing text for one webpage. This helps search engines understand the page and can make its listing more appealing to potential visitors. [More details in the skill README](skills/seo-page-metadata/README.md).

- **`seo-serp-optimization`** — Finds opportunities for a webpage to appear more prominently in Google and recommends content improvements that support those opportunities. This can help the page earn more attention and clicks from the search results. [More details in the skill README](skills/seo-serp-optimization/README.md).

- **`seo-international-opportunities`** — Compares search opportunities across countries and languages and identifies where expansion is most promising. This helps you choose markets carefully and create content that fits local search behavior rather than relying on direct translation alone. [More details in the skill README](skills/seo-international-opportunities/README.md).

- **`seo-growth-forecasting`** — Estimates how better Google rankings could affect future website traffic. This helps set realistic expectations, compare opportunities, and decide where SEO time and budget are most likely to produce value. [More details in the skill README](skills/seo-growth-forecasting/README.md).

- **`seo-full-report`** — Combines all SEO analyses for one domain from a supplied date or date range into one prioritized implementation plan. This helps teams focus on the most critical fixes, coordinate overlapping recommendations, and act on the strongest ranking opportunities first. [More details in the skill README](skills/seo-full-report/README.md).

## Related skills

- `dataforseo-skill`: general DataForSEO MCP tool selection, sequencing, validation, protocol guidance, and troubleshooting.
- `seo-technical-page-audit`: task-based single-page technical SEO analysis and fix-ready Markdown reporting.
- `seo-competitor-gap-analysis`: organic competitor discovery, keyword-gap analysis, Competitive Score, and Markdown reporting.
- `seo-keyword-research`: seed- and domain-based keyword discovery, intent grouping, opportunity scoring, and Markdown reporting.
- `seo-rankings`: live Google organic rank checking, search-volume context, tiered actions, and Markdown reporting.
- `seo-ranking-watchlist`: persistent file-based keyword monitoring through a compact direct API helper with a 20-keyword MCP discovery fallback, live position diffs across runs, and optional ranking-change reports.
- `seo-content-suggestions`: topical clustering, competitor content gaps, Content Score, and prioritized article briefs.
- `seo-content-decay-refresh`: ranking-decay detection, seasonality classification, traffic-impact estimates, and refresh briefs for existing pages.
- `seo-cannibalization-internal-linking`: same-intent keyword overlap, primary-page selection, consolidation or differentiation decisions, and sampled internal-link mapping.
- `seo-text-keyword-optimization`: supplied-text keyword discovery, low-difficulty prioritization, and three concrete revision approaches.
- `seo-page-metadata`: primary-topic extraction, keyword-opportunity ranking, and coherent search/social metadata packages.
- `seo-serp-optimization`: live SERP-feature ownership, attainability, page-format comparison, and exact structural recommendations.
- `seo-international-opportunities`: isolated country/language opportunity comparison, localized keyword clusters, market sequencing, and international URL planning.
- `seo-growth-forecasting`: conservative, expected, and ambitious organic growth scenarios with page- and keyword-level derived traffic estimates and opportunity-versus-difficulty prioritization.
- `seo-full-report`: date-scoped source reconciliation, current visibility validation, ranking-opportunity highlights, and an action-first 30/60/90-day SEO plan.

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
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-ranking-watchlist
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-content-suggestions
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-content-decay-refresh
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-cannibalization-internal-linking
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-text-keyword-optimization
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-page-metadata
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-serp-optimization
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-international-opportunities
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-growth-forecasting
npx skills add https://github.com/Starraider/dataforseo-skills --skill seo-full-report
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

## Repository extras

- `agents/*.yaml` provides OpenAI-facing discovery metadata for each reporting skill.
- All skills keep their runtime instructions in `SKILL.md`; all reporting skills include non-live evaluation cases.
- GitHub Pages should remain disabled because the README and marketplace entry are sufficient.
- Proposed GitHub description: `Agent skills for DataForSEO MCP analysis, technical audits, competitor gaps, keyword research, full SEO reports, SEO growth forecasting, international SEO opportunities, content-decay refreshes, keyword cannibalization, internal linking, text optimization, page metadata, SERP features, topical authority, live rank checking, and ranking watchlists.`
- Proposed GitHub topics: `agent-skill`, `dataforseo`, `mcp`, `seo`, `technical-seo`, `competitor-analysis`, `keyword-gap`, `keyword-research`, `full-seo-report`, `seo-prioritization`, `seo-forecasting`, `organic-traffic-forecast`, `international-seo`, `seo-localization`, `content-decay`, `content-refresh`, `keyword-cannibalization`, `internal-linking`, `content-optimization`, `page-metadata`, `serp-features`, `featured-snippets`, `topical-authority`, `content-gap`, `rank-tracking`, `ranking-watchlist`.

## License

Developed and maintained by Sven Kalbhenn.
Code and scripts: [LICENSE-MIT](LICENSE-MIT) (Sven Kalbhenn)
Skills and documentation: [LICENSE-CC-BY-SA-4.0](LICENSE-CC-BY-SA-4.0)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Changes to discovery fields must document why an override is intentional.

Questions and feedback welcome via GitHub issues or e-mail: sven@skom.de
