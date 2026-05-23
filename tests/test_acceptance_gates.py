import json
import unittest

from tools.acceptance_gates import (
    REQUIRED_GRAPH_ENTITY_TYPES,
    REQUIRED_GRAPH_RELATIONSHIPS,
    ROOT,
    check_cli_contracts,
    check_graph_contracts,
    check_export_contracts,
    check_packaging_contract,
    check_progress_freshness,
    check_product_api_contract,
    check_product_ui_contract,
    check_v1_5_backlog_contract,
    check_v2_backlog_contract,
    check_report_contracts,
    load_json,
)


class AcceptanceGatesTests(unittest.TestCase):
    def test_cli_contracts_are_stable(self) -> None:
        check_cli_contracts()

    def test_required_reports_exist(self) -> None:
        check_report_contracts()

    def test_graph_contracts_are_satisfied(self) -> None:
        check_graph_contracts()

    def test_export_contracts_are_satisfied(self) -> None:
        check_export_contracts()

    def test_progress_freshness_gate_passes(self) -> None:
        check_progress_freshness()

    def test_packaging_contract_is_satisfied(self) -> None:
        check_packaging_contract()

    def test_product_api_contract_is_satisfied(self) -> None:
        check_product_api_contract()

    def test_product_ui_contract_is_satisfied(self) -> None:
        check_product_ui_contract()

    def test_v1_5_backlog_contract_is_satisfied(self) -> None:
        check_v1_5_backlog_contract()

    def test_v2_backlog_contract_is_satisfied(self) -> None:
        check_v2_backlog_contract()

    def test_ml_pilot_graph_contains_required_contract_terms(self) -> None:
        entities = load_json(ROOT / "reports" / "ml-pilot" / "graph" / "entities.json")
        relationships = load_json(ROOT / "reports" / "ml-pilot" / "graph" / "relationships.json")
        entity_types = {entity["type"] for entity in entities}
        relationship_types = {relationship["relation"] for relationship in relationships}

        self.assertTrue(REQUIRED_GRAPH_ENTITY_TYPES.issubset(entity_types))
        self.assertTrue(REQUIRED_GRAPH_RELATIONSHIPS.issubset(relationship_types))

    def test_autopilot_next_mission_is_plan_only(self) -> None:
        next_mission = json.loads((ROOT / "reports" / "product" / "next-mission.json").read_text(encoding="utf-8"))

        self.assertEqual(next_mission["safe_mode"], "plan_only")
        if next_mission.get("mission") is not None:
            self.assertIn("/home/stocksadmin/workspace/ML/**", next_mission["blocked_paths"])
        else:
            self.assertIn("No dependency-ready planned mission", next_mission["reason"])


if __name__ == "__main__":
    unittest.main()
