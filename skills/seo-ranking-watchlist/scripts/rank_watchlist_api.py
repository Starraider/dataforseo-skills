#!/usr/bin/env python3
"""Retrieve DataForSEO ranks and atomically maintain a ranking watchlist."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import uuid
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable
from urllib import error, parse, request


API_BASE = "https://api.dataforseo.com/v3"
LABS_PATH = "dataforseo_labs/google/ranked_keywords/live"
SERP_PATH = "serp/google/organic/live/advanced"
NO_SEARCH_RESULTS_CODE = 40102
DEFAULT_SCOPE = {
    "location_name": "United States",
    "language_code": "en",
    "device": "desktop",
    "depth": 100,
}


class WatchlistError(RuntimeError):
    def __init__(self, message: str, *, fallback_safe: bool = False) -> None:
        super().__init__(message)
        self.fallback_safe = fallback_safe


class ScriptUnavailable(WatchlistError):
    def __init__(self, message: str) -> None:
        super().__init__(message, fallback_safe=True)


class PartialRunError(WatchlistError):
    def __init__(self, message: str, run_file: Path) -> None:
        super().__init__(message)
        self.run_file = run_file


def normalize_domain(value: str) -> str:
    candidate = value.strip().lower().rstrip(".")
    parsed = parse.urlsplit(f"//{candidate}")
    try:
        port = parsed.port
    except ValueError as exc:
        raise argparse.ArgumentTypeError("domain contains an invalid port") from exc
    if (
        not parsed.hostname
        or parsed.username
        or parsed.password
        or port
        or parsed.path not in {"", "/"}
        or parsed.query
        or parsed.fragment
    ):
        raise argparse.ArgumentTypeError("domain must be a bare hostname")
    domain = parsed.hostname.rstrip(".")
    if domain.startswith("www."):
        domain = domain[4:]
    if not re.fullmatch(r"(?=.{1,253}$)[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", domain):
        raise argparse.ArgumentTypeError("domain contains unsupported characters")
    if "." not in domain or any(
        not label or len(label) > 63 for label in domain.split(".")
    ):
        raise argparse.ArgumentTypeError("domain must be a valid hostname")
    return domain


def bounded_int(minimum: int, maximum: int):
    def parse_value(value: str) -> int:
        number = int(value)
        if not minimum <= number <= maximum:
            raise argparse.ArgumentTypeError(
                f"value must be between {minimum} and {maximum}"
            )
        return number

    return parse_value


def normalize_keyword(value: str) -> str:
    keyword = " ".join(value.split())
    if not keyword or len(keyword) > 80 or len(keyword.split()) > 10:
        raise WatchlistError(
            "keywords must contain 1-80 characters and no more than 10 words"
        )
    return keyword


def ordered_keywords(groups: Iterable[Iterable[str]]) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    for group in groups:
        for raw in group:
            keyword = normalize_keyword(raw)
            key = keyword.casefold()
            if key not in seen:
                seen.add(key)
                values.append(keyword)
    return values


def env_value(value: str) -> str:
    value = value.strip()
    if not (len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}):
        value = re.sub(r"\s+#.*$", "", value).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def credentials(env_file: str | None) -> tuple[str, str]:
    username = os.environ.get("DATAFORSEO_USERNAME") or os.environ.get(
        "DATAFORSEO_LOGIN"
    )
    password = os.environ.get("DATAFORSEO_PASSWORD")
    if username and password:
        return username, password

    path = Path(env_file).expanduser() if env_file else Path.cwd() / ".env"
    if not path.is_file():
        raise ScriptUnavailable(
            "DataForSEO credentials are unavailable; set DATAFORSEO_USERNAME "
            "(or DATAFORSEO_LOGIN) and DATAFORSEO_PASSWORD, or provide --env-file"
        )
    values: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ScriptUnavailable(f"cannot read credential file {path}: {exc}") from exc
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
        if key in {
            "DATAFORSEO_USERNAME",
            "DATAFORSEO_LOGIN",
            "DATAFORSEO_PASSWORD",
        }:
            values[key] = env_value(value)
    username = values.get("DATAFORSEO_USERNAME") or values.get("DATAFORSEO_LOGIN")
    password = values.get("DATAFORSEO_PASSWORD")
    if not username or not password:
        raise ScriptUnavailable(
            f"credential file {path} must define DATAFORSEO_USERNAME "
            "(or DATAFORSEO_LOGIN) and DATAFORSEO_PASSWORD"
        )
    return username, password


class DataForSEOClient:
    def __init__(self, username: str, password: str, timeout: float) -> None:
        token = base64.b64encode(f"{username}:{password}".encode()).decode()
        self.headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
            "User-Agent": "dataforseo-skills/seo-ranking-watchlist",
        }
        self.timeout = timeout

    def post(self, path: str, task: dict[str, Any]) -> dict[str, Any]:
        api_request = request.Request(
            f"{API_BASE}/{path}",
            data=json.dumps([task]).encode(),
            headers=self.headers,
            method="POST",
        )
        try:
            with request.urlopen(api_request, timeout=self.timeout) as response:
                payload = json.load(response)
        except error.HTTPError as exc:
            raise WatchlistError(
                f"DataForSEO HTTP error {exc.code} for {path}"
            ) from exc
        except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise WatchlistError(f"DataForSEO request failed for {path}: {exc}") from exc
        return checked_task(payload, path)


def checked_task(payload: dict[str, Any], endpoint: str) -> dict[str, Any]:
    if payload.get("status_code") != 20000:
        raise WatchlistError(
            f"DataForSEO error for {endpoint}: {payload.get('status_code')} "
            f"{payload.get('status_message', 'Unknown error')}"
        )
    tasks = payload.get("tasks") or []
    if not tasks:
        raise WatchlistError(f"DataForSEO returned no task for {endpoint}")
    task = tasks[0]
    if endpoint == SERP_PATH and task.get("status_code") == NO_SEARCH_RESULTS_CODE:
        return task
    if task.get("status_code") != 20000:
        raise WatchlistError(
            f"DataForSEO task error for {endpoint}: {task.get('status_code')} "
            f"{task.get('status_message', 'Unknown error')}"
        )
    return task


def first_result(task: dict[str, Any], endpoint: str, *, required: bool) -> dict[str, Any]:
    results = task.get("result") or []
    if not results:
        if required:
            raise WatchlistError(f"DataForSEO returned no result object for {endpoint}")
        return {}
    return results[0]


def build_discovery_payload(
    domain: str, location_name: str, language_code: str, limit: int
) -> dict[str, Any]:
    return {
        "target": domain,
        "location_name": location_name,
        "language_code": language_code,
        "item_types": ["organic"],
        "historical_serp_mode": "live",
        "limit": limit,
        "order_by": [
            "keyword_data.keyword_info.search_volume,desc",
            "ranked_serp_element.serp_item.rank_group,asc",
        ],
    }


def normalize_discovery(task: dict[str, Any]) -> list[dict[str, Any]]:
    result = first_result(task, LABS_PATH, required=False)
    records = []
    for item in result.get("items") or []:
        keyword_data = item.get("keyword_data") or {}
        serp_item = (item.get("ranked_serp_element") or {}).get("serp_item") or {}
        keyword = keyword_data.get("keyword")
        if not isinstance(keyword, str) or not keyword.strip():
            continue
        records.append(
            {
                "keyword": " ".join(keyword.split()),
                "labs_position": serp_item.get("rank_group"),
                "search_volume": (keyword_data.get("keyword_info") or {}).get(
                    "search_volume"
                ),
                "url": serp_item.get("url"),
            }
        )
    return records


def build_serp_payload(
    domain: str,
    keyword: str,
    location_name: str,
    language_code: str,
    device: str,
    depth: int,
) -> dict[str, Any]:
    return {
        "keyword": keyword,
        "location_name": location_name,
        "language_code": language_code,
        "device": device,
        "depth": depth,
        "target": f"*{domain}*",
        "stop_crawl_on_match": [
            {"match_value": domain, "match_type": "with_subdomains"}
        ],
        "find_targets_in": ["organic"],
    }


def item_domain(item: dict[str, Any]) -> str:
    value = item.get("domain")
    if not value and item.get("url"):
        value = parse.urlsplit(item["url"]).hostname
    domain = str(value or "").lower().rstrip(".")
    return domain[4:] if domain.startswith("www.") else domain


def normalize_serp(
    task: dict[str, Any], keyword: str, domain: str, depth: int
) -> dict[str, Any]:
    if task.get("status_code") == NO_SEARCH_RESULTS_CODE:
        return {
            "keyword": keyword,
            "position": None,
            "url": None,
            "checked_at": None,
            "cost_usd": task.get("cost"),
        }
    result = first_result(task, SERP_PATH, required=True)
    matches = []
    for item in result.get("items") or []:
        candidate = item_domain(item)
        rank = item.get("rank_group")
        if (
            item.get("type") == "organic"
            and (candidate == domain or candidate.endswith(f".{domain}"))
            and isinstance(rank, int)
            and 1 <= rank <= depth
        ):
            matches.append(item)
    best = min(matches, key=lambda item: item["rank_group"]) if matches else None
    return {
        "keyword": keyword,
        "position": best["rank_group"] if best else None,
        "url": best.get("url") if best else None,
        "checked_at": result.get("datetime"),
        "cost_usd": task.get("cost"),
    }


def is_no_search_results_error(message: Any) -> bool:
    return isinstance(message, str) and (
        f"{NO_SEARCH_RESULTS_CODE} No Search Results" in message
    )


def null_position_result(keyword: str) -> dict[str, Any]:
    return {
        "keyword": keyword,
        "position": None,
        "url": None,
        "checked_at": None,
        "cost_usd": None,
    }


def coerce_no_search_results(manifest: dict[str, Any]) -> None:
    errors = manifest.get("errors") or {}
    if not isinstance(errors, dict):
        return
    for keyword, message in list(errors.items()):
        if is_no_search_results_error(message):
            manifest.setdefault("results", {})[keyword] = null_position_result(keyword)
            manifest.setdefault("costs_usd", {}).setdefault("serp", {})[keyword] = None
            del errors[keyword]


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp")
    try:
        with temporary.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=True, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_flag = getattr(os, "O_DIRECTORY", 0)
        directory_fd = os.open(path.parent, os.O_RDONLY | directory_flag)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()


def read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WatchlistError(f"cannot read {label} {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise WatchlistError(f"{label} {path} must contain a JSON object")
    return payload


def load_watchlist(path: Path, *, required: bool = False) -> dict[str, Any]:
    if not path.exists():
        if required:
            raise WatchlistError(f"watchlist not found: {path}")
        return {"domains": {}}
    payload = read_json(path, "watchlist")
    if not isinstance(payload.get("domains"), dict):
        raise WatchlistError(f"watchlist {path} must contain a domains object")
    return payload


def file_digest(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        raise WatchlistError(f"cannot hash watchlist {path}: {exc}") from exc


def watchlist_path(value: str | None, domain: str) -> Path:
    if value:
        return Path(value).expanduser().resolve()
    return (Path.cwd() / "SEO" / domain / "watchlist.json").resolve()


def run_path(value: str | None, watchlist: Path) -> Path:
    if value:
        return Path(value).expanduser().resolve()
    timestamp = datetime.now().astimezone().strftime("%Y%m%dT%H%M%S%z")
    name = f"{timestamp}_{uuid.uuid4().hex[:8]}.json"
    return watchlist.parent / ".watchlist-runs" / name


def current_timestamp() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def current_date() -> str:
    return datetime.now().astimezone().date().isoformat()


def existing_entry(payload: dict[str, Any], domain: str) -> dict[str, Any] | None:
    entry = payload.get("domains", {}).get(domain)
    if entry is not None and not isinstance(entry, dict):
        raise WatchlistError(f"watchlist entry for {domain} must be an object")
    return entry


def entry_keywords(entry: dict[str, Any] | None) -> list[str]:
    if not entry:
        return []
    keywords = entry.get("keywords")
    if not isinstance(keywords, list) or not all(
        isinstance(keyword, str) for keyword in keywords
    ):
        raise WatchlistError("existing watchlist keywords must be a string array")
    return ordered_keywords([keywords])


def entry_history(entry: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not entry:
        return []
    history = entry.get("history")
    if not isinstance(history, list) or not all(
        isinstance(snapshot, dict) for snapshot in history
    ):
        raise WatchlistError("existing watchlist history must be an object array")
    return list(history)


def selected_scope(args: argparse.Namespace, entry: dict[str, Any] | None) -> dict[str, Any]:
    stored = entry.get("scope") if entry else None
    if stored is not None and not isinstance(stored, dict):
        raise WatchlistError("existing watchlist scope must be an object")
    scope = dict(stored or DEFAULT_SCOPE)
    for field in ("location_name", "language_code", "device", "depth"):
        value = getattr(args, field, None)
        if value is not None:
            scope[field] = value
    if scope.get("device") not in {"desktop", "mobile"}:
        raise WatchlistError("scope device must be desktop or mobile")
    if not isinstance(scope.get("depth"), int) or not 10 <= scope["depth"] <= 100:
        raise WatchlistError("scope depth must be between 10 and 100")
    if not scope.get("location_name") or not scope.get("language_code"):
        raise WatchlistError("scope location and language must not be empty")
    if stored and scope != stored:
        history = entry_history(entry)
        if args.command == "check":
            raise WatchlistError("check scope must exactly match the saved scope")
        if history and not args.reset_scope:
            raise WatchlistError(
                "scope differs from saved history; rerun add with --reset-scope"
            )
    return scope


def new_manifest(
    args: argparse.Namespace,
    operation: str,
    scope: dict[str, Any],
    watchlist: Path,
    run_file: Path,
    entry: dict[str, Any] | None,
) -> dict[str, Any]:
    timestamp = current_timestamp()
    return {
        "schema_version": 1,
        "run_id": run_file.stem,
        "status": "discovering" if operation == "add" else "checking",
        "operation": operation,
        "domain": args.domain,
        "label": args.label or (entry or {}).get("label") or args.domain,
        "scope": scope,
        "watchlist_path": str(watchlist),
        "watchlist_sha256": file_digest(watchlist),
        "reset_scope": bool(getattr(args, "reset_scope", False)),
        "commit_requested": bool(args.commit),
        "keywords": [],
        "discovered": [],
        "results": {},
        "errors": {},
        "costs_usd": {"discovery": None, "serp": {}},
        "snapshot_date": current_date(),
        "created_at": timestamp,
        "updated_at": timestamp,
    }


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    manifest["updated_at"] = current_timestamp()
    atomic_write_json(path, manifest)


def check_one(
    client: DataForSEOClient,
    domain: str,
    keyword: str,
    scope: dict[str, Any],
) -> dict[str, Any]:
    task = client.post(
        SERP_PATH,
        build_serp_payload(
            domain,
            keyword,
            scope["location_name"],
            scope["language_code"],
            scope["device"],
            scope["depth"],
        ),
    )
    return normalize_serp(task, keyword, domain, scope["depth"])


def check_all(
    client: DataForSEOClient,
    manifest: dict[str, Any],
    run_file: Path,
    workers: int,
) -> None:
    coerce_no_search_results(manifest)
    missing = [
        keyword
        for keyword in manifest["keywords"]
        if keyword not in manifest.get("results", {})
    ]
    if not missing:
        return
    manifest["status"] = "checking"
    for keyword in missing:
        manifest.setdefault("errors", {}).pop(keyword, None)
    write_manifest(run_file, manifest)

    future_keywords: dict[Future[dict[str, Any]], str] = {}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        for keyword in missing:
            future = executor.submit(
                check_one,
                client,
                manifest["domain"],
                keyword,
                manifest["scope"],
            )
            future_keywords[future] = keyword
        for future in as_completed(future_keywords):
            keyword = future_keywords[future]
            try:
                result = future.result()
                manifest["results"][keyword] = result
                manifest["costs_usd"]["serp"][keyword] = result.get("cost_usd")
            except Exception as exc:  # Preserve every other paid result before failing.
                manifest["errors"][keyword] = str(exc)
            write_manifest(run_file, manifest)

    if manifest["errors"]:
        manifest["status"] = "partial"
        write_manifest(run_file, manifest)
        raise PartialRunError(
            f"{len(manifest['errors'])} live checks failed; resume only missing checks",
            run_file,
        )


def snapshot_from_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    rankings = []
    for keyword in manifest["keywords"]:
        result = manifest.get("results", {}).get(keyword)
        if not isinstance(result, dict):
            raise WatchlistError(f"run has no completed result for {keyword!r}")
        position = result.get("position")
        if position is not None and (
            not isinstance(position, int)
            or not 1 <= position <= manifest["scope"]["depth"]
        ):
            raise WatchlistError(f"run has invalid position for {keyword!r}")
        rankings.append({"keyword": keyword, "position": position})
    return {"date": manifest["snapshot_date"], "rankings": rankings}


def snapshot_already_committed(
    entry: dict[str, Any] | None,
    manifest: dict[str, Any],
    snapshot: dict[str, Any],
) -> bool:
    if not entry or entry.get("scope") != manifest["scope"]:
        return False
    if entry.get("keywords") != manifest["keywords"]:
        return False
    history = entry_history(entry)
    return bool(history and history[-1] == snapshot)


def commit_manifest(manifest: dict[str, Any], run_file: Path) -> Path:
    if manifest.get("errors"):
        raise WatchlistError("cannot commit a run containing failed checks")
    watchlist = Path(manifest["watchlist_path"])
    snapshot = snapshot_from_manifest(manifest)
    payload = load_watchlist(watchlist)
    entry = existing_entry(payload, manifest["domain"])
    current_hash = file_digest(watchlist)
    expected_hash = manifest.get("watchlist_sha256")
    if current_hash != expected_hash:
        if snapshot_already_committed(entry, manifest, snapshot):
            manifest["status"] = "committed"
            manifest["committed_at"] = current_timestamp()
            write_manifest(run_file, manifest)
            return watchlist
        raise WatchlistError(
            "watchlist changed during the run; refusing to overwrite newer data"
        )

    updated_entry = dict(entry or {})
    history = [] if manifest.get("reset_scope") else entry_history(entry)
    history.append(snapshot)
    updated_entry.update(
        {
            "label": manifest["label"],
            "scope": manifest["scope"],
            "keywords": manifest["keywords"],
            "history": history,
        }
    )
    updated_payload = dict(payload)
    domains = dict(payload.get("domains") or {})
    domains[manifest["domain"]] = updated_entry
    updated_payload["domains"] = domains
    atomic_write_json(watchlist, updated_payload)
    manifest["status"] = "committed"
    manifest["committed_at"] = current_timestamp()
    write_manifest(run_file, manifest)
    return watchlist


def known_cost_total(manifest: dict[str, Any]) -> float:
    values = [manifest.get("costs_usd", {}).get("discovery")]
    values.extend((manifest.get("costs_usd", {}).get("serp") or {}).values())
    return sum(value for value in values if isinstance(value, (int, float)))


def summary(manifest: dict[str, Any], run_file: Path) -> dict[str, Any]:
    results = manifest.get("results") or {}
    positions = [
        result.get("position")
        for result in results.values()
        if isinstance(result, dict)
    ]
    return {
        "schema_version": 1,
        "status": manifest["status"],
        "operation": manifest["operation"],
        "source": "dataforseo_api",
        "watchlist_path": manifest["watchlist_path"],
        "run_file": str(run_file),
        "keyword_count": len(manifest.get("keywords") or []),
        "completed_checks": len(results),
        "numeric_positions": sum(isinstance(position, int) for position in positions),
        "not_found_within_depth": sum(position is None for position in positions),
        "opportunities_11_20": sum(
            isinstance(position, int) and 11 <= position <= 20
            for position in positions
        ),
        "failed_checks": len(manifest.get("errors") or {}),
        "known_cost_total_usd": known_cost_total(manifest),
        "snapshot_date": manifest["snapshot_date"],
    }


def prepare_run(args: argparse.Namespace) -> tuple[dict[str, Any], Path]:
    target_watchlist = watchlist_path(args.watchlist, args.domain)
    payload = load_watchlist(target_watchlist, required=args.command == "check")
    entry = existing_entry(payload, args.domain)
    if args.command == "check" and not entry:
        raise WatchlistError(f"domain is not saved in {target_watchlist}")
    scope = selected_scope(args, entry)
    target_run = run_path(args.run_file, target_watchlist)
    manifest = new_manifest(
        args, args.command, scope, target_watchlist, target_run, entry
    )
    supplied = ordered_keywords([args.keyword or []])
    existing = entry_keywords(entry)
    if args.command == "check":
        if supplied:
            raise WatchlistError("check uses only the exact saved keyword list")
        if not existing:
            raise WatchlistError("saved watchlist keyword list is empty")
        manifest["keywords"] = existing
    else:
        manifest["supplied_keywords"] = supplied
        manifest["existing_keywords"] = existing
    write_manifest(target_run, manifest)
    return manifest, target_run


def run_new(args: argparse.Namespace) -> tuple[dict[str, Any], Path]:
    manifest, run_file = prepare_run(args)
    username, password = credentials(args.env_file)
    client = DataForSEOClient(username, password, args.request_timeout)
    if args.command == "add":
        try:
            task = client.post(
                LABS_PATH,
                build_discovery_payload(
                    args.domain,
                    manifest["scope"]["location_name"],
                    manifest["scope"]["language_code"],
                    args.limit,
                ),
            )
            discovered = normalize_discovery(task)
            manifest["discovered"] = discovered
            manifest["costs_usd"]["discovery"] = task.get("cost")
            manifest["keywords"] = ordered_keywords(
                [
                    manifest.pop("supplied_keywords"),
                    manifest.pop("existing_keywords"),
                    [record["keyword"] for record in discovered],
                ]
            )
            if not manifest["keywords"]:
                raise WatchlistError("discovery and supplied keyword lists are empty")
            write_manifest(run_file, manifest)
        except Exception as exc:
            manifest["status"] = "failed"
            manifest["failure"] = str(exc)
            write_manifest(run_file, manifest)
            raise PartialRunError(str(exc), run_file) from exc

    check_all(client, manifest, run_file, args.workers)
    manifest["status"] = "complete"
    write_manifest(run_file, manifest)
    if args.commit:
        commit_manifest(manifest, run_file)
    return manifest, run_file


def run_resume(args: argparse.Namespace) -> tuple[dict[str, Any], Path]:
    run_file = Path(args.run_file).expanduser().resolve()
    manifest = read_json(run_file, "run file")
    if manifest.get("schema_version") != 1:
        raise WatchlistError("unsupported run file schema")
    if manifest.get("status") == "committed":
        return manifest, run_file
    if not manifest.get("keywords"):
        raise WatchlistError(
            "run stopped before keyword discovery completed; a new discovery call "
            "requires explicit approval"
        )
    username, password = credentials(args.env_file)
    client = DataForSEOClient(username, password, args.request_timeout)
    check_all(client, manifest, run_file, args.workers)
    manifest["status"] = "complete"
    write_manifest(run_file, manifest)
    if args.commit or manifest.get("commit_requested"):
        commit_manifest(manifest, run_file)
    return manifest, run_file


def add_scope_arguments(cli: argparse.ArgumentParser) -> None:
    cli.add_argument("--location-name")
    cli.add_argument("--language-code")
    cli.add_argument("--device", choices=("desktop", "mobile"))
    cli.add_argument("--depth", type=bounded_int(10, 100))


def add_run_arguments(cli: argparse.ArgumentParser) -> None:
    cli.add_argument("domain", type=normalize_domain)
    add_scope_arguments(cli)
    cli.add_argument("--keyword", action="append", help="explicit keyword; repeatable")
    cli.add_argument("--label")
    cli.add_argument("--watchlist", help="canonical watchlist path")
    cli.add_argument("--run-file", help="durable run-manifest path")
    cli.add_argument("--commit", action="store_true", help="atomically update watchlist")
    cli.add_argument("--env-file", help="credential file; defaults to environment or ./.env")
    cli.add_argument("--request-timeout", type=float, default=120.0)
    cli.add_argument("--workers", type=bounded_int(1, 10), default=5)


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(
        description="Retrieve DataForSEO ranks and atomically maintain a watchlist."
    )
    subparsers = cli.add_subparsers(dest="command", required=True)
    preflight = subparsers.add_parser("preflight", help="validate local credentials")
    preflight.add_argument("--env-file")

    add = subparsers.add_parser("add", help="discover keywords and check live ranks")
    add_run_arguments(add)
    add.add_argument("--limit", type=bounded_int(1, 100), default=100)
    add.add_argument("--reset-scope", action="store_true")

    check = subparsers.add_parser("check", help="check exact saved keywords")
    add_run_arguments(check)
    check.set_defaults(reset_scope=False)

    resume = subparsers.add_parser("resume", help="resume missing checks from a run file")
    resume.add_argument("run_file")
    resume.add_argument("--commit", action="store_true")
    resume.add_argument("--env-file")
    resume.add_argument("--request-timeout", type=float, default=120.0)
    resume.add_argument("--workers", type=bounded_int(1, 10), default=5)
    return cli


def main() -> int:
    try:
        args = parser().parse_args()
        if args.command == "preflight":
            credentials(args.env_file)
            output = {"schema_version": 1, "status": "complete", "billable_calls": 0}
        else:
            if args.request_timeout <= 0:
                raise WatchlistError("request timeout must be positive")
            if args.command == "resume":
                manifest, run_file = run_resume(args)
            else:
                manifest, run_file = run_new(args)
            output = summary(manifest, run_file)
        json.dump(output, sys.stdout, ensure_ascii=True, separators=(",", ":"))
        sys.stdout.write("\n")
        return 0
    except ScriptUnavailable as exc:
        json.dump(
            {"status": "unavailable", "fallback_safe": True, "message": str(exc)},
            sys.stderr,
            ensure_ascii=True,
        )
        sys.stderr.write("\n")
        return 2
    except PartialRunError as exc:
        json.dump(
            {
                "status": "partial",
                "fallback_safe": False,
                "run_file": str(exc.run_file),
                "message": str(exc),
            },
            sys.stderr,
            ensure_ascii=True,
        )
        sys.stderr.write("\n")
        return 3
    except (WatchlistError, OSError) as exc:
        json.dump(
            {
                "status": "error",
                "fallback_safe": getattr(exc, "fallback_safe", False),
                "message": str(exc),
            },
            sys.stderr,
            ensure_ascii=True,
        )
        sys.stderr.write("\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
