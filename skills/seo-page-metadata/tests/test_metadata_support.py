#!/usr/bin/env python3

from __future__ import annotations

from decimal import Decimal
import json
from pathlib import Path
import sys
import unittest


SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

from metadata_support import (  # noqa: E402
    ContractError,
    collect_cost,
    collect_costs,
    extract_instant_metadata,
    extract_primary_evidence,
    extract_related_rows,
    format_cost,
    keyword_key,
    merge_rows,
    normalize_text,
    rank_rows,
    report_filename,
    validate_url,
)


class URLTests(unittest.TestCase):
    def test_url_validation_removes_fragment_and_normalizes_domain(self):
        result = validate_url("HTTPS://WWW.Example.DE:8443/a?q=1#fragment")
        self.assertEqual(result.request_url, "https://www.example.de:8443/a?q=1")
        self.assertEqual(
            result.report_url,
            "https://www.example.de:8443/a?[redacted]#[redacted]",
        )
        self.assertEqual(result.domain, "example.de")
        self.assertTrue(result.had_query_or_fragment)

    def test_url_validation_rejects_credentials_and_other_schemes(self):
        for value in (
            "ftp://example.com/a",
            "https://user:pass@example.com/a",
            "https://example.com/a path",
            "example.com",
        ):
            with self.subTest(value=value), self.assertRaises(ContractError):
                validate_url(value)

    def test_filename_hides_query_and_is_deterministic(self):
        _, first = report_filename("https://example.com/a?customer=secret", "2026-06-21")
        _, second = report_filename("https://example.com/a?customer=other", "2026-06-21")
        self.assertNotIn("customer", first)
        self.assertNotIn("secret", first)
        self.assertNotEqual(first, second)
        self.assertLessEqual(len(first), 140)
        self.assertTrue(first.endswith(".md"))

    def test_filename_without_query_still_has_collision_hash(self):
        _, filename = report_filename("https://example.com/a/b", "2026-06-21")
        self.assertRegex(filename, r"_[0-9a-f]{8}\.md$")

    def test_long_filename_is_capped_with_hash(self):
        _, filename = report_filename("https://example.com/" + "a" * 300, "2026-06-21")
        self.assertEqual(len(filename), 140)
        self.assertRegex(filename, r"_[0-9a-f]{8}\.md$")

    def test_filename_rejects_invalid_calendar_date(self):
        with self.assertRaises(ContractError):
            report_filename("https://example.com/a", "2026-02-30")


class KeywordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture = SKILL_ROOT / "tests" / "fixtures" / "related_keywords_success.json"
        cls.payload = json.loads(fixture.read_text())

    def test_unicode_and_whitespace_normalization(self):
        self.assertEqual(normalize_text("  cafe\u0301\u00a0  service "), "café service")
        self.assertEqual(keyword_key("STRASSE"), keyword_key("strasse"))

    def test_related_extraction_removes_seed_and_preserves_zero_and_null(self):
        rows = extract_related_rows(self.payload, "mobile vet lahore")
        self.assertEqual(len(rows), 3)
        emergency = next(row for row in rows if row["keyword"] == "Emergency Vet Lahore")
        self.assertEqual(emergency["search_volume"], 0)
        self.assertEqual(emergency["ads_competition"], 0)
        self.assertEqual(emergency["cpc"], 0)
        incomplete = next(row for row in rows if row["keyword"] == "Animal Doctor at Home")
        self.assertIsNone(incomplete["keyword_difficulty"])

    def test_merge_keeps_first_metric_and_records_conflict(self):
        rows = [
            {
                "keyword": "Home Vet Visit Lahore",
                "search_volume": 100,
                "keyword_difficulty": 10,
                "ads_competition": None,
                "ads_competition_level": None,
                "cpc": 1.25,
                "source_seeds": ["mobile vet lahore"],
                "conflicts": [],
            },
            {
                "keyword": " home\u00a0vet visit lahore ",
                "search_volume": 120,
                "keyword_difficulty": 10,
                "ads_competition": 0.2,
                "ads_competition_level": "LOW",
                "cpc": 1.25,
                "source_seeds": ["home veterinarian lahore"],
                "conflicts": [],
            },
        ]
        merged = merge_rows(rows)
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["search_volume"], 100)
        self.assertEqual(merged[0]["ads_competition"], 0.2)
        self.assertEqual(len(merged[0]["conflicts"]), 1)
        self.assertEqual(len(merged[0]["source_seeds"]), 2)

    def test_ranking_preserves_zero_and_reports_incomplete(self):
        rows = merge_rows(extract_related_rows(self.payload, "mobile vet lahore"))
        ranked, incomplete = rank_rows(rows)
        self.assertEqual(incomplete, 1)
        self.assertEqual(ranked[0]["keyword"], "Home Vet Visit Lahore")
        self.assertEqual(ranked[-1]["opportunity_proxy"], 0.0)

    def test_task_failure_is_not_empty_success(self):
        payload = {
            "status_code": 20000,
            "tasks_error": 1,
            "tasks": [{"status_code": 40501, "status_message": "crawl in progress"}],
        }
        with self.assertRaises(ContractError):
            extract_related_rows(payload, "seed")

    def test_ranking_rejects_metrics_outside_documented_ranges(self):
        for volume, difficulty in ((-1, 10), (10, -1), (10, 101)):
            with self.subTest(volume=volume, difficulty=difficulty), self.assertRaises(ContractError):
                rank_rows(
                    [
                        {
                            "keyword": "invalid metric",
                            "search_volume": volume,
                            "keyword_difficulty": difficulty,
                        }
                    ]
                )


class OnPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture = SKILL_ROOT / "tests" / "fixtures" / "onpage_success.json"
        cls.payload = json.loads(fixture.read_text())

    def test_current_metadata_is_extracted_from_instant_pages(self):
        metadata = extract_instant_metadata(self.payload["instant_pages"])
        self.assertEqual(metadata["title"], "Online Pet Store")
        self.assertEqual(metadata["http_status"], 200)
        self.assertEqual(metadata["social_media_tags"]["og:title"], "Online Pet Store")

    def test_primary_evidence_excludes_header_footer_and_secondary_content(self):
        evidence = extract_primary_evidence(self.payload["content_parsing"])
        self.assertEqual(evidence["languages"], ["en"])
        self.assertEqual(evidence["evidence_mode"], "structured_main_topic")
        self.assertFalse(evidence["degraded"])
        self.assertIn("Mobile Veterinary Visits in Lahore", evidence["headings"])
        combined = " ".join(evidence["headings"] + evidence["primary_text"])
        for excluded in ("Shop Pet Food", "Privacy policy", "Recent posts", "Karachi"):
            self.assertNotIn(excluded, combined)

    def test_primary_evidence_falls_back_to_projected_text(self):
        payload = (
            "# Herzlich Willkommen!\n\n"
            "Mein Name ist Sven Kalbhenn.\n\n"
            "Seit mehr als 20 Jahren erstelle ich Websites für meine Kunden.\n\n"
            "Kontakt\n\n"
            "Tel.: +49 156 78581807\n\n"
            "E-Mail: sven@skom.de\n\n"
            "© 2022 SKom\n"
        )
        evidence = extract_primary_evidence(payload)
        self.assertEqual(evidence["evidence_mode"], "projection_degraded_text")
        self.assertTrue(evidence["degraded"])
        self.assertEqual(evidence["languages"], [])
        self.assertIn("Herzlich Willkommen!", evidence["headings"])
        combined = " ".join(evidence["headings"] + evidence["primary_text"])
        self.assertIn("Seit mehr als 20 Jahren erstelle ich Websites für meine Kunden.", combined)
        for excluded in ("Kontakt", "+49 156 78581807", "sven@skom.de", "© 2022 SKom"):
            self.assertNotIn(excluded, combined)

    def test_primary_evidence_falls_back_to_page_as_markdown_when_main_topic_missing(self):
        payload = json.loads(json.dumps(self.payload["content_parsing"]))
        item = payload["tasks"][0]["result"][0]["items"][0]
        item["page_content"]["main_topic"] = []
        item["page_as_markdown"] = (
            "# Mobile Veterinary Visits in Lahore\n\n"
            "Our veterinarians provide mobile checkups and urgent home visits throughout Lahore.\n\n"
            "Privacy policy\n"
        )
        evidence = extract_primary_evidence(payload)
        self.assertEqual(evidence["evidence_mode"], "projection_degraded_text")
        self.assertTrue(evidence["degraded"])
        combined = " ".join(evidence["headings"] + evidence["primary_text"])
        self.assertIn("Mobile Veterinary Visits in Lahore", combined)
        self.assertNotIn("Privacy policy", combined)

    def test_onpage_http_failure_is_rejected(self):
        payload = json.loads(json.dumps(self.payload["content_parsing"]))
        payload["tasks"][0]["result"][0]["items"][0]["status_code"] = 404
        with self.assertRaises(ContractError):
            extract_primary_evidence(payload)


class CostTests(unittest.TestCase):
    def test_task_cost_is_used_once_instead_of_envelope_cost(self):
        payload = {"cost": 9, "tasks": [{"cost": 0.00625}, {"cost": 0.004}]}
        total, complete = collect_cost(payload)
        self.assertEqual(total, Decimal("0.01025"))
        self.assertTrue(complete)
        self.assertEqual(format_cost(total), "0,01 USD")

    def test_missing_task_cost_marks_total_incomplete(self):
        total, complete = collect_cost({"tasks": [{"cost": 0.01}, {}]})
        self.assertEqual(total, Decimal("0.01"))
        self.assertFalse(complete)

    def test_multiple_response_costs_sum_unrounded_then_format_once(self):
        total, complete = collect_costs(
            [
                {"tasks": [{"cost": 0.0049}]},
                {"tasks": [{"cost": 0.0049}]},
            ]
        )
        self.assertEqual(total, Decimal("0.0098"))
        self.assertTrue(complete)
        self.assertEqual(format_cost(total), "0,01 USD")

    def test_invalid_cost_is_rejected(self):
        with self.assertRaises(ContractError):
            collect_cost({"tasks": [{"cost": -0.01}]})


if __name__ == "__main__":
    unittest.main()
