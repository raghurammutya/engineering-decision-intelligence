import json
import tempfile
import unittest
from pathlib import Path

from tools.autopilot_progress import (
    completion_summary,
    load_backlog,
    mission_completion_delta,
    next_mission,
    render_mission_checklist,
    render_mission_summary,
    write_outputs,
)


class AutopilotProgressTests(unittest.TestCase):
    def test_backlog_calculates_current_completion(self) -> None:
        data = load_backlog(Path("roadmap/autopilot-backlog.json"))

        summary = completion_summary(data)

        self.assertEqual(summary["total_weight"], 100.0)
        self.assertGreater(summary["completion_percent"], 0)
        self.assertLess(summary["completion_percent"], 100)

    def test_next_mission_is_dependency_ready(self) -> None:
        data = load_backlog(Path("roadmap/autopilot-backlog.json"))

        mission = next_mission(data)

        self.assertIsNotNone(mission)
        assert mission is not None
        self.assertEqual(mission["id"], "graph-v2-decision-relationships")

    def test_outputs_include_progress_and_next_mission(self) -> None:
        data = load_backlog(Path("roadmap/autopilot-backlog.json"))
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)

            write_outputs(data, out, "2026-05-23T00:00:00+00:00")

            progress = json.loads((out / "progress.json").read_text(encoding="utf-8"))
            markdown = (out / "progress.md").read_text(encoding="utf-8")
            expected = completion_summary(data)["completion_percent"]
            self.assertEqual(progress["completion"]["completion_percent"], expected)
            self.assertEqual(progress["next_recommended_mission"]["id"], "graph-v2-decision-relationships")
            self.assertIn(f"Completion against product vision: `{expected}%`", markdown)

    def test_next_mission_exposes_safe_plan_boundary(self) -> None:
        data = load_backlog(Path("roadmap/autopilot-backlog.json"))
        mission = next_mission(data)
        assert mission is not None

        summary = render_mission_summary(data, "2026-05-23T00:00:00+00:00")
        checklist = render_mission_checklist(data, "2026-05-23T00:00:00+00:00")

        self.assertEqual(mission_completion_delta(data, mission), 6.0)
        self.assertIn("Safe mode: plan_only", summary)
        self.assertIn("/home/stocksadmin/workspace/ML/**", summary)
        self.assertIn("It does not edit files, mutate external systems, or touch blocked paths.", checklist)
        self.assertIn("- [ ] No blocked path was modified.", checklist)

    def test_progress_outputs_include_next_mission_artifacts(self) -> None:
        data = load_backlog(Path("roadmap/autopilot-backlog.json"))
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)

            write_outputs(data, out, "2026-05-23T00:00:00+00:00")

            self.assertTrue((out / "next-mission-checklist.md").exists())
            self.assertTrue((out / "next-mission.json").exists())


if __name__ == "__main__":
    unittest.main()
