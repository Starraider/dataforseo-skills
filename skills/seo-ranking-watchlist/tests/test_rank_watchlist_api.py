#!/usr/bin/env python3
"""Regression tests for durable ranking-watchlist API runs."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "skills/seo-ranking-watchlist/scripts/rank_watchlist_api.py"


def load_module():
    spec = importlib.util.spec_from_file_location("rank_watchlist_api", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def serp_task(keyword: str, position: int = 18) -> dict:
    return {
        "cost": 0.006,
        "result": [
            {
                "datetime": "2026-06-22 12:00:00 +00:00",
                "items": [
                    {
                        "type": "organic",
                        "rank_group": position,
                        "domain": "www.example.com",
                        "url": f"https://www.example.com/{keyword.replace(' ', '-')}",
                    }
                ],
            }
        ],
    }


class FakeClient:
    def __init__(self, module, failing: set[str] | None = None) -> None:
        self.module = module
        self.failing = failing or set()
        self.calls: list[str] = []

    def post(self, path: str, payload: dict) -> dict:
        assert path == self.module.SERP_PATH
        keyword = payload["keyword"]
        self.calls.append(keyword)
        if keyword in self.failing:
            raise self.module.WatchlistError(f"fixture failure for {keyword}")
        return serp_task(keyword)


def base_manifest(watchlist: Path) -> dict:
    return {
        "schema_version": 1,
        "run_id": "fixture-run",
        "status": "checking",
        "operation": "add",
        "domain": "example.com",
        "label": "Example",
        "scope": {
            "location_name": "Germany",
            "language_code": "de",
            "device": "desktop",
            "depth": 100,
        },
        "watchlist_path": str(watchlist),
        "watchlist_sha256": None,
        "reset_scope": False,
        "commit_requested": True,
        "keywords": ["first term", "second term"],
        "discovered": [],
        "results": {},
        "errors": {},
        "costs_usd": {"discovery": 0.01, "serp": {}},
        "snapshot_date": "2026-06-22",
        "created_at": "2026-06-22T12:00:00+00:00",
        "updated_at": "2026-06-22T12:00:00+00:00",
    }


def test_payload_normalization(module) -> None:
    assert module.normalize_domain("WWW.Example.com.") == "example.com"
    try:
        module.normalize_domain("example.com:invalid")
        raise AssertionError("invalid port should fail domain normalization")
    except module.argparse.ArgumentTypeError:
        pass

    discovery_payload = module.build_discovery_payload(
        "example.com", "Germany", "de", 100
    )
    assert discovery_payload["limit"] == 100
    assert discovery_payload["item_types"] == ["organic"]
    assert discovery_payload["historical_serp_mode"] == "live"

    discovery_task = {
        "cost": 0.01,
        "result": [
            {
                "items": [
                    {
                        "keyword_data": {
                            "keyword": " outlet   center ",
                            "keyword_info": {"search_volume": 1200},
                        },
                        "ranked_serp_element": {
                            "serp_item": {
                                "rank_group": 18,
                                "url": "https://example.com/outlet",
                            }
                        },
                    }
                ]
            }
        ],
    }
    assert module.normalize_discovery(discovery_task) == [
        {
            "keyword": "outlet center",
            "labs_position": 18,
            "search_volume": 1200,
            "url": "https://example.com/outlet",
        }
    ]

    serp_payload = module.build_serp_payload(
        "example.com", "outlet center", "Germany", "de", "desktop", 100
    )
    assert serp_payload["target"] == "*example.com*"
    assert serp_payload["find_targets_in"] == ["organic"]
    assert serp_payload["stop_crawl_on_match"] == [
        {"match_value": "example.com", "match_type": "with_subdomains"}
    ]
    normalized = module.normalize_serp(
        serp_task("outlet center"), "outlet center", "example.com", 100
    )
    assert normalized["position"] == 18
    assert normalized["cost_usd"] == 0.006

    no_results = module.normalize_serp(
        {"status_code": 40102, "cost": 0.004},
        "missing term",
        "example.com",
        100,
    )
    assert no_results["position"] is None
    assert no_results["url"] is None
    assert no_results["cost_usd"] == 0.004


def test_partial_run_and_resume(module, root: Path) -> None:
    watchlist = root / "SEO/example.com/watchlist.json"
    run_file = root / "SEO/example.com/.watchlist-runs/fixture.json"
    manifest = base_manifest(watchlist)
    module.write_manifest(run_file, manifest)

    first_client = FakeClient(module, {"second term"})
    try:
        module.check_all(first_client, manifest, run_file, workers=2)
        raise AssertionError("partial run should fail")
    except module.PartialRunError:
        pass
    persisted = json.loads(run_file.read_text(encoding="utf-8"))
    assert "first term" in persisted["results"]
    assert "second term" in persisted["errors"]

    second_client = FakeClient(module)
    module.check_all(second_client, persisted, run_file, workers=2)
    assert second_client.calls == ["second term"]
    assert set(persisted["results"]) == {"first term", "second term"}
    assert persisted["errors"] == {}


def test_resume_coerces_no_search_results(module, root: Path) -> None:
    watchlist = root / "SEO/example.com/watchlist.json"
    run_file = root / "SEO/example.com/.watchlist-runs/no-results.json"
    manifest = base_manifest(watchlist)
    manifest["errors"] = {
        "first term": (
            "DataForSEO task error for serp/google/organic/live/advanced: "
            "40102 No Search Results."
        )
    }
    manifest["results"] = {
        "second term": {
            "keyword": "second term",
            "position": 12,
            "url": "https://example.com/second",
            "checked_at": "2026-06-22 12:00:00 +00:00",
            "cost_usd": 0.006,
        }
    }
    module.write_manifest(run_file, manifest)

    module.coerce_no_search_results(manifest)

    assert manifest["errors"] == {}
    assert manifest["results"]["first term"]["position"] is None
    assert manifest["results"]["first term"]["url"] is None


def test_atomic_idempotent_commit(module, root: Path) -> None:
    watchlist = root / "SEO/example.com/watchlist.json"
    run_file = root / "SEO/example.com/.watchlist-runs/commit.json"
    manifest = base_manifest(watchlist)
    manifest["results"] = {
        "first term": {
            "keyword": "first term",
            "position": 18,
            "url": "https://example.com/first",
            "checked_at": "2026-06-22 12:00:00 +00:00",
            "cost_usd": 0.006,
        },
        "second term": {
            "keyword": "second term",
            "position": None,
            "url": None,
            "checked_at": "2026-06-22 12:00:00 +00:00",
            "cost_usd": 0.01,
        },
    }
    module.write_manifest(run_file, manifest)
    module.commit_manifest(manifest, run_file)
    module.commit_manifest(manifest, run_file)

    payload = json.loads(watchlist.read_text(encoding="utf-8"))
    entry = payload["domains"]["example.com"]
    assert entry["label"] == "Example"
    assert entry["scope"]["language_code"] == "de"
    assert len(entry["history"]) == 1
    assert entry["history"][0]["rankings"] == [
        {"keyword": "first term", "position": 18},
        {"keyword": "second term", "position": None},
    ]
    assert json.loads(run_file.read_text(encoding="utf-8"))["status"] == "committed"


def test_bounded_summary(module, root: Path) -> None:
    manifest = base_manifest(root / "watchlist.json")
    manifest["keywords"] = [f"keyword {index}" for index in range(100)]
    manifest["results"] = {
        keyword: {
            "keyword": keyword,
            "position": 15,
            "url": f"https://example.com/{index}",
            "checked_at": "2026-06-22 12:00:00 +00:00",
            "cost_usd": 0.006,
        }
        for index, keyword in enumerate(manifest["keywords"])
    }
    output = module.summary(manifest, root / "run.json")
    encoded = json.dumps(output, separators=(",", ":"))
    assert len(encoded) < 1000
    assert output["keyword_count"] == 100
    assert output["opportunities_11_20"] == 100


def test_concurrent_change_is_rejected(module, root: Path) -> None:
    watchlist = root / "conflict/watchlist.json"
    run_file = root / "conflict/run.json"
    manifest = base_manifest(watchlist)
    manifest["results"] = {
        keyword: {
            "keyword": keyword,
            "position": 18,
            "url": "https://example.com/result",
            "checked_at": "2026-06-22 12:00:00 +00:00",
            "cost_usd": 0.006,
        }
        for keyword in manifest["keywords"]
    }
    module.write_manifest(run_file, manifest)
    module.atomic_write_json(
        watchlist,
        {
            "domains": {
                "other.example": {
                    "label": "Concurrent update",
                    "scope": module.DEFAULT_SCOPE,
                    "keywords": ["other"],
                    "history": [],
                }
            }
        },
    )
    try:
        module.commit_manifest(manifest, run_file)
        raise AssertionError("concurrent watchlist update should block commit")
    except module.WatchlistError as exc:
        assert "changed during the run" in str(exc)
    payload = json.loads(watchlist.read_text(encoding="utf-8"))
    assert "example.com" not in payload["domains"]


def main() -> int:
    module = load_module()
    test_payload_normalization(module)
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        test_partial_run_and_resume(module, root)
        test_resume_coerces_no_search_results(module, root)
        test_atomic_idempotent_commit(module, root)
        test_bounded_summary(module, root)
        test_concurrent_change_is_rejected(module, root)
    print("rank_watchlist_api regression tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
