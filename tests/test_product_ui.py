import tempfile
import unittest
from pathlib import Path

from edi.product_api import build_snapshot
from edi.product_ui import render_operator_view, write_operator_view


class ProductUiTests(unittest.TestCase):
    def test_render_operator_view_uses_snapshot_sections(self) -> None:
        snapshot = build_snapshot(Path("."), "2026-05-23T00:00:00+00:00")

        html = render_operator_view(snapshot)

        self.assertIn("Engineering Decision Intelligence", html)
        self.assertIn("Product completion", html)
        self.assertIn("Next mission", html)
        self.assertIn("Top Decisions", html)
        self.assertIn("Telemetry correlations", html)
        self.assertIn("Scanner tuning candidates", html)

    def test_write_operator_view_materializes_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "operator.html"

            write_operator_view(Path("."), out, "2026-05-23T00:00:00+00:00")

            self.assertTrue(out.exists())
            self.assertIn("<!doctype html>", out.read_text(encoding="utf-8").lower())


if __name__ == "__main__":
    unittest.main()
