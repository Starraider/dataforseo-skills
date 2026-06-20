#!/usr/bin/env python3
"""Regression checks for the normalized fetch_task_onpage helper output."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "skills/seo-technical-page-audit/scripts/fetch_task_onpage.py"
FIXTURE_PATH = (
    ROOT / "skills/seo-technical-page-audit/tests/fixtures/fetch_task_onpage_shape.json"
)


def load_module():
    spec = importlib.util.spec_from_file_location("fetch_task_onpage", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_module()
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    normalized = module.normalize_summary(
        fixture["audited_url"],
        fixture["crawled_page_url"],
        "en-US",
        fixture["endpoints"],
    )

    assert normalized["accept_language_used"] == "en-US"
    assert normalized["page_timing_source"] == "pages.page_timing"
    assert normalized["page_status_code"] == 200
    assert normalized["onpage_score"] == 91.59
    assert normalized["broken_link_urls"] == []
    assert normalized["broken_resource_urls"] == [
        "https://www.example.com/assets/main.js"
    ]
    assert normalized["valid_hreflang_targets"] == [
        "https://www.example.com/",
        "https://www.example.com/de/"
    ]
    assert normalized["render_blocking_resource_urls"] == [
        "https://www.example.com/assets/main.js",
        "https://www.example.com/assets/app.css"
    ]
    assert normalized["inventory_counts"]["resources"] == {"returned": 2, "total": 3}
    assert normalized["truncated_inventories"] == ["resources"]
    assert normalized["waterfall_page_url"] == "https://analytics.example/script.js"
    assert normalized["waterfall_page_url_anomaly"] is True
    assert normalized["microdata_summary"] == {
        "fatal": 0,
        "error": 0,
        "warning": 0,
        "info": 0,
    }

    print("fetch_task_onpage fixture regression passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
