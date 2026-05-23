"""Validate local DIP contract artifacts used as pre-runtime evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


CONTRACT_FILES = {
    "decision-spec-contract-v1": "dip/contracts/decision-spec-v1.json",
    "capability-registry-contract-v1": "dip/contracts/capability-registry-v1.json",
    "policy-preflight-contract-v1": "dip/contracts/policy-preflight-v1.json",
    "simulation-evidence-contract-v1": "dip/contracts/simulation-evidence-v1.json",
}

EXAMPLE_FILES = {
    "decision-spec-contract-v1": "dip/examples/support-ticket-routing-decision-spec.json",
    "capability-registry-contract-v1": "dip/examples/support-ticket-capability-registry.json",
    "policy-preflight-contract-v1": "dip/examples/support-ticket-policy-preflight.json",
    "simulation-evidence-contract-v1": "dip/examples/support-ticket-simulation-evidence.json",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def missing_fields(payload: dict[str, Any], required_fields: list[str]) -> list[str]:
    return [field for field in required_fields if field not in payload]


def validate_decision_spec(example: dict[str, Any], contract: dict[str, Any]) -> list[str]:
    errors = [f"missing decision spec field: {field}" for field in missing_fields(example, contract["required_fields"])]
    if example.get("environment_scope", {}).get("production_allowed") is not False:
        errors.append("decision spec must default production_allowed to false")
    allowed_labels = set(contract.get("source_labels", []))
    labels = set(example.get("source_labels", []))
    if not labels or not labels.issubset(allowed_labels):
        errors.append("decision spec source labels must be declared and allowed")
    return errors


def validate_capability_registry(example: dict[str, Any], contract: dict[str, Any]) -> list[str]:
    records = example.get("capabilities", [])
    errors: list[str] = []
    if not records:
        return ["capability registry must include capabilities"]
    for record in records:
        for field in contract["required_fields"]:
            if field not in record:
                errors.append(f"missing capability field: {field}")
    return errors


def validate_policy_preflight(example: dict[str, Any], contract: dict[str, Any]) -> list[str]:
    errors = [f"missing preflight field: {field}" for field in missing_fields(example, contract["required_fields"])]
    if example.get("result") not in contract.get("allowed_results", []):
        errors.append("preflight result must be allowed, denied, or approval_required")
    if example.get("ai_override_allowed") is not False:
        errors.append("AI override must be false for preflight decisions")
    return errors


def validate_simulation_evidence(example: dict[str, Any], contract: dict[str, Any]) -> list[str]:
    errors = [f"missing simulation field: {field}" for field in missing_fields(example, contract["required_fields"])]
    if not isinstance(example.get("changed_outcome_count"), int):
        errors.append("changed_outcome_count must be an integer")
    if not example.get("case_set"):
        errors.append("case_set is required")
    return errors


def validate_contract_artifacts(root: Path) -> dict[str, Any]:
    validators = {
        "decision-spec-contract-v1": validate_decision_spec,
        "capability-registry-contract-v1": validate_capability_registry,
        "policy-preflight-contract-v1": validate_policy_preflight,
        "simulation-evidence-contract-v1": validate_simulation_evidence,
    }
    records = []
    for contract_id, contract_file in CONTRACT_FILES.items():
        example_file = EXAMPLE_FILES[contract_id]
        contract_path = root / contract_file
        example_path = root / example_file
        errors = []
        if not contract_path.exists():
            errors.append("contract file missing")
        if not example_path.exists():
            errors.append("example file missing")
        if not errors:
            contract = load_json(contract_path)
            example = load_json(example_path)
            errors.extend(validators[contract_id](example, contract))
        records.append(
            {
                "slice_id": contract_id,
                "contract_path": contract_file,
                "example_path": example_file,
                "passed": not errors,
                "errors": errors,
            }
        )
    passed_count = len([record for record in records if record["passed"]])
    return {
        "contract_count": len(records),
        "passed_contract_count": passed_count,
        "all_contracts_valid": passed_count == len(records),
        "records": records,
    }
