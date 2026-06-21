#!/usr/bin/env python3
"""Print one exact DataForSEO MCP tool catalog entry."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: lookup_tool.py <tool-name>", file=sys.stderr)
        return 2

    query = sys.argv[1].removeprefix("mcp__dataforseo__")
    catalog_path = Path(__file__).resolve().parents[1] / "references" / "mcp-tools.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    matches = [tool for tool in catalog["tools"] if tool["name"] == query]

    if not matches:
        suggestions = [tool["name"] for tool in catalog["tools"] if query in tool["name"]]
        print(f"unknown tool: {query}", file=sys.stderr)
        if suggestions:
            print("possible matches:", *suggestions, sep="\n- ", file=sys.stderr)
        return 1

    print(json.dumps(matches[0], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
