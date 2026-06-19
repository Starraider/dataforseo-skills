# Repository instructions

- This repository is intended to contain multiple skills for performing SEO analyses and generating corresponding SEO reports.
- Every SEO analysis and reporting skill must use the DataForSEO MCP server.
- Use the official [DataForSEO API documentation](https://docs.dataforseo.com/v3/) and [DataForSEO White Papers and knowledge base](https://dataforseo.com/knowledgebase) when designing, implementing, or verifying skills.
- Keep each skill under `skills/<skill-name>/SKILL.md` and register it in both plugin and distribution manifests.
- Keep `SKILL.md` frontmatter limited to Agent Skills specification fields and begin descriptions with `Use when`.
- Never commit DataForSEO credentials, authorization headers, live response data containing customer information, or billable live-test defaults.
- Run `scripts/validate-skill.sh` before submitting changes.
- Keep discovery metadata, README claims, and marketplace metadata aligned.
