#!/usr/bin/env python3
"""Extract request/response examples for one URL from DataForSEO's Postman collection."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable


def requests(node: Any) -> Iterable[dict[str, Any]]:
    if isinstance(node, dict):
        if "request" in node:
            yield node
        for value in node.values():
            yield from requests(value)
    elif isinstance(node, list):
        for value in node:
            yield from requests(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Exact request URL from the tool catalog")
    parser.add_argument(
        "collection",
        nargs="?",
        type=Path,
        default=Path("dataforseo_xmpl_v3_postman.json"),
    )
    args = parser.parse_args()

    data = json.loads(args.collection.read_text(encoding="utf-8"))
    matches = [
        item
        for item in requests(data)
        if item.get("request", {}).get("url", {}).get("raw") == args.url
    ]
    print(json.dumps(matches, indent=2, ensure_ascii=False))
    return 0 if matches else 1


if __name__ == "__main__":
    raise SystemExit(main())
