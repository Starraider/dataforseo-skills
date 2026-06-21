# DataForSEO MCP protocol and REST reference

This reference covers behavior shared by the tool catalog. Per-tool names, descriptions, parameter contracts, accepted values, defaults, validation limits, underlying method/path, and official source links are in `mcp-tools.json`.

## Contents

- [Protocol layers](#protocol-layers)
- [MCP setup and authentication](#mcp-setup-and-authentication)
- [Raw MCP request and response syntax](#raw-mcp-request-and-response-syntax)
- [Underlying REST syntax](#underlying-rest-syntax)
- [Response contracts](#response-contracts)
- [Errors and retry handling](#errors-and-retry-handling)
- [Rate limits and timeouts](#rate-limits-and-timeouts)
- [Pagination and batching](#pagination-and-batching)
- [Encoding, uploads, and exports](#encoding-uploads-and-exports)
- [Callbacks and webhooks](#callbacks-and-webhooks)
- [Official clients and minimal REST calls](#official-clients-and-minimal-rest-calls)
- [Troubleshooting](#troubleshooting)

## Protocol layers

Keep these contracts distinct:

1. An agent calls an MCP tool by name with one JSON arguments object.
2. MCP Streamable HTTP carries a JSON-RPC `tools/call` request to `https://mcp.dataforseo.com/mcp` (the compatibility endpoint is `https://mcp.dataforseo.com/http`). A local installation normally uses stdio.
3. The official server maps arguments to DataForSEO REST at `https://api.dataforseo.com/v3/...`, normally as a one-element JSON task array.

For analysis, call the MCP tool. Raw MCP and REST examples below are for integration and troubleshooting.

## MCP setup and authentication

### Basic authentication

DataForSEO uses the API login and password from the API Access dashboard, not an arbitrary API-key header.

Remote HTTP header:

```http
Authorization: Basic <base64(username:password)>
```

Local stdio configuration:

```json
{
  "mcpServers": {
    "dataforseo": {
      "command": "npx",
      "args": ["-y", "dataforseo-mcp-server@latest"],
      "env": {
        "DATAFORSEO_USERNAME": "your_api_login",
        "DATAFORSEO_PASSWORD": "your_api_password"
      }
    }
  }
}
```

Never print, commit, or place the Base64 token in reports.

### OAuth 2.1 authorization code with PKCE

The remote server advertises:

```json
{
  "resource": "https://mcp.dataforseo.com/mcp",
  "authorization_servers": ["https://data.dataforseo.com"],
  "bearer_methods_supported": ["header"]
}
```

Authorization-server metadata currently declares `authorization_code` and `refresh_token`, PKCE `S256`, public clients (`token_endpoint_auth_methods_supported: ["none"]`), and scope `api`:

```text
GET https://data.dataforseo.com/.well-known/oauth-authorization-server
```

Flow:

1. Register a public client at `POST https://data.dataforseo.com/oauth/clients/register` using JSON registration metadata such as `client_name`, `redirect_uris`, `grant_types`, `response_types`, and `token_endpoint_auth_method: "none"`.
2. Generate a random `code_verifier`; send its Base64url SHA-256 digest as `code_challenge`.
3. Open `GET https://data.dataforseo.com/oauth/authorize` with `response_type=code`, `client_id`, exact `redirect_uri`, `scope=api`, `state`, `code_challenge`, `code_challenge_method=S256`, and `resource=https://mcp.dataforseo.com/mcp`.
4. Verify returned `state`, then exchange the code:

```http
POST https://data.dataforseo.com/oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&client_id=<id>&code=<code>&redirect_uri=<encoded-uri>&code_verifier=<verifier>&resource=https%3A%2F%2Fmcp.dataforseo.com%2Fmcp
```

5. Send `Authorization: Bearer <access_token>` on every MCP HTTP request.
6. When a refresh token is returned, refresh it with:

```http
POST https://data.dataforseo.com/oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&client_id=<id>&refresh_token=<refresh-token>&scope=api&resource=https%3A%2F%2Fmcp.dataforseo.com%2Fmcp
```

Use the actual metadata response and token response as authority; token lifetimes and refresh-token rotation are server-controlled. JWT is not a separate login flow. The MCP server accepts a Bearer token and checks a JWT `exp` claim when present; opaque Bearer tokens are also forwarded for authoritative validation.

## Raw MCP request and response syntax

Use an MCP SDK in production. For protocol version `2025-06-18`, every POST uses UTF-8 JSON and these headers:

```http
POST /mcp HTTP/1.1
Host: mcp.dataforseo.com
Authorization: Basic <token>  # or Bearer <access_token>
Content-Type: application/json
Accept: application/json, text/event-stream
MCP-Protocol-Version: 2025-06-18
```

Initialize first:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-06-18",
    "capabilities": {},
    "clientInfo": {"name": "seo-client", "version": "1.0.0"}
  }
}
```

Send `notifications/initialized`, then discover the deployment-specific catalog with `tools/list`. Call a tool as follows:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "dataforseo_labs_bulk_keyword_difficulty",
    "arguments": {
      "keywords": ["technical seo audit", "seo site audit"],
      "location_name": "United States",
      "language_code": "en"
    }
  }
}
```

If initialization returns `Mcp-Session-Id`, send it on subsequent requests. Do not invent one. Newer negotiated protocol versions may require additional mirrored `Mcp-Method` and `Mcp-Name` headers; follow the version returned by `initialize` and the matching MCP specification.

Successful tool-call envelope:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {"type": "text", "text": "{\n  \"id\": \"...\",\n  \"status_code\": 20000,\n  \"status_message\": \"Ok.\",\n  \"items\": []\n}"}
    ]
  }
}
```

The official server catches most tool/provider errors and returns text such as:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [{"type": "text", "text": "Error: API Error: ... (Code: 40501)"}]
  }
}
```

Treat that content as failure even if `isError` is absent.

## Underlying REST syntax

Canonical request:

```http
POST https://api.dataforseo.com/v3/dataforseo_labs/google/bulk_keyword_difficulty/live
Authorization: Basic <base64(login:password)>
Content-Type: application/json
Accept: application/json

[
  {
    "keywords": ["technical seo audit", "seo site audit"],
    "location_name": "United States",
    "language_code": "en"
  }
]
```

GET endpoints omit the request body unless the endpoint documentation explicitly allows filtering by POST. No cataloged endpoint uses query-string parameters; dynamic values appear in path segments. URL-encode dynamic path segments.

The MCP server sends `Authorization`, `Content-Type: application/json`, and a `User-Agent` identifying its package. By default it appends `.ai` to the underlying path to request a reduced response. `DATAFORSEO_FULL_RESPONSE=true` disables that behavior; several utility/model tools force the full endpoint. A field configuration can further reduce returned fields.

Stable REST response headers include:

- `Content-Type: application/json` for JSON responses.
- `X-RateLimit-Limit`: endpoint ceiling per minute.
- `X-RateLimit-Remaining`: remaining requests in the current window.
- `Content-Encoding: gzip` when compression is used.

Other headers such as `Date`, `Server`, `Content-Length`, connection handling, caching, and CORS vary and must not be hard-coded.

## Response contracts

Full DataForSEO response:

```json
{
  "version": "string",
  "status_code": 20000,
  "status_message": "Ok.",
  "time": "0.1234 sec.",
  "cost": 0.0103,
  "tasks_count": 1,
  "tasks_error": 0,
  "tasks": [
    {
      "id": "task-id",
      "status_code": 20000,
      "status_message": "Ok.",
      "time": "0.1000 sec.",
      "cost": 0.0103,
      "result_count": 1,
      "path": ["v3", "..."],
      "data": {},
      "result": []
    }
  ]
}
```

Field meanings:

- `version`: provider response version.
- top-level `status_code`/`status_message`: request-level DataForSEO status.
- `time`: provider processing duration string.
- `cost`: total USD cost returned for the request.
- `tasks_count`/`tasks_error`: tasks accepted and tasks with errors.
- task `id`: provider task identifier.
- task status fields: task-level status; validate independently of HTTP and top-level status.
- `result_count`: number of result containers.
- `path`: resolved API path segments.
- `data`: normalized submitted task parameters.
- `result`: endpoint-specific result array.

Reduced `.ai` response commonly has:

```json
{
  "id": "task-id",
  "status_code": 20000,
  "status_message": "Ok.",
  "items": []
}
```

Some tools return `result`, a bare `items` array, or a specially filtered object. Therefore there is no single exact endpoint-specific MCP response schema independent of server configuration. Use the catalog's official documentation URL for field definitions, inspect the actual JSON, and do not require fields removed by `.ai` or field filtering. The supplied Postman collection contains dated full examples and response headers; extract one with `extract_postman_example.py` rather than treating it as current schema.

## Errors and retry handling

DataForSEO usually returns HTTP `200` with an internal status. Exceptions documented by the provider include HTTP `401` Unauthorized, `402` Payment Required, `404` Not Found, and `500` Internal Server Error.

Important internal statuses:

| Code | Meaning | Handling |
| --- | --- | --- |
| `20000` | success | Parse task status and result. |
| `40006` | more than 100 tasks | Split standard REST batches; MCP normally sends one task. |
| `40100` | unauthorized | Fix credentials; no unchanged retry. |
| `40102` | no search results | Report empty coverage; do not fabricate data. |
| `40103` | task execution failed | Retry only with approval and bounded backoff. |
| `40200`, `40210` | payment/balance problem | Stop and resolve billing. |
| `40202` | per-minute rate exceeded | Wait for the next window; lower request rate. |
| `40203` | cost limit exceeded | Stop; change dashboard limit or reduce scope. |
| `40204`, `40207` | subscription/IP access denied | Fix account access or whitelist. |
| `40205`, `40206` | duplicate-task limit | Stop duplicate submissions. |
| `40209` | too many simultaneous queries | Reduce concurrency below 30 and retry later. |
| `40400`-`40408` | resource/task/path/input target missing | Correct the request; only retry after correction. |
| `40501`-`40506` | invalid/unknown fields or excessive intersections | Correct or narrow the payload. |
| `40601`, `40602` | task handed/queued | Poll or await callback only for standard REST tasks. |
| `50000`, `50301`, `50303`, `50304` | internal/temporary service problem | Exponential backoff with jitter; pause 5-10 minutes after repeated failures. |
| `50401` | live task exceeded 120 seconds | Retry once with approval or switch to standard REST if explicitly authorized. |
| `50402` | target page exceeded 50 seconds | Retry later or use a different page. |

MCP authentication errors from the official server include HTTP `401` with `WWW-Authenticate` and:

```json
{"error":"invalid auth","error_description":"invalid auth"}
```

Expired Bearer example:

```json
{"error":"invalid_token","error_description":"expired bearer token"}
```

Retry transient failures with full jitter, for example delays randomly selected from ceilings of 1, 2, 4, and 8 seconds, capped at three retries. Respect `Retry-After` when present. A repeated live call may be billable, so obtain approval before retrying in an analysis workflow.

## Rate limits and timeouts

The authoritative per-endpoint ceiling is the returned `X-RateLimit-Limit` header. Current general guidance:

- General limit: 2,000 API requests per minute.
- Live Google Ads endpoints: 12 requests per minute.
- Live Google Trends: 250 live tasks per minute across all users; standard tasks are recommended for volume.
- User Data: 6 requests per minute; API Status and Errors: 10; Tasks Ready: 20.
- Database-backed Content Analysis, DataForSEO Trends, DataForSEO Labs, Backlinks, AI Optimization, and OnPage allow at most 30 simultaneous requests per user.
- OnPage Instant Pages and Content Parsing Live REST requests allow at most 20 tasks. The MCP tools send one task per call.

Do not assume that the MCP gateway adds capacity. Limit concurrency below the provider ceiling. Use a 120-second client timeout for SERP Live; allow slightly more at the transport layer. OnPage target timeout errors can occur after 50 seconds.

## Pagination and batching

Cataloged list tools use `limit` and `offset` when exposed. The next page starts at `offset + returned_items_count` (or the requested limit when the endpoint returns a full page). Stop when the returned page is shorter than the requested limit or when `offset + items_count >= total_count`. There are no cursor tokens or `next` links in the captured tool contracts.

Every page is another possibly billable MCP call. Deduplicate by the endpoint's stable identifier and retain page provenance.

Batch capabilities are parameter-specific:

- `dataforseo_labs_bulk_keyword_difficulty`: up to 1,000 keywords.
- `dataforseo_labs_google_keyword_overview`: up to 700 keywords, each at most 80 characters and 10 words.
- Other array maxima are stated in their exact catalog declarations.

The cataloged MCP tools are Live/utility calls and generally map one tool call to one REST task. DataForSEO standard `task_post` REST endpoints can accept up to 100 tasks per HTTP request, but they are not exposed by this MCP catalog. Do not imply MCP bulk support beyond an exposed array parameter.

Recommended bulk behavior: chunk at the schema maximum, run conservatively below 30 concurrent requests, checkpoint completed chunks, retry only transient failed chunks, and preserve input order plus a stable key for reassembly.

## Encoding, uploads, and exports

- MCP JSON-RPC and REST JSON are UTF-8.
- REST POST bodies are JSON task arrays; use `Content-Type: application/json`.
- Keywords with `%` or `+` can have endpoint-specific escaping rules documented in the tool description; follow them exactly.
- The 83 captured tools expose no CSV, multipart, binary upload, bulk-import, or asynchronous export endpoint. No MCP-level file-size or chunk-upload contract therefore applies.
- Parse local CSV as UTF-8, normalize it locally, then send JSON arrays within the selected tool's item limits. Never send a file path as if it were uploaded.
- REST can return JSON by default and supports `.xml` on documented endpoints; certain result endpoints support `.html`. MCP returns textual JSON and does not expose a response-format switch.

## Callbacks and webhooks

The captured MCP tools expose live calls and no `pingback_url`, `postback_url`, or callback event registration. Webhooks are therefore not available through these tool contracts.

Underlying standard REST task endpoints can support:

- Pingback: provider sends an HTTP `GET` when a task completes. Use placeholders such as `https://example.com/ping?id=$id&tag=$tag`.
- Postback: provider sends the completed result by gzip-compressed HTTP `POST`. SERP and Merchant standard tasks also require the documented `postback_data` value such as `advanced`.

Example task fragment (outside the MCP catalog):

```json
{
  "keyword": "technical seo audit",
  "tag": "audit-2026-06-21",
  "pingback_url": "https://example.com/ping?id=$id&tag=$tag",
  "postback_url": "https://example.com/result?id=$id&tag=$tag",
  "postback_data": "advanced"
}
```

Validate TLS, authenticate callbacks at your edge, allow only documented DataForSEO source addresses when feasible, enforce body-size limits, decompress gzip safely, validate the task `id`/`tag`, make processing idempotent, and respond within 10 seconds. DataForSEO does not document a signature-verification header for these callbacks; do not invent one. Failed callbacks can be resent without setting and paying for a duplicate task through `POST /v3/appendix/webhook_resend`, up to 100 task IDs.

## Official clients and minimal REST calls

Official repositories exist for Python, C#, TypeScript, and Java. The API documentation also recommends a PHP client and provides simple PHP and Python REST clients. The official MCP server is distributed as `dataforseo-mcp-server` on npm. Prefer the MCP SDK supplied by the host application for tool calls.

Minimal REST examples, using the same one-element body:

```bash
curl --user "$DATAFORSEO_USERNAME:$DATAFORSEO_PASSWORD" \
  -H 'Content-Type: application/json' \
  --data '[{"keywords":["technical seo audit"],"location_name":"United States","language_code":"en"}]' \
  'https://api.dataforseo.com/v3/dataforseo_labs/google/bulk_keyword_difficulty/live'
```

```js
const auth = Buffer.from(`${process.env.DATAFORSEO_USERNAME}:${process.env.DATAFORSEO_PASSWORD}`).toString("base64");
const response = await fetch("https://api.dataforseo.com/v3/dataforseo_labs/google/bulk_keyword_difficulty/live", {
  method: "POST",
  headers: {Authorization: `Basic ${auth}`, "Content-Type": "application/json"},
  body: JSON.stringify([{keywords: ["technical seo audit"], location_name: "United States", language_code: "en"}]),
  signal: AbortSignal.timeout(120_000)
});
if (!response.ok) throw new Error(`HTTP ${response.status}`);
const data = await response.json();
```

```python
import os
import requests

response = requests.post(
    "https://api.dataforseo.com/v3/dataforseo_labs/google/bulk_keyword_difficulty/live",
    auth=(os.environ["DATAFORSEO_USERNAME"], os.environ["DATAFORSEO_PASSWORD"]),
    json=[{"keywords": ["technical seo audit"], "location_name": "United States", "language_code": "en"}],
    timeout=120,
)
response.raise_for_status()
data = response.json()
```

```php
<?php
$body = [[
    "keywords" => ["technical seo audit"],
    "location_name" => "United States",
    "language_code" => "en",
]];
$ch = curl_init("https://api.dataforseo.com/v3/dataforseo_labs/google/bulk_keyword_difficulty/live");
curl_setopt_array($ch, [
    CURLOPT_USERPWD => getenv("DATAFORSEO_USERNAME") . ":" . getenv("DATAFORSEO_PASSWORD"),
    CURLOPT_HTTPHEADER => ["Content-Type: application/json"],
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => json_encode($body),
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 120,
]);
$raw = curl_exec($ch);
if ($raw === false || curl_getinfo($ch, CURLINFO_RESPONSE_CODE) >= 400) {
    throw new RuntimeException(curl_error($ch));
}
$data = json_decode($raw, true, flags: JSON_THROW_ON_ERROR);
?>
```

## Troubleshooting

- Tool missing: inspect `tools/list`; enable the corresponding `ENABLED_MODULES` value and restart the local server. Some clients cap active tools.
- `401` or `40100`: verify the API login/password, Base64 encoding, Bearer expiry, redirect URI, and that authorization is sent on every request.
- `402`: check balance, subscription, daily/endpoint cost limits, and IP whitelist.
- `40402` or HTTP `404`: compare the exact mapped path and dynamic path value; do not append `.ai` manually when calling canonical REST unless that reduced endpoint is intended.
- `40501`, `40503`, `40506`: compare the active tool schema; remove unknown fields and preserve the one-object MCP arguments shape.
- Empty results: distinguish `40102` from a successful response with zero items; verify country/language/location and normalized target.
- Timeouts: use 120 seconds for SERP Live, reduce depth, avoid excessive fan-out, and consider a standard REST workflow only when the user authorizes leaving MCP.
- Large output: request lower limits, filter at the endpoint, or configure field filtering. Never discard identifiers, costs, or fields needed to support the conclusion without noting it.

Primary sources: [DataForSEO MCP setup](https://dataforseo.com/model-context-protocol), [official MCP server](https://github.com/dataforseo/mcp-server-typescript), [API documentation](https://docs.dataforseo.com/v3/), [errors](https://docs.dataforseo.com/v3/appendix/errors/), [rate limits](https://dataforseo.com/help-center/rate-limits-and-request-limits), and [MCP specification](https://modelcontextprotocol.io/specification/2025-06-18/).
