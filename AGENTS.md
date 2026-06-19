# Repository instructions

- This repository is intended to contain multiple skills for performing SEO analyses and generating corresponding SEO reports.
- Current skills:
  - `skills/seo-technical-page-audit/SKILL.md` audits one supplied page with the DataForSEO MCP OnPage tools, assigns a DataForSEO-derived Technical Score, prioritizes fixes, and writes a detailed Markdown report.
  - `skills/seo-competitor-gap-analysis/SKILL.md` identifies organic competitors with the DataForSEO MCP tools, quantifies keyword and traffic gaps, scores competitiveness, and writes a detailed Markdown report.
  - `skills/seo-keyword-research/SKILL.md` researches seed- or domain-based keywords with the DataForSEO MCP tools, scores opportunities, and writes a detailed Markdown report.
  - `skills/seo-rankings/SKILL.md` checks live Google organic positions and search volumes for a domain and keyword list, assigns ranking tiers and actions, and writes a detailed Markdown report.
- Every SEO analysis and reporting skill must use the DataForSEO MCP server.
- Use the official [DataForSEO API documentation](https://docs.dataforseo.com/v3/) and [DataForSEO White Papers and knowledge base](https://dataforseo.com/knowledgebase) when designing, implementing, or verifying skills.
- Keep each skill under `skills/<skill-name>/SKILL.md` and register it in both plugin and distribution manifests.
- Keep `SKILL.md` frontmatter limited to Agent Skills specification fields and begin descriptions with `Use when`.
- Never commit DataForSEO credentials, authorization headers, live response data containing customer information, or billable live-test defaults.
- For `seo-technical-page-audit`, require an absolute HTTP(S) page URL, ask for it when absent, and use `SEO/<domain>/` as the default report directory unless the user specifies another location.
- Preserve the requested report filename convention: `<YYYY-MM-DD>_Techical-Report_<safe-URL>.md`.
- Run `scripts/validate-skill.sh` before submitting changes.
- Keep discovery metadata, README claims, and marketplace metadata aligned.
