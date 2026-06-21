#!/usr/bin/env python3
"""Deterministic helpers for the seo-page-metadata skill.

This module intentionally uses only the Python standard library. Raw provider
responses may be supplied through stdin for normalization but must not be
committed to the repository.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any
import unicodedata
from urllib.parse import SplitResult, urlsplit, urlunsplit


SUCCESS_STATUS = 20000
MAX_FILENAME_LENGTH = 140


class ContractError(ValueError):
    """Raised when input or a provider response violates the skill contract."""


@dataclass(frozen=True)
class ValidatedURL:
    supplied_url: str
    request_url: str
    report_url: str
    domain: str
    had_query_or_fragment: bool


def normalize_text(value: str) -> str:
    if not isinstance(value, str):
        raise ContractError("keyword text must be a string")
    return " ".join(unicodedata.normalize("NFKC", value).split())


def keyword_key(value: str) -> str:
    return normalize_text(value).casefold()


def _has_control_characters(value: str) -> bool:
    return any(unicodedata.category(char) == "Cc" for char in value)


def validate_url(value: str) -> ValidatedURL:
    if not isinstance(value, str) or not value or _has_control_characters(value):
        raise ContractError("URL must be a non-empty string without control characters")
    if any(char.isspace() for char in value):
        raise ContractError("URL must not contain unescaped whitespace")
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError as exc:
        raise ContractError(f"malformed URL: {exc}") from exc
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ContractError("URL scheme must be http or https")
    if not parsed.hostname:
        raise ContractError("URL must include a hostname")
    if parsed.username is not None or parsed.password is not None:
        raise ContractError("URL must not contain embedded credentials")
    hostname = parsed.hostname.rstrip(".").lower()
    try:
        hostname = hostname.encode("idna").decode("ascii")
    except UnicodeError as exc:
        raise ContractError("URL hostname is not valid IDNA") from exc
    if hostname.startswith("www."):
        domain = hostname[4:]
    else:
        domain = hostname
    domain = domain.replace(":", "-")
    if not domain:
        raise ContractError("normalized hostname is empty")

    host_for_url = hostname
    if ":" in host_for_url and not host_for_url.startswith("["):
        host_for_url = f"[{host_for_url}]"
    netloc = host_for_url
    if port is not None:
        netloc = f"{netloc}:{port}"
    cleaned = SplitResult(
        parsed.scheme.lower(), netloc, parsed.path or "/", parsed.query, ""
    )
    request_url = urlunsplit(cleaned)
    report_url = urlunsplit(
        SplitResult(
            parsed.scheme.lower(),
            netloc,
            parsed.path or "/",
            "[redacted]" if parsed.query else "",
            "[redacted]" if parsed.fragment else "",
        )
    )
    return ValidatedURL(
        supplied_url=value,
        request_url=request_url,
        report_url=report_url,
        domain=domain,
        had_query_or_fragment=bool(parsed.query or parsed.fragment),
    )


def _safe_slug(request_url: str) -> str:
    parsed = urlsplit(request_url)
    readable = urlunsplit((parsed.scheme, parsed.netloc, parsed.path or "/", "", ""))
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", readable).strip("_")
    slug = re.sub(r"_+", "_", slug)
    return slug or "page"


def report_filename(url: str, report_date: str | None = None) -> tuple[ValidatedURL, str]:
    validated = validate_url(url)
    report_date = report_date or date.today().isoformat()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", report_date):
        raise ContractError("date must use YYYY-MM-DD")
    try:
        date.fromisoformat(report_date)
    except ValueError as exc:
        raise ContractError("date must be a valid calendar date") from exc
    slug = _safe_slug(validated.request_url)
    digest = hashlib.sha256(validated.request_url.encode("utf-8")).hexdigest()[:8]
    hash_suffix = f"_{digest}"
    prefix = f"{report_date}_Page-Metadata_"
    extension = ".md"
    available = MAX_FILENAME_LENGTH - len(prefix) - len(hash_suffix) - len(extension)
    if available < 1:
        raise ContractError("filename limit is too small")
    if len(slug) > available:
        slug = slug[:available].rstrip("._-") or "page"
    filename = f"{prefix}{slug}{hash_suffix}{extension}"
    return validated, filename


def _require_success(payload: dict) -> list[dict]:
    if not isinstance(payload, dict):
        raise ContractError("provider payload must be a JSON object")
    if payload.get("status_code") != SUCCESS_STATUS:
        raise ContractError(
            f"provider status {payload.get('status_code')}: {payload.get('status_message')}"
        )
    if payload.get("tasks_error") not in (None, 0):
        raise ContractError(f"provider reports {payload.get('tasks_error')} task errors")
    tasks = payload.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise ContractError("provider response has no tasks")
    for task in tasks:
        if not isinstance(task, dict) or task.get("status_code") != SUCCESS_STATUS:
            status = task.get("status_code") if isinstance(task, dict) else None
            message = task.get("status_message") if isinstance(task, dict) else None
            raise ContractError(f"task status {status}: {message}")
    return tasks


def _crawl_items(tasks: list[dict]) -> list[dict]:
    items: list[dict] = []
    for task in tasks:
        results = task.get("result")
        if not isinstance(results, list) or not results:
            raise ContractError("successful OnPage task has no result")
        for result in results:
            if not isinstance(result, dict):
                raise ContractError("OnPage result must be an object")
            if result.get("crawl_progress") != "finished":
                raise ContractError(f"OnPage crawl is not finished: {result.get('crawl_progress')}")
            result_items = result.get("items")
            if not isinstance(result_items, list) or not result_items:
                raise ContractError("successful OnPage result has no items")
            items.extend(item for item in result_items if isinstance(item, dict))
    return items


def extract_instant_metadata(payload: dict) -> dict:
    items = _crawl_items(_require_success(payload))
    html_items = [item for item in items if item.get("resource_type") == "html"]
    if not html_items:
        resource_types = sorted({str(item.get("resource_type")) for item in items})
        raise ContractError(f"Instant Pages returned no HTML page: {resource_types}")
    item = html_items[0]
    status = item.get("status_code")
    if not isinstance(status, int) or not 200 <= status <= 299:
        raise ContractError(f"Instant Pages page HTTP status is not successful: {status}")
    meta = item.get("meta") or {}
    if not isinstance(meta, dict):
        raise ContractError("Instant Pages meta field must be an object")
    social = meta.get("social_media_tags") or {}
    if not isinstance(social, dict):
        social = {}
    return {
        "resolved_url": item.get("url"),
        "location": item.get("location"),
        "http_status": status,
        "resource_type": item.get("resource_type"),
        "title": meta.get("title"),
        "description": meta.get("description"),
        "meta_keywords": meta.get("meta_keywords"),
        "canonical": meta.get("canonical"),
        "title_length": meta.get("title_length"),
        "description_length": meta.get("description_length"),
        "social_media_tags": social,
    }


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        key = value.casefold()
        if key not in seen:
            seen.add(key)
            output.append(value)
    return output


PROJECTED_TEXT_WARNING = (
    "Content Parsing structure was unavailable; using conservative fallback extraction "
    "from projected text."
)

MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
BOILERPLATE_LINE_PATTERNS = (
    re.compile(r"(?i)^start the conversation$"),
    re.compile(r"(?i)^kontakt$"),
    re.compile(r"(?i)^folge mir:?$"),
    re.compile(r"(?i)^zum blog$"),
    re.compile(r"(?i)^privacy policy$"),
    re.compile(r"(?i)^datenschutzerklärung$"),
    re.compile(r"(?i)^impressum$"),
    re.compile(r"(?i)^cookie(?: policy| settings| banner)?$"),
    re.compile(r"(?i)^tel\.?:"),
    re.compile(r"(?i)^e-?mail:"),
    re.compile(r"(?i)^©"),
)
CONTACT_VALUE_PATTERNS = (
    re.compile(r"(?i)^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$"),
    re.compile(r"^\+?\d[\d\s()/.-]+$"),
)


def _normalize_projected_text(raw_text: str) -> str:
    text = MARKDOWN_LINK_RE.sub(r"\1", raw_text)
    text = re.sub(r"[`*_]+", "", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text


def _is_boilerplate_line(line: str) -> bool:
    normalized = normalize_text(line)
    if not normalized:
        return True
    if any(pattern.match(normalized) for pattern in BOILERPLATE_LINE_PATTERNS):
        return True
    if any(pattern.match(normalized) for pattern in CONTACT_VALUE_PATTERNS):
        return True
    if len(normalized) <= 2:
        return True
    return False


def _extract_from_projected_text(raw_text: str, status: int = 200) -> dict:
    text = _normalize_projected_text(raw_text)
    lines = [line.strip() for line in text.splitlines()]
    headings: list[str] = []
    primary_text: list[str] = []
    paragraph_lines: list[str] = []

    def flush_paragraph() -> None:
        if not paragraph_lines:
            return
        paragraph = normalize_text(" ".join(paragraph_lines))
        paragraph_lines.clear()
        if _is_boilerplate_line(paragraph):
            return
        primary_text.append(paragraph)

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            flush_paragraph()
            continue
        if line.startswith("#"):
            flush_paragraph()
            heading = normalize_text(line.lstrip("#").strip())
            if heading and not _is_boilerplate_line(heading):
                headings.append(heading)
            continue
        candidate = normalize_text(line)
        if _is_boilerplate_line(candidate):
            flush_paragraph()
            continue
        paragraph_lines.append(candidate)
    flush_paragraph()

    return {
        "http_status": status,
        "headings": _unique(headings),
        "primary_text": _unique(primary_text),
        "languages": [],
        "evidence_mode": "projection_degraded_text",
        "degraded": True,
        "warnings": [PROJECTED_TEXT_WARNING],
    }


def extract_primary_evidence(payload: Any) -> dict:
    if isinstance(payload, str):
        return _extract_from_projected_text(payload)
    if isinstance(payload, dict) and isinstance(payload.get("text"), str) and "tasks" not in payload:
        return _extract_from_projected_text(payload["text"])
    items = _crawl_items(_require_success(payload))
    content_items = [item for item in items if item.get("type") == "content_parsing_element"]
    if not content_items:
        raise ContractError("Content Parsing returned no content_parsing_element")
    item = content_items[0]
    status = item.get("status_code")
    if not isinstance(status, int) or not 200 <= status <= 299:
        raise ContractError(f"Content Parsing page HTTP status is not successful: {status}")
    page_content = item.get("page_content") or {}
    if not isinstance(page_content, dict):
        raise ContractError("Content Parsing page_content must be an object")
    topics = page_content.get("main_topic") or []
    if not isinstance(topics, list):
        raise ContractError("Content Parsing main_topic must be an array")

    headings: list[str] = []
    texts: list[str] = []
    languages: list[str] = []
    for topic in topics:
        if not isinstance(topic, dict):
            continue
        for field in ("main_title", "h_title"):
            value = topic.get(field)
            if isinstance(value, str) and normalize_text(value):
                headings.append(normalize_text(value))
        language = topic.get("language")
        if isinstance(language, str) and normalize_text(language):
            languages.append(normalize_text(language))
        primary = topic.get("primary_content") or []
        if not isinstance(primary, list):
            continue
        for block in primary:
            text = block.get("text") if isinstance(block, dict) else None
            if isinstance(text, str) and normalize_text(text):
                texts.append(normalize_text(text))
    if not headings and not texts:
        projected_text = item.get("page_as_markdown")
        if isinstance(projected_text, str) and normalize_text(projected_text):
            return _extract_from_projected_text(projected_text, status=status)
    return {
        "http_status": status,
        "headings": _unique(headings),
        "primary_text": _unique(texts),
        "languages": _unique(languages),
        "evidence_mode": "structured_main_topic",
        "degraded": False,
        "warnings": [],
    }


def extract_related_rows(payload: dict, source_seed: str) -> list[dict]:
    tasks = _require_success(payload)
    seed_key = keyword_key(source_seed)
    rows: list[dict] = []
    for task in tasks:
        results = task.get("result")
        if not isinstance(results, list) or not results:
            raise ContractError("successful Related Keywords task has no result")
        for result in results:
            items = result.get("items") if isinstance(result, dict) else None
            if items is None:
                continue
            if not isinstance(items, list):
                raise ContractError("Related Keywords items must be an array")
            for item in items:
                data = item.get("keyword_data") if isinstance(item, dict) else None
                if not isinstance(data, dict) or not isinstance(data.get("keyword"), str):
                    continue
                keyword = normalize_text(data["keyword"])
                if not keyword or keyword_key(keyword) == seed_key:
                    continue
                info = data.get("keyword_info") or {}
                properties = data.get("keyword_properties") or {}
                if not isinstance(info, dict) or not isinstance(properties, dict):
                    raise ContractError("Related Keywords metric fields must be objects or null")
                rows.append(
                    {
                        "keyword": keyword,
                        "search_volume": info.get("search_volume"),
                        "keyword_difficulty": properties.get("keyword_difficulty"),
                        "ads_competition": info.get("competition"),
                        "ads_competition_level": info.get("competition_level"),
                        "cpc": info.get("cpc"),
                        "source_seeds": [normalize_text(source_seed)],
                        "conflicts": [],
                    }
                )
    return rows


METRIC_FIELDS = (
    "search_volume",
    "keyword_difficulty",
    "ads_competition",
    "ads_competition_level",
    "cpc",
)


def merge_rows(rows: list[dict]) -> list[dict]:
    merged: dict[str, dict] = {}
    for raw in rows:
        keyword = normalize_text(raw["keyword"])
        key = keyword_key(keyword)
        incoming_seeds = [normalize_text(seed) for seed in raw.get("source_seeds", [])]
        if key not in merged:
            merged[key] = {
                "keyword": keyword,
                **{field: raw.get(field) for field in METRIC_FIELDS},
                "source_seeds": sorted(set(incoming_seeds), key=str.casefold),
                "conflicts": list(raw.get("conflicts", [])),
            }
            continue
        current = merged[key]
        current["source_seeds"] = sorted(
            set(current["source_seeds"]) | set(incoming_seeds), key=str.casefold
        )
        for field in METRIC_FIELDS:
            old = current.get(field)
            new = raw.get(field)
            if old is None and new is not None:
                current[field] = new
            elif old is not None and new is not None and old != new:
                conflict = {"field": field, "kept": old, "observed": new}
                if conflict not in current["conflicts"]:
                    current["conflicts"].append(conflict)
    return sorted(merged.values(), key=lambda row: keyword_key(row["keyword"]))


def rank_rows(rows: list[dict], limit: int = 20) -> tuple[list[dict], int]:
    if not isinstance(limit, int) or limit < 1:
        raise ContractError("ranking limit must be a positive integer")
    eligible: list[tuple[dict, Decimal, Decimal, Decimal]] = []
    incomplete = 0
    for raw in rows:
        row = dict(raw)
        volume = row.get("search_volume")
        difficulty = row.get("keyword_difficulty")
        if volume is None or difficulty is None:
            row["opportunity_proxy"] = None
            incomplete += 1
            continue
        try:
            volume_decimal = Decimal(str(volume))
            difficulty_decimal = Decimal(str(difficulty))
        except Exception as exc:
            raise ContractError(f"invalid volume or keyword difficulty for {row.get('keyword')}") from exc
        if not volume_decimal.is_finite() or not difficulty_decimal.is_finite():
            raise ContractError(f"non-finite metrics for {row.get('keyword')}")
        if volume_decimal < 0 or not Decimal("0") <= difficulty_decimal <= Decimal("100"):
            raise ContractError(f"metrics outside documented ranges for {row.get('keyword')}")
        score = volume_decimal / (difficulty_decimal + Decimal("10"))
        row["opportunity_proxy"] = float(score)
        eligible.append((row, score, volume_decimal, difficulty_decimal))
    eligible.sort(
        key=lambda item: (
            -item[1],
            -item[2],
            item[3],
            keyword_key(item[0]["keyword"]),
        )
    )
    return [item[0] for item in eligible[:limit]], incomplete


def _cost_decimal(value: object) -> Decimal:
    try:
        parsed = Decimal(str(value))
    except Exception as exc:
        raise ContractError(f"invalid cost value: {value!r}") from exc
    if not parsed.is_finite() or parsed < 0:
        raise ContractError(f"invalid cost value: {value!r}")
    return parsed


def collect_cost(payload: dict) -> tuple[Decimal, bool]:
    if not isinstance(payload, dict):
        raise ContractError("provider payload must be a JSON object")
    tasks = payload.get("tasks")
    if isinstance(tasks, list) and tasks:
        values = [task.get("cost") for task in tasks if isinstance(task, dict)]
        complete = len(values) == len(tasks) and all(value is not None for value in values)
        total = sum((_cost_decimal(value) for value in values if value is not None), Decimal("0"))
        return total, complete
    value = payload.get("cost")
    if value is None:
        return Decimal("0"), False
    return _cost_decimal(value), True


def collect_costs(payloads: list[dict]) -> tuple[Decimal, bool]:
    if not isinstance(payloads, list) or not payloads:
        raise ContractError("cost input must contain at least one provider response")
    total = Decimal("0")
    complete = True
    for payload in payloads:
        value, item_complete = collect_cost(payload)
        total += value
        complete = complete and item_complete
    return total, complete


def format_cost(value: Decimal) -> str:
    rounded = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{rounded:.2f}".replace(".", ",") + " USD"


def _read_stdin_json() -> Any:
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        raise ContractError(f"stdin is not valid JSON: {exc}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    filename_parser = subparsers.add_parser("filename")
    filename_parser.add_argument("--url", required=True)
    filename_parser.add_argument("--date")
    filename_parser.add_argument("--root", default="SEO")

    count_parser = subparsers.add_parser("count")
    count_parser.add_argument("--text", required=True)

    related_parser = subparsers.add_parser("normalize-related")
    related_parser.add_argument("--seed", required=True)

    subparsers.add_parser("normalize-batch")
    subparsers.add_parser("rank")
    subparsers.add_parser("extract-instant")
    subparsers.add_parser("extract-content")
    subparsers.add_parser("cost")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "filename":
            validated, filename = report_filename(args.url, args.date)
            root = Path(args.root).expanduser()
            if not root.is_absolute():
                root = Path.cwd() / root
            output = {
                "supplied_url": validated.supplied_url,
                "request_url": validated.request_url,
                "report_url": validated.report_url,
                "domain": validated.domain,
                "filename": filename,
                "report_path": str((root / validated.domain / filename).resolve()),
            }
        elif args.command == "count":
            output = {"text": args.text, "unicode_code_points": len(args.text)}
        elif args.command == "normalize-related":
            rows = merge_rows(extract_related_rows(_read_stdin_json(), args.seed))
            ranked, incomplete = rank_rows(rows)
            output = {"rows": rows, "ranked": ranked, "incomplete_metrics": incomplete}
        elif args.command == "normalize-batch":
            payload = _read_stdin_json()
            calls = payload.get("calls") if isinstance(payload, dict) else None
            if not isinstance(calls, list) or not calls:
                raise ContractError("batch input must contain a non-empty calls array")
            rows = []
            for call in calls:
                if not isinstance(call, dict) or not isinstance(call.get("seed"), str):
                    raise ContractError("every batch call must contain seed and response")
                rows.extend(extract_related_rows(call.get("response"), call["seed"]))
            output = {"rows": merge_rows(rows)}
        elif args.command == "rank":
            payload = _read_stdin_json()
            rows = payload.get("rows") if isinstance(payload, dict) else payload
            if not isinstance(rows, list):
                raise ContractError("rank input must be a rows array or an object containing rows")
            ranked, incomplete = rank_rows(rows)
            output = {"ranked": ranked, "incomplete_metrics": incomplete}
        elif args.command == "extract-instant":
            output = extract_instant_metadata(_read_stdin_json())
        elif args.command == "extract-content":
            output = extract_primary_evidence(_read_stdin_json())
        else:
            payload = _read_stdin_json()
            responses = payload.get("responses") if isinstance(payload, dict) else None
            if responses is not None:
                total, complete = collect_costs(responses)
            else:
                total, complete = collect_cost(payload)
            output = {"unrounded": str(total), "formatted": format_cost(total), "complete": complete}
    except ContractError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
