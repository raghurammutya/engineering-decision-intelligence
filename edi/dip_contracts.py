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
    "decision-diff-v1": "dip/contracts/decision-diff-v1.json",
    "approval-record-contract-v1": "dip/contracts/approval-record-v1.json",
    "case-evidence-pack-v1": "dip/contracts/case-evidence-pack-v1.json",
    "replay-reader-v1": "dip/contracts/replay-result-v1.json",
    "marketplace-governance-contract-v1": "dip/contracts/marketplace-governance-v1.json",
    "shared-context-governance-contract-v1": "dip/contracts/shared-context-governance-v1.json",
    "mvp-trust-loop-cli-v1": "dip/contracts/trust-loop-run-v1.json",
    "dip-mvp-acceptance-pack-v1": "dip/contracts/dip-mvp-acceptance-v1.json",
}

EXAMPLE_FILES = {
    "decision-spec-contract-v1": "dip/examples/support-ticket-routing-decision-spec.json",
    "capability-registry-contract-v1": "dip/examples/support-ticket-capability-registry.json",
    "policy-preflight-contract-v1": "dip/examples/support-ticket-policy-preflight.json",
    "simulation-evidence-contract-v1": "dip/examples/support-ticket-simulation-evidence.json",
    "decision-diff-v1": "dip/examples/support-ticket-decision-diff.json",
    "approval-record-contract-v1": "dip/examples/support-ticket-approval-record.json",
    "case-evidence-pack-v1": "dip/examples/support-ticket-case-evidence.json",
    "replay-reader-v1": "dip/examples/support-ticket-replay-result.json",
    "marketplace-governance-contract-v1": "dip/examples/support-ticket-marketplace-governance.json",
    "shared-context-governance-contract-v1": "dip/examples/support-ticket-shared-context-governance.json",
    "mvp-trust-loop-cli-v1": "dip/examples/support-ticket-trust-loop-run.json",
    "dip-mvp-acceptance-pack-v1": "dip/examples/dip-mvp-acceptance.json",
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


def validate_required_fields(example: dict[str, Any], contract: dict[str, Any], label: str) -> list[str]:
    return [f"missing {label} field: {field}" for field in missing_fields(example, contract["required_fields"])]


def validate_decision_diff(example: dict[str, Any], contract: dict[str, Any]) -> list[str]:
    errors = validate_required_fields(example, contract, "decision diff")
    if not isinstance(example.get("changed_outcome_count"), int):
        errors.append("decision diff changed_outcome_count must be an integer")
    return errors


def validate_approval_record(example: dict[str, Any], contract: dict[str, Any]) -> list[str]:
    errors = validate_required_fields(example, contract, "approval")
    if example.get("ai_approved") is not False:
        errors.append("approval record must not be AI-approved")
    if example.get("decision") not in contract.get("allowed_decisions", []):
        errors.append("approval decision is not allowed")
    return errors


def validate_case_evidence(example: dict[str, Any], contract: dict[str, Any]) -> list[str]:
    errors = validate_required_fields(example, contract, "case evidence")
    if example.get("storage_mode") not in contract.get("allowed_storage_modes", []):
        errors.append("case evidence storage mode is not allowed")
    if example.get("mutable") is not False:
        errors.append("case evidence must be immutable or append-only")
    return errors


def validate_replay_result(example: dict[str, Any], contract: dict[str, Any]) -> list[str]:
    errors = validate_required_fields(example, contract, "replay")
    if example.get("side_effects_executed") is not False:
        errors.append("replay must not execute side effects")
    return errors


def validate_trust_loop_run(example: dict[str, Any], contract: dict[str, Any]) -> list[str]:
    errors = validate_required_fields(example, contract, "trust loop")
    required_steps = contract.get("required_steps", [])
    completed_steps = example.get("completed_steps", [])
    missing_steps = [step for step in required_steps if step not in completed_steps]
    errors.extend(f"missing trust loop step: {step}" for step in missing_steps)
    if example.get("runtime_execution_requested") is not False:
        errors.append("trust loop must not request runtime execution")
    return errors


def validate_marketplace_governance(example: dict[str, Any], contract: dict[str, Any]) -> list[str]:
    errors = validate_required_fields(example, contract, "marketplace governance")
    if example.get("runtime_invocation_allowed") is not False:
        errors.append("marketplace governance fixture must not allow runtime invocation")
    return errors


def validate_shared_context_governance(example: dict[str, Any], contract: dict[str, Any]) -> list[str]:
    errors = validate_required_fields(example, contract, "shared context governance")
    if example.get("runtime_exchange_allowed") is not False:
        errors.append("shared context fixture must not allow runtime exchange")
    return errors


def validate_mvp_acceptance(example: dict[str, Any], contract: dict[str, Any]) -> list[str]:
    errors = validate_required_fields(example, contract, "DIP MVP acceptance")
    if example.get("runtime_integration_authorized") is not False:
        errors.append("DIP MVP acceptance must not authorize runtime integration")
    if example.get("production_decision_execution_authorized") is not False:
        errors.append("DIP MVP acceptance must not authorize production decision execution")
    return errors


def validate_contract_artifacts(root: Path) -> dict[str, Any]:
    validators = {
        "decision-spec-contract-v1": validate_decision_spec,
        "capability-registry-contract-v1": validate_capability_registry,
        "policy-preflight-contract-v1": validate_policy_preflight,
        "simulation-evidence-contract-v1": validate_simulation_evidence,
        "decision-diff-v1": validate_decision_diff,
        "approval-record-contract-v1": validate_approval_record,
        "case-evidence-pack-v1": validate_case_evidence,
        "replay-reader-v1": validate_replay_result,
        "marketplace-governance-contract-v1": validate_marketplace_governance,
        "shared-context-governance-contract-v1": validate_shared_context_governance,
        "mvp-trust-loop-cli-v1": validate_trust_loop_run,
        "dip-mvp-acceptance-pack-v1": validate_mvp_acceptance,
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
