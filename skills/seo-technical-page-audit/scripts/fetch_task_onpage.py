#!/usr/bin/env python3
"""Fetch a one-page DataForSEO OnPage task and its detailed endpoint results."""

from __future__ import annotations

import argparse
import base64
import json
import re
import sys
import time
from pathlib import Path
from typing import Any
from urllib import error, parse, request


API_BASE = "https://api.dataforseo.com/v3/on_page"
PENDING_CODES = {40601, 40602}
DEVICE_PRESETS = ("desktop", "mobile")


class AuditError(RuntimeError):
    pass


class EnvFileRequired(AuditError):
    pass


def absolute_page_url(value: str) -> str:
    parsed = parse.urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise argparse.ArgumentTypeError("URL must be an absolute HTTP(S) URL")
    if parsed.username or parsed.password:
        raise argparse.ArgumentTypeError("URL must not contain credentials")
    return value


def result_limit(value: str) -> int:
    parsed = int(value)
    if not 1 <= parsed <= 1000:
        raise argparse.ArgumentTypeError("result limit must be between 1 and 1000")
    return parsed


def env_value(value: str) -> str:
    value = value.strip()
    if not (len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}):
        value = re.sub(r"\s+#.*$", "", value).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def credentials_from_env_file(path: Path) -> tuple[str, str]:
    if not path.is_file():
        raise EnvFileRequired(
            f"credential file not found: {path}; provide its path with --env-file"
        )
    values: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise AuditError(f"cannot read credential file {path}: {exc}") from exc

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("export "):
            stripped = stripped[7:].lstrip()
        if "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        if key in {"DATAFORSEO_USERNAME", "DATAFORSEO_LOGIN", "DATAFORSEO_PASSWORD"}:
            values[key] = env_value(value)

    username = values.get("DATAFORSEO_USERNAME") or values.get("DATAFORSEO_LOGIN")
    password = values.get("DATAFORSEO_PASSWORD")
    if not username or not password:
        raise AuditError(
            f"credential file {path} must define DATAFORSEO_USERNAME "
            "(or DATAFORSEO_LOGIN) and DATAFORSEO_PASSWORD"
        )
    return username, password


class DataForSEOClient:
    def __init__(self, username: str, password: str, request_timeout: float) -> None:
        token = base64.b64encode(f"{username}:{password}".encode()).decode()
        self.headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
            "User-Agent": "dataforseo-skills/seo-technical-page-audit",
        }
        self.request_timeout = request_timeout

    def call(self, method: str, path: str, payload: Any | None = None) -> dict[str, Any]:
        body = None if payload is None else json.dumps(payload).encode()
        api_request = request.Request(
            f"{API_BASE}/{path}", data=body, headers=self.headers, method=method
        )
        try:
            with request.urlopen(api_request, timeout=self.request_timeout) as response:
                result = json.load(response)
        except error.HTTPError as exc:
            raise AuditError(f"DataForSEO HTTP error {exc.code} for {path}") from exc
        except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise AuditError(f"DataForSEO request failed for {path}: {exc}") from exc

        if result.get("status_code") != 20000:
            raise AuditError(
                f"DataForSEO error for {path}: {result.get('status_code')} "
                f"{result.get('status_message', 'Unknown error')}"
            )
        return result


def first_task(response: dict[str, Any], endpoint: str) -> dict[str, Any]:
    tasks = response.get("tasks") or []
    if not tasks:
        raise AuditError(f"DataForSEO returned no task for {endpoint}")
    task = tasks[0]
    code = task.get("status_code")
    if code not in {20000, 20100, *PENDING_CODES}:
        raise AuditError(
            f"DataForSEO task error for {endpoint}: {code} "
            f"{task.get('status_message', 'Unknown error')}"
        )
    return task


def crawl_finished(summary: dict[str, Any]) -> bool:
    task = first_task(summary, "summary")
    if task.get("status_code") in PENDING_CODES:
        return False
    results = task.get("result") or []
    return bool(results and results[0].get("crawl_progress") == "finished")


def checked_call(
    client: DataForSEOClient, method: str, path: str, payload: Any | None = None
) -> dict[str, Any]:
    response = client.call(method, path, payload)
    first_task(response, path)
    return response


def crawled_page_url(pages: dict[str, Any], fallback: str) -> str:
    task = first_task(pages, "pages")
    results = task.get("result") or []
    items = results[0].get("items") or [] if results else []
    return items[0].get("url") or fallback if items else fallback


def task_result(response: dict[str, Any], endpoint: str) -> dict[str, Any]:
    task = first_task(response, endpoint)
    results = task.get("result") or []
    return results[0] if results else {}


def result_items(result: dict[str, Any]) -> list[dict[str, Any]]:
    items = result.get("items")
    return items if isinstance(items, list) else []


def truncated_inventory(result: dict[str, Any]) -> bool:
    returned = result.get("items_count")
    total = result.get("total_items_count")
    return isinstance(returned, int) and isinstance(total, int) and total > returned


def normalize_summary(
    audited_url: str,
    effective_url: str,
    accept_language: str,
    endpoints: dict[str, dict[str, Any]],
    device: str = "desktop",
) -> dict[str, Any]:
    pages_result = task_result(endpoints["pages"], "pages")
    page_items = result_items(pages_result)
    page = page_items[0] if page_items else {}

    links_result = task_result(endpoints["links"], "links")
    link_items = result_items(links_result)

    resources_result = task_result(endpoints["resources"], "resources")
    resource_items = result_items(resources_result)

    redirect_result = task_result(endpoints["redirect_chains"], "redirect_chains")
    redirect_items = result_items(redirect_result)

    non_indexable_result = task_result(endpoints["non_indexable"], "non_indexable")
    non_indexable_items = result_items(non_indexable_result)

    waterfall_result = task_result(endpoints["waterfall"], "waterfall")
    waterfall_items = result_items(waterfall_result)
    waterfall_group = waterfall_items[0] if waterfall_items else {}
    waterfall_resources = result_items({"items": waterfall_group.get("resources")})
    waterfall_page_url = waterfall_group.get("page_url")

    microdata_result = task_result(endpoints["microdata"], "microdata")

    inventories = {
        "links": links_result,
        "redirect_chains": redirect_result,
        "non_indexable": non_indexable_result,
        "resources": resources_result,
        "waterfall": waterfall_result,
        "microdata": microdata_result,
    }

    return {
        "accept_language_used": accept_language,
        "audited_url": audited_url,
        "device": device,
        "effective_url": effective_url,
        "page_timing_source": "pages.page_timing",
        "page_status_code": page.get("status_code"),
        "onpage_score": page.get("onpage_score"),
        "broken_link_urls": [
            item.get("link_to")
            for item in link_items
            if item.get("is_broken") and item.get("link_to")
        ],
        "broken_resource_urls": [
            item.get("url")
            for item in resource_items
            if item.get("checks", {}).get("is_broken") and item.get("url")
        ],
        "non_indexable_urls": [
            item.get("url") for item in non_indexable_items if item.get("url")
        ],
        "valid_hreflang_targets": [
            item.get("link_to")
            for item in link_items
            if item.get("is_valid_hreflang") and item.get("link_to")
        ],
        "render_blocking_resource_urls": [
            item.get("url")
            for item in waterfall_resources
            if item.get("is_render_blocking") and item.get("url")
        ],
        "inventory_counts": {
            name: {
                "returned": result.get("items_count"),
                "total": result.get("total_items_count"),
            }
            for name, result in inventories.items()
        },
        "truncated_inventories": [
            name for name, result in inventories.items() if truncated_inventory(result)
        ],
        "waterfall_page_url": waterfall_page_url,
        "waterfall_page_url_anomaly": bool(
            waterfall_page_url and waterfall_page_url != effective_url
        ),
        "microdata_summary": microdata_result.get("test_summary"),
    }


def build_task_payload(
    target: str, url: str, accept_language: str, device: str
) -> dict[str, Any]:
    if device not in DEVICE_PRESETS:
        raise AuditError(f"unsupported device preset: {device}")
    return {
        "target": target,
        "start_url": url,
        "max_crawl_pages": 1,
        "force_sitewide_checks": True,
        "load_resources": True,
        "enable_javascript": True,
        # DataForSEO currently rejects browser_preset unless browser rendering
        # is enabled explicitly, even when enable_javascript is already true.
        "enable_browser_rendering": True,
        # Suppress consent overlays so rendered audits are less likely to be
        # dominated by cookie popups instead of the page itself.
        "disable_cookie_popup": True,
        "accept_language": accept_language,
        "validate_micromarkup": True,
        "browser_preset": device,
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    env_file = Path(args.env_file).expanduser() if args.env_file else Path.cwd() / ".env"
    username, password = credentials_from_env_file(env_file.resolve())

    parsed = parse.urlsplit(args.url)
    target = (parsed.hostname or "").lower().rstrip(".")
    if target.startswith("www."):
        target = target[4:]
    accept_language = args.accept_language or "en-US"

    client = DataForSEOClient(username, password, args.request_timeout)
    task_payload = build_task_payload(target, args.url, accept_language, args.device)

    task_post = checked_call(
        client,
        "POST",
        "task_post",
        [task_payload],
    )
    task_id = first_task(task_post, "task_post").get("id")
    if not task_id:
        raise AuditError("DataForSEO task_post returned no task ID")

    deadline = time.monotonic() + args.poll_timeout
    while True:
        summary = client.call("GET", f"summary/{task_id}")
        if crawl_finished(summary):
            break
        if time.monotonic() >= deadline:
            raise AuditError(f"crawl {task_id} did not finish within {args.poll_timeout}s")
        time.sleep(args.poll_interval)

    common = {"id": task_id, "limit": args.result_limit}
    pages = checked_call(client, "POST", "pages", [common])
    effective_url = crawled_page_url(pages, args.url)
    endpoints = {
        "task_post": task_post,
        "summary": summary,
        "pages": pages,
        "links": checked_call(client, "POST", "links", [common]),
        "redirect_chains": checked_call(
            client, "POST", "redirect_chains", [{**common, "url": args.url}]
        ),
        "non_indexable": checked_call(client, "POST", "non_indexable", [common]),
        "resources": checked_call(
            client, "POST", "resources", [{**common, "url": effective_url}]
        ),
        "waterfall": checked_call(
            client, "POST", "waterfall", [{"id": task_id, "url": effective_url}]
        ),
        "microdata": checked_call(
            client, "POST", "microdata", [{"id": task_id, "url": effective_url}]
        ),
    }
    costs = {name: response.get("cost") for name, response in endpoints.items()}
    known_costs = [cost for cost in costs.values() if isinstance(cost, (int, float))]
    normalized = normalize_summary(
        args.url, effective_url, accept_language, endpoints, args.device
    )

    return {
        "schema_version": 1,
        "status": "complete",
        "device": args.device,
        "task_id": task_id,
        "audited_url": args.url,
        "crawled_page_url": effective_url,
        "normalized": normalized,
        "costs_usd": costs,
        "known_cost_total_usd": sum(known_costs),
        "endpoints": endpoints,
    }


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(
        description="Run a one-page DataForSEO OnPage task and print all results as JSON."
    )
    cli.add_argument("url", type=absolute_page_url)
    cli.add_argument(
        "--env-file",
        help="credential file path; defaults to .env in the current project root",
    )
    cli.add_argument(
        "--accept-language",
        help="Accept-Language header for crawling; defaults to en-US",
    )
    cli.add_argument(
        "--device",
        choices=DEVICE_PRESETS,
        default="desktop",
        help="browser preset to audit; defaults to desktop",
    )
    cli.add_argument("--poll-timeout", type=float, default=180.0)
    cli.add_argument("--poll-interval", type=float, default=5.0)
    cli.add_argument("--request-timeout", type=float, default=60.0)
    cli.add_argument("--result-limit", type=result_limit, default=1000)
    return cli


def main() -> int:
    try:
        args = parser().parse_args()
        if args.poll_timeout <= 0 or args.poll_interval <= 0 or args.request_timeout <= 0:
            raise AuditError("timeouts and poll interval must be positive")
        json.dump(run(args), sys.stdout, ensure_ascii=True)
        sys.stdout.write("\n")
        return 0
    except EnvFileRequired as exc:
        json.dump(
            {"status": "env_file_required", "message": str(exc)},
            sys.stderr,
            ensure_ascii=True,
        )
        sys.stderr.write("\n")
        return 2
    except (AuditError, OSError) as exc:
        json.dump({"status": "error", "message": str(exc)}, sys.stderr, ensure_ascii=True)
        sys.stderr.write("\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
