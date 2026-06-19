# Repository instructions

- This repository is intended to contain multiple skills for performing SEO analyses and generating corresponding SEO reports.
- Current skills:
  - `skills/dataforseo-api/SKILL.md` plans, implements, reviews, and troubleshoots DataForSEO API integrations.
  - `skills/technical-seo-page-audit/SKILL.md` audits one supplied page with the DataForSEO MCP OnPage tools, assigns a DataForSEO-derived Technical Score, prioritizes fixes, and writes a detailed Markdown report.
- Every SEO analysis and reporting skill must use the DataForSEO MCP server.
- Use the official [DataForSEO API documentation](https://docs.dataforseo.com/v3/) and [DataForSEO White Papers and knowledge base](https://dataforseo.com/knowledgebase) when designing, implementing, or verifying skills.
- Keep each skill under `skills/<skill-name>/SKILL.md` and register it in both plugin and distribution manifests.
- Keep `SKILL.md` frontmatter limited to Agent Skills specification fields and begin descriptions with `Use when`.
- Never commit DataForSEO credentials, authorization headers, live response data containing customer information, or billable live-test defaults.
- For `technical-seo-page-audit`, require an absolute HTTP(S) page URL, ask for it when absent, and use `/SEO/` as the default report directory unless the user specifies another location.
- Preserve the requested report filename convention: `<YYYY-MM-DD>_Techical-Report_<safe-URL>.md`.
- Run `scripts/validate-skill.sh` before submitting changes.
- Keep discovery metadata, README claims, and marketplace metadata aligned.
