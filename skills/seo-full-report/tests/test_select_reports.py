#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "select_reports.py"
SPEC = importlib.util.spec_from_file_location("select_reports", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SelectReportsTest(unittest.TestCase):
    def test_normalizes_http_url(self) -> None:
        self.assertEqual(MODULE.normalize_domain("https://www.Example.com/path"), "example.com")

    def test_rejects_invalid_port(self) -> None:
        with self.assertRaises(argparse.ArgumentTypeError):
            MODULE.normalize_domain("example.com:not-a-port")

    def test_selects_inclusive_range_and_excludes_prior_full_report(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            directory = root / "example.com"
            directory.mkdir()
            for name in (
                "2026-06-19_Technical_example.com.md",
                "2026-06-20_Rankings_example.com.md",
                "2026-06-20_Full-SEO-Report_example.com_2026-06-19.md",
                "2026-06-21_Content_example.com.md",
                "notes.md",
            ):
                (directory / name).write_text(name)

            args = MODULE.build_parser().parse_args(
                [
                    "example.com",
                    "--start-date",
                    "2026-06-19",
                    "--end-date",
                    "2026-06-20",
                    "--root",
                    str(root),
                ]
            )
            start, end = MODULE.resolve_dates(MODULE.build_parser(), args)
            result = MODULE.select(args, start, end)

            self.assertEqual(result["selected_count"], 2)
            self.assertEqual(
                [item["filename"] for item in result["selected"]],
                ["2026-06-19_Technical_example.com.md", "2026-06-20_Rankings_example.com.md"],
            )
            self.assertEqual(
                result["excluded_full_reports"],
                ["2026-06-20_Full-SEO-Report_example.com_2026-06-19.md"],
            )

    def test_missing_directory_returns_empty_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parser = MODULE.build_parser()
            args = parser.parse_args(
                ["example.org", "--date", "2026-06-22", "--root", temporary]
            )
            start, end = MODULE.resolve_dates(parser, args)
            result = MODULE.select(args, start, end)
            self.assertFalse(result["directory_exists"])
            self.assertEqual(result["selected"], [])


if __name__ == "__main__":
    unittest.main()
