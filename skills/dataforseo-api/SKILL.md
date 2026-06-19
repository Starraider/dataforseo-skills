---
name: dataforseo-api
description: "Use when planning, implementing, reviewing, or troubleshooting DataForSEO API integrations, including endpoint selection, task lifecycle handling, authentication, rate limits, cost controls, and response normalization."
license: "(MIT AND CC-BY-SA-4.0). See LICENSE-MIT and LICENSE-CC-BY-SA-4.0"
compatibility: "Requires network access for live DataForSEO requests and credentials supplied through environment variables."
---

# DataForSEO API

Build reliable DataForSEO integrations without guessing endpoint behavior or silently creating billable work.

## Workflow

1. Identify the required dataset, target, location, language, freshness, and output format.
2. Consult the current official DataForSEO documentation before selecting an endpoint or request schema. Do not rely on remembered endpoint details.
3. Determine whether the endpoint is live or task-based. For task-based APIs, model submission, polling or retrieval, terminal states, and partial failures explicitly.
4. Estimate request volume and explain likely billing implications before issuing broad, repeated, or high-volume requests.
5. Keep credentials in environment variables. Never write credentials to source files, logs, fixtures, examples, or command history.
6. Implement bounded retries with backoff for transient failures. Do not retry validation, authentication, or insufficient-balance failures blindly.
7. Preserve the provider status code and message while normalizing results. Handle successful HTTP responses that contain task-level errors.
8. Add tests using sanitized fixtures or mocks. Live tests must be opt-in and clearly marked as billable.
9. Report the selected endpoint, assumptions, estimated request count, changed files, and verification performed.

## Guardrails

- Ask before making billable live requests unless the user explicitly authorized them.
- Start with the smallest representative query.
- Never expose the DataForSEO login, password, authorization header, or raw environment contents.
- Treat rate limits, pagination, duplicate tasks, and idempotency as design requirements.
- Separate transport errors, provider-level errors, and empty-but-valid results.
- Prefer official DataForSEO documentation and schemas over third-party examples.

## Expected Result

Produce maintainable integration code or a concrete implementation plan with explicit request semantics, safe credential handling, cost-aware execution, and verification evidence.

