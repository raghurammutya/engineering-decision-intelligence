"""Run the local pre-runtime DIP trust-loop fixture."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

from edi.dip_contracts import validate_contract_artifacts


TRUST_LOOP_FILES = [
    "case-evidence.json",
    "replay-result.json",
    "trust-loop-run.json",
    "dip-mvp-acceptance.json",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def trust_loop_payload(root: Path) -> dict[str, Any]:
    validation = validate_contract_artifacts(root)
    case_evidence = load_json(root / "dip/examples/support-ticket-case-evidence.json")
    replay_result = load_json(root / "dip/examples/support-ticket-replay-result.json")
    run = load_json(root / "dip/examples/support-ticket-trust-loop-run.json")
    acceptance = load_json(root / "dip/examples/dip-mvp-acceptance.json")
    complete = (
        validation["all_contracts_valid"]
        and acceptance.get("trust_loop_complete") is True
        and acceptance.get("runtime_integration_authorized") is False
        and acceptance.get("production_decision_execution_authorized") is False
    )
    return {
        "trust_loop_complete": complete,
        "runtime_execution_requested": run.get("runtime_execution_requested", True),
        "case_evidence": case_evidence,
        "replay_result": replay_result,
        "trust_loop_run": run,
        "dip_mvp_acceptance": acceptance,
        "contract_validation": validation,
    }


def write_trust_loop_outputs(root: Path, out: Path) -> dict[str, Any]:
    payload = trust_loop_payload(root)
    write_json(out / "case-evidence.json", payload["case_evidence"])
    write_json(out / "replay-result.json", payload["replay_result"])
    write_json(out / "trust-loop-run.json", payload["trust_loop_run"])
    write_json(out / "dip-mvp-acceptance.json", payload["dip_mvp_acceptance"])
    return payload


def check_trust_loop_outputs(root: Path, out: Path) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        temp_out = Path(tmp) / "trust-loop"
        write_trust_loop_outputs(root, temp_out)
        for filename in TRUST_LOOP_FILES:
            current = (out / filename).read_text(encoding="utf-8")
            expected = (temp_out / filename).read_text(encoding="utf-8")
            if current != expected:
                raise SystemExit(f"DIP trust-loop drift detected: {filename}")
    return True
