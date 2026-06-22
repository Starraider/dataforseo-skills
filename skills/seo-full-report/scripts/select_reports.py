#!/usr/bin/env python3
"""Select date-prefixed source reports for seo-full-report."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit


DATE_PREFIX = re.compile(r"^(\d{4}-\d{2}-\d{2})_")
HOST_LABEL = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")


def iso_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid ISO date {value!r}; use YYYY-MM-DD") from exc


def normalize_domain(value: str) -> str:
    raw = value.strip()
    if not raw:
        raise argparse.ArgumentTypeError("domain must not be empty")

    parsed = urlsplit(raw if "://" in raw else f"//{raw}")
    if parsed.scheme and parsed.scheme not in {"http", "https"}:
        raise argparse.ArgumentTypeError("domain URL must use HTTP or HTTPS")
    try:
        port = parsed.port
    except ValueError as exc:
        raise argparse.ArgumentTypeError("domain contains an invalid port") from exc
    if parsed.username or parsed.password or port:
        raise argparse.ArgumentTypeError("domain must not contain credentials or a port")
    if "://" not in raw and (parsed.path not in {"", "/"} or parsed.query or parsed.fragment):
        raise argparse.ArgumentTypeError("a domain without HTTP(S) must not contain a path, query, or fragment")

    host = (parsed.hostname or "").lower().rstrip(".")
    if host.startswith("www."):
        host = host[4:]
    labels = host.split(".")
    if len(labels) < 2 or any(not HOST_LABEL.fullmatch(label) for label in labels):
        raise argparse.ArgumentTypeError(f"invalid domain {value!r}")
    return host


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("domain", type=normalize_domain)
    parser.add_argument("--root", default="SEO", help="report root; defaults to SEO")
    parser.add_argument("--date", type=iso_date, help="one report date")
    parser.add_argument("--start-date", type=iso_date, help="inclusive range start")
    parser.add_argument("--end-date", type=iso_date, help="inclusive range end")
    parser.add_argument(
        "--include-full-reports",
        action="store_true",
        help="include earlier _Full-SEO-Report_ outputs",
    )
    return parser


def resolve_dates(parser: argparse.ArgumentParser, args: argparse.Namespace) -> tuple[date, date]:
    if args.date and (args.start_date or args.end_date):
        parser.error("use --date or --start-date with --end-date, not both")
    if args.date:
        return args.date, args.date
    if not args.start_date or not args.end_date:
        parser.error("provide --date or both --start-date and --end-date")
    if args.start_date > args.end_date:
        parser.error("--start-date must not be after --end-date")
    return args.start_date, args.end_date


def select(args: argparse.Namespace, start: date, end: date) -> dict[str, object]:
    directory = (Path(args.root).expanduser() / args.domain).resolve()
    selected: list[dict[str, object]] = []
    excluded_full_reports: list[str] = []

    if directory.is_dir():
        for path in sorted(directory.iterdir(), key=lambda item: item.name):
            if not path.is_file():
                continue
            match = DATE_PREFIX.match(path.name)
            if not match:
                continue
            try:
                report_date = date.fromisoformat(match.group(1))
            except ValueError:
                continue
            if not start <= report_date <= end:
                continue
            if "_Full-SEO-Report_" in path.name and not args.include_full_reports:
                excluded_full_reports.append(path.name)
                continue
            selected.append(
                {
                    "date": report_date.isoformat(),
                    "filename": path.name,
                    "path": str(path.resolve()),
                    "size_bytes": path.stat().st_size,
                }
            )

    return {
        "domain": args.domain,
        "directory": str(directory),
        "directory_exists": directory.is_dir(),
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "include_full_reports": args.include_full_reports,
        "excluded_full_reports": excluded_full_reports,
        "selected_count": len(selected),
        "selected": selected,
    }


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    start, end = resolve_dates(parser, args)
    json.dump(select(args, start, end), sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
