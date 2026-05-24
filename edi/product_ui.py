"""Generate a static operator view from the Product API snapshot."""

from __future__ import annotations

import html
from pathlib import Path
from typing import Any

from edi.product_api import build_snapshot


def _text(value: Any) -> str:
    return html.escape(str(value))


def _mission_id(snapshot: dict[str, Any]) -> str:
    mission = snapshot.get("product", {}).get("next_recommended_mission")
    if isinstance(mission, dict):
        return str(mission.get("id", "none"))
    return "none"


def _lane_label(lane: Any) -> str:
    if isinstance(lane, dict):
        name = lane.get("lane", "unknown")
        count = lane.get("count", 0)
        risk = lane.get("highest_risk", "unknown")
        return f"{name}: {count} items, highest risk {risk}"
    return str(lane)


def _summary_label(value: Any) -> str:
    if isinstance(value, dict):
        return ", ".join(f"{key}={item}" for key, item in sorted(value.items()))
    return str(value)


def render_operator_view(snapshot: dict[str, Any]) -> str:
    product = snapshot["product"]
    executive = snapshot["executive"]
    risk = snapshot["risk"]
    ai_agents = snapshot.get("ai_agents", {})
    scanner_tuning = snapshot.get("scanner_tuning", {})
    operationalization = snapshot.get("operationalization", {})
    v2 = snapshot.get("v2", {})
    v3 = snapshot.get("v3", {})
    v4 = snapshot.get("v4", {})
    v5 = snapshot.get("v5", {})
    substrate = snapshot.get("substrate", {})
    dip = snapshot.get("dip", {})
    top_decisions = executive.get("top_decisions", [])[:10]
    action_lanes = executive.get("action_lanes", [])
    owner_counts = risk.get("owner_review_counts", {})
    telemetry_summary = risk.get("telemetry_summary", {})

    decision_rows = "\n".join(
        "<tr>"
        f"<td>{_text(row.get('priority', ''))}</td>"
        f"<td>{_text(row.get('risk_level', ''))}</td>"
        f"<td>{_text(row.get('path', ''))}</td>"
        f"<td>{_text(row.get('next_action', ''))}</td>"
        "</tr>"
        for row in top_decisions
    ) or '<tr><td colspan="4">No decision records available.</td></tr>'

    lane_items = "\n".join(f"<li>{_text(_lane_label(lane))}</li>" for lane in action_lanes) or "<li>No action lanes available.</li>"
    owner_items = "\n".join(
        f"<li><strong>{_text(key)}</strong>: {_text(value)}</li>"
        for key, value in sorted(owner_counts.items())
    ) or "<li>No owner review counts available.</li>"
    telemetry_items = "\n".join(
        f"<li><strong>{_text(key)}</strong>: {_text(_summary_label(value))}</li>"
        for key, value in sorted(telemetry_summary.items())
    ) or "<li>No telemetry summary available.</li>"

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Engineering Decision Intelligence Operator View</title>
  <style>
    body {{
      margin: 0;
      font-family: Arial, sans-serif;
      color: #172026;
      background: #f4f7f9;
    }}
    header {{
      background: #17324d;
      color: white;
      padding: 24px 32px;
    }}
    main {{
      padding: 24px 32px 40px;
      max-width: 1180px;
      margin: 0 auto;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
      gap: 12px;
      margin: 20px 0;
    }}
    .metric, section {{
      background: white;
      border: 1px solid #d7e0e7;
      border-radius: 6px;
      padding: 16px;
    }}
    .metric strong {{
      display: block;
      font-size: 28px;
      margin-top: 6px;
    }}
    section {{
      margin-top: 16px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}
    th, td {{
      text-align: left;
      border-bottom: 1px solid #d7e0e7;
      padding: 10px 8px;
      vertical-align: top;
    }}
    th {{
      background: #edf2f5;
    }}
    .columns {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Engineering Decision Intelligence</h1>
    <p>Generated: {_text(snapshot.get('generated_at', 'unknown'))}</p>
  </header>
  <main>
    <div class="metrics">
      <div class="metric">Product completion<strong>{_text(product.get('completion_percent'))}%</strong></div>
      <div class="metric">Next mission<strong>{_text(_mission_id(snapshot))}</strong></div>
      <div class="metric">Runtime signals<strong>{_text(risk.get('runtime_signal_count'))}</strong></div>
      <div class="metric">Telemetry correlations<strong>{_text(risk.get('telemetry_correlation_count'))}</strong></div>
      <div class="metric">AI-agent surfaces<strong>{_text(ai_agents.get('capability_count', 0))}</strong></div>
      <div class="metric">Scanner tuning candidates<strong>{_text(scanner_tuning.get('candidate_count', 0))}</strong></div>
      <div class="metric">Review workflow items<strong>{_text(operationalization.get('review_workflow_count', 0))}</strong></div>
      <div class="metric">v1.5 acceptance<strong>{_text(operationalization.get('v1_5_acceptance_state', 'unknown'))}</strong></div>
      <div class="metric">V2 completion<strong>{_text(v2.get('completion_percent', 0))}%</strong></div>
      <div class="metric">V2 acceptance<strong>{_text(v2.get('acceptance_state', 'unknown'))}</strong></div>
      <div class="metric">Portfolio repos<strong>{_text(v2.get('portfolio_repo_count', 0))}</strong></div>
      <div class="metric">Policy preflight<strong>{_text(v2.get('preflight_decision_count', 0))}</strong></div>
      <div class="metric">V3 completion<strong>{_text(v3.get('completion_percent', 0))}%</strong></div>
      <div class="metric">V3 acceptance<strong>{_text(v3.get('acceptance_state', 'unknown'))}</strong></div>
      <div class="metric">Connectors<strong>{_text(v3.get('connector_count', 0))}</strong></div>
      <div class="metric">Reconciliation loops<strong>{_text(v3.get('reconciliation_loop_count', 0))}</strong></div>
      <div class="metric">V4 completion<strong>{_text(v4.get('completion_percent', 0))}%</strong></div>
      <div class="metric">V4 acceptance<strong>{_text(v4.get('acceptance_state', 'unknown'))}</strong></div>
      <div class="metric">Live connector configs<strong>{_text(v4.get('connector_count', 0))}</strong></div>
      <div class="metric">Operational SLOs<strong>{_text(v4.get('slo_count', 0))}</strong></div>
      <div class="metric">V5 tooling<strong>{_text(v5.get('tooling_completion_percent', 0))}%</strong></div>
      <div class="metric">V5 live claims<strong>{_text(v5.get('live_claim_completion_percent', 0))}%</strong></div>
      <div class="metric">Substrate policy<strong>{_text(substrate.get('policy_completion_percent', 0))}%</strong></div>
      <div class="metric">Substrate live evidence<strong>{_text(substrate.get('live_evidence_completion_percent', 0))}%</strong></div>
      <div class="metric">DIP v0.1 skeleton<strong>{_text(dip.get('v0_1_pre_runtime_trust_loop_skeleton_percent', 0))}%</strong></div>
      <div class="metric">DIP policy engine<strong>{_text(dip.get('deterministic_policy_engine_readiness_percent', 0))}%</strong></div>
      <div class="metric">DIP case store<strong>{_text(dip.get('durable_case_store_readiness_percent', 0))}%</strong></div>
      <div class="metric">DIP v0.2 backlog<strong>{_text(dip.get('v0_2_backlog_defined_percent', 0))}%</strong></div>
      <div class="metric">DIP v0.3 evidence<strong>{_text(dip.get('v0_3_computed_policy_diff_evidence_percent', 0))}%</strong></div>
      <div class="metric">DIP v0.4 simulation<strong>{_text(dip.get('v0_4_computed_simulation_evidence_percent', 0))}%</strong></div>
      <div class="metric">DIP v0.5 durable evidence<strong>{_text(dip.get('v0_5_durable_case_approval_evidence_percent', 0))}%</strong></div>
      <div class="metric">DIP v0.6 identity evidence<strong>{_text(dip.get('v0_6_identity_rbac_approval_evidence_percent', 0))}%</strong></div>
      <div class="metric">DIP v0.7 repo governance<strong>{_text(dip.get('v0_7_repository_governance_evidence_percent', 0))}%</strong></div>
      <div class="metric">DIP v0.8 release lifecycle<strong>{_text(dip.get('v0_8_release_lifecycle_evidence_percent', 0))}%</strong></div>
      <div class="metric">DIP v0.9 identity contract<strong>{_text(dip.get('v0_9_external_identity_contract_evidence_percent', 0))}%</strong></div>
      <div class="metric">DIP v1.0 durable store<strong>{_text(dip.get('v1_0_durable_store_contract_evidence_percent', 0))}%</strong></div>
      <div class="metric">DIP v1.2 review surface<strong>{_text(dip.get('v1_2_product_review_surface_evidence_percent', 0))}%</strong></div>
      <div class="metric">DIP v1.4 capability governance<strong>{_text(dip.get('v1_4_capability_governance_evidence_percent', 0))}%</strong></div>
      <div class="metric">DIP v1.5 shared context<strong>{_text(dip.get('v1_5_shared_context_contract_evidence_percent', 0))}%</strong></div>
      <div class="metric">DIP v2.0 runtime assessment<strong>{_text(dip.get('v2_0_runtime_readiness_assessment_percent', 0))}%</strong></div>
      <div class="metric">DIP v2.1 exception/schema<strong>{_text(dip.get('v2_1_governed_exception_schema_stability_percent', 0))}%</strong></div>
      <div class="metric">DIP v2.2 approval boundary<strong>{_text(dip.get('v2_2_external_approval_boundary_percent', 0))}%</strong></div>
      <div class="metric">DIP v2.3 store adapter<strong>{_text(dip.get('v2_3_durable_case_store_adapter_percent', 0))}%</strong></div>
      <div class="metric">DIP v2.4 adapter parity<strong>{_text(dip.get('v2_4_evidence_store_adapter_parity_percent', 0))}%</strong></div>
      <div class="metric">DIP v2.5 policy engine<strong>{_text(dip.get('v2_5_policy_engine_hardening_percent', 0))}%</strong></div>
      <div class="metric">DIP v2.6 approval adapter<strong>{_text(dip.get('v2_6_external_approval_adapter_percent', 0))}%</strong></div>
      <div class="metric">DIP v2.7 live RBAC<strong>{_text(dip.get('v2_7_live_identity_rbac_percent', 0))}%</strong></div>
      <div class="metric">DIP v2.8 backend<strong>{_text(dip.get('v2_8_durable_evidence_backend_percent', 0))}%</strong></div>
      <div class="metric">DIP v2.9 promotion<strong>{_text(dip.get('v2_9_release_promotion_rollback_percent', 0))}%</strong></div>
      <div class="metric">DIP v3.0 GA<strong>{_text(dip.get('v3_0_pre_runtime_ga_percent', 0))}%</strong></div>
      <div class="metric">DIP v3.5 controls<strong>{_text(dip.get('v3_5_runtime_control_plane_design_percent', 0))}%</strong></div>
      <div class="metric">DIP v4.0 gate<strong>{_text(dip.get('v4_0_limited_runtime_authority_gate_percent', 0))}%</strong></div>
      <div class="metric">DIP v5.0 advisory<strong>{_text(dip.get('v5_0_governed_advisory_runtime_percent', 0))}%</strong></div>
      <div class="metric">DIP v6.0 hardening<strong>{_text(dip.get('v6_0_platform_hardening_assessment_percent', 0))}%</strong></div>
      <div class="metric">DIP v6.1 identity authority<strong>{_text(dip.get('v6_1_live_identity_authority_percent', 0))}%</strong></div>
      <div class="metric">DIP v6.2 approval provider<strong>{_text(dip.get('v6_2_live_decision_approval_provider_percent', 0))}%</strong></div>
      <div class="metric">DIP v6.3 durable store<strong>{_text(dip.get('v6_3_production_durable_case_store_percent', 0))}%</strong></div>
      <div class="metric">DIP v6.4 promotion chain<strong>{_text(dip.get('v6_4_production_promotion_chain_percent', 0))}%</strong></div>
      <div class="metric">DIP v7.0 pilot gate<strong>{_text(dip.get('v7_0_controlled_runtime_pilot_percent', 0))}%</strong></div>
      <div class="metric">DIP v7.5 marketplace<strong>{_text(dip.get('v7_5_marketplace_runtime_governance_percent', 0))}%</strong></div>
      <div class="metric">DIP v8.0 shared context<strong>{_text(dip.get('v8_0_shared_context_runtime_governance_percent', 0))}%</strong></div>
      <div class="metric">DIP v9.0 authority review<strong>{_text(dip.get('v9_0_production_authority_readiness_review_percent', 0))}%</strong></div>
      <div class="metric">DIP v10.0 plan review<strong>{_text(dip.get('v10_0_completion_plan_execution_percent', 0))}%</strong></div>
      <div class="metric">DIP v11.0 API foundation<strong>{_text(dip.get('v11_0_api_first_platform_foundation_percent', 0))}%</strong></div>
      <div class="metric">DIP v15.0 API foundation<strong>{_text(dip.get('v15_0_api_foundation_percent', 0))}%</strong></div>
      <div class="metric">DIP v20.0 architecture<strong>{_text(dip.get('v20_0_architecture_closure_percent', 0))}%</strong></div>
      <div class="metric">DIP v25.0 contracts<strong>{_text(dip.get('v25_0_contract_closure_percent', 0))}%</strong></div>
      <div class="metric">DIP pre-runtime scope<strong>{_text(dip.get('pre_runtime_completion_scope_percent', 0))}%</strong></div>
      <div class="metric">DIP target evidence<strong>{_text(dip.get('target_repo_evidence_percent', 0))}%</strong></div>
      <div class="metric">DIP governance clean<strong>{_text(dip.get('target_repo_governance_clean_percent', 0))}%</strong></div>
    </div>
    <section>
      <h2>Top Decisions</h2>
      <table>
        <thead><tr><th>Priority</th><th>Risk</th><th>Path</th><th>Next Action</th></tr></thead>
        <tbody>{decision_rows}</tbody>
      </table>
    </section>
    <div class="columns">
      <section>
        <h2>Action Lanes</h2>
        <ul>{lane_items}</ul>
      </section>
      <section>
        <h2>Owner Review Counts</h2>
        <ul>{owner_items}</ul>
      </section>
      <section>
        <h2>Telemetry Summary</h2>
        <ul>{telemetry_items}</ul>
      </section>
      <section>
        <h2>V2 Operational Intelligence</h2>
        <ul>
          <li><strong>Portfolio artifacts</strong>: {_text(v2.get('portfolio_artifact_count', 0))}</li>
          <li><strong>Low-confidence high-risk</strong>: {_text(v2.get('low_confidence_high_risk_count', 0))}</li>
          <li><strong>Lineage gaps</strong>: {_text(v2.get('lineage_gap_count', 0))}</li>
        </ul>
      </section>
      <section>
        <h2>V3 Operationalization</h2>
        <ul>
          <li><strong>Connector records</strong>: {_text(v3.get('connector_record_count', 0))}</li>
          <li><strong>Divergences</strong>: {_text(v3.get('divergence_count', 0))}</li>
          <li><strong>Preflight CI records</strong>: {_text(v3.get('preflight_ci_record_count', 0))}</li>
          <li><strong>Pilot state</strong>: {_text(v3.get('pilot_state', 'unknown'))}</li>
        </ul>
      </section>
      <section>
        <h2>V4 Live Enforcement Readiness</h2>
        <ul>
          <li><strong>Ready connector configs</strong>: {_text(v4.get('ready_for_install_count', 0))}</li>
          <li><strong>CI target state</strong>: {_text(v4.get('ci_target_state', 'unknown'))}</li>
          <li><strong>Reconciliation loops</strong>: {_text(v4.get('reconciliation_loop_count', 0))}</li>
        </ul>
      </section>
      <section>
        <h2>V5 Target Installation</h2>
        <ul>
          <li><strong>1Password CLI installed</strong>: {_text(v5.get('op_installed', False))}</li>
          <li><strong>Secret references</strong>: {_text(v5.get('secret_reference_count', 0))}</li>
          <li><strong>Blocked live claims</strong>: {_text(len(v5.get('blocked_claims', [])))}</li>
        </ul>
      </section>
      <section>
        <h2>Operational Substrate</h2>
        <ul>
          <li><strong>Acceptance</strong>: {_text(substrate.get('acceptance_state', 'unknown'))}</li>
          <li><strong>Promotion order</strong>: {_text(' -> '.join(substrate.get('promotion_order', [])))}</li>
          <li><strong>Blocked substrate claims</strong>: {_text(len(substrate.get('blocked_claims', [])))}</li>
        </ul>
      </section>
      <section>
        <h2>Decision Intelligence Platform</h2>
        <ul>
          <li><strong>Acceptance</strong>: {_text(dip.get('acceptance_state', 'unknown'))}</li>
          <li><strong>Maturity claim</strong>: {_text(dip.get('maturity_claim', 'unknown'))}</li>
          <li><strong>First wedge</strong>: {_text(dip.get('first_wedge', 'unknown'))}</li>
          <li><strong>v0.1 skeleton</strong>: {_text(dip.get('v0_1_pre_runtime_trust_loop_skeleton_percent', 0))}%</li>
          <li><strong>v0.2 backlog</strong>: {_text(dip.get('v0_2_backlog_defined_percent', 0))}% ({_text(dip.get('v0_2_backlog_status_label', 'unknown'))})</li>
          <li><strong>Target repo evidence</strong>: {_text(dip.get('target_repo_evidence_percent', 0))}%</li>
          <li><strong>Target repo governance clean</strong>: {_text(dip.get('target_repo_governance_clean_percent', 0))}%</li>
          <li><strong>v0.8 release lifecycle</strong>: {_text(dip.get('v0_8_release_lifecycle_evidence_percent', 0))}% ({_text(dip.get('v0_8_status_label', 'unknown'))})</li>
          <li><strong>v0.9 external identity contract</strong>: {_text(dip.get('v0_9_external_identity_contract_evidence_percent', 0))}% ({_text(dip.get('v0_9_status_label', 'unknown'))})</li>
          <li><strong>v1.0 durable store contract</strong>: {_text(dip.get('v1_0_durable_store_contract_evidence_percent', 0))}% ({_text(dip.get('v1_0_status_label', 'unknown'))})</li>
          <li><strong>v1.1 governance parity</strong>: {_text(dip.get('v1_1_governance_enforcement_parity_percent', 0))}% ({_text(dip.get('v1_1_status_label', 'unknown'))})</li>
          <li><strong>v1.2 product review surface</strong>: {_text(dip.get('v1_2_product_review_surface_evidence_percent', 0))}% ({_text(dip.get('v1_2_status_label', 'unknown'))})</li>
          <li><strong>v1.3 multi-domain simulation</strong>: {_text(dip.get('v1_3_multi_domain_simulation_evidence_percent', 0))}% ({_text(dip.get('v1_3_status_label', 'unknown'))})</li>
          <li><strong>v1.4 capability governance</strong>: {_text(dip.get('v1_4_capability_governance_evidence_percent', 0))}% ({_text(dip.get('v1_4_status_label', 'unknown'))})</li>
          <li><strong>v1.5 shared context contract</strong>: {_text(dip.get('v1_5_shared_context_contract_evidence_percent', 0))}% ({_text(dip.get('v1_5_status_label', 'unknown'))})</li>
          <li><strong>v2.0 runtime assessment</strong>: {_text(dip.get('v2_0_runtime_readiness_assessment_percent', 0))}% ({_text(dip.get('v2_0_status_label', 'unknown'))})</li>
          <li><strong>v2.1 governed exception/schema stability</strong>: {_text(dip.get('v2_1_governed_exception_schema_stability_percent', 0))}% ({_text(dip.get('v2_1_status_label', 'unknown'))})</li>
          <li><strong>Independent human review observed</strong>: {_text(dip.get('independent_human_review_observed', False))}</li>
          <li><strong>v2.2 external approval boundary</strong>: {_text(dip.get('v2_2_external_approval_boundary_percent', 0))}% ({_text(dip.get('v2_2_status_label', 'unknown'))})</li>
          <li><strong>Live external approval observed</strong>: {_text(dip.get('live_external_approval_system_observed', False))}</li>
          <li><strong>v2.3 durable case store adapter</strong>: {_text(dip.get('v2_3_durable_case_store_adapter_percent', 0))}% ({_text(dip.get('v2_3_status_label', 'unknown'))})</li>
          <li><strong>Production durable store observed</strong>: {_text(dip.get('production_durable_case_store_backend_observed', False))}</li>
          <li><strong>v2.4 evidence store adapter parity</strong>: {_text(dip.get('v2_4_evidence_store_adapter_parity_percent', 0))}% ({_text(dip.get('v2_4_status_label', 'unknown'))})</li>
          <li><strong>Adapter runtime backend invoked</strong>: {_text(dip.get('adapter_runtime_backend_invoked', False))}</li>
          <li><strong>v2.5 policy engine hardening</strong>: {_text(dip.get('v2_5_policy_engine_hardening_percent', 0))}% ({_text(dip.get('v2_5_status_label', 'unknown'))})</li>
          <li><strong>Policy engine runtime authority observed</strong>: {_text(dip.get('policy_engine_runtime_authority_observed', False))}</li>
          <li><strong>v2.6 external approval adapter</strong>: {_text(dip.get('v2_6_external_approval_adapter_percent', 0))}% ({_text(dip.get('v2_6_status_label', 'unknown'))})</li>
          <li><strong>External approval adapter live system observed</strong>: {_text(dip.get('external_approval_adapter_live_system_observed', False))}</li>
          <li><strong>External approval adapter AI approval allowed</strong>: {_text(dip.get('external_approval_adapter_ai_approval_allowed', False))}</li>
          <li><strong>v2.7 live identity/RBAC</strong>: {_text(dip.get('v2_7_live_identity_rbac_percent', 0))}% ({_text(dip.get('v2_7_status_label', 'unknown'))})</li>
          <li><strong>Live identity RBAC</strong>: {_text(dip.get('live_identity_rbac_provider', 'unknown'))}/{_text(dip.get('live_identity_rbac_repository_permission', 'unknown'))}</li>
          <li><strong>Live identity RBAC MFA claim observed</strong>: {_text(dip.get('live_identity_rbac_mfa_claim_observed', False))}</li>
          <li><strong>v2.8 durable evidence backend</strong>: {_text(dip.get('v2_8_durable_evidence_backend_percent', 0))}% ({_text(dip.get('v2_8_status_label', 'unknown'))})</li>
          <li><strong>Durable backend runtime invoked</strong>: {_text(dip.get('durable_evidence_backend_runtime_invoked', False))}</li>
          <li><strong>v2.9 release promotion/rollback</strong>: {_text(dip.get('v2_9_release_promotion_rollback_percent', 0))}% ({_text(dip.get('v2_9_status_label', 'unknown'))})</li>
          <li><strong>Production deployment executed</strong>: {_text(dip.get('prod_deployment_executed', False))}</li>
          <li><strong>v3.0 pre-runtime GA</strong>: {_text(dip.get('v3_0_pre_runtime_ga_percent', 0))}% ({_text(dip.get('v3_0_status_label', 'unknown'))})</li>
          <li><strong>v3.1 governance closure</strong>: {_text(dip.get('v3_1_governance_closure_percent', 0))}% ({_text(dip.get('v3_1_status_label', 'unknown'))})</li>
          <li><strong>v3.2 external identity integration</strong>: {_text(dip.get('v3_2_external_identity_integration_percent', 0))}% ({_text(dip.get('v3_2_status_label', 'unknown'))})</li>
          <li><strong>v3.2 external identity live ready</strong>: {_text(dip.get('v3_2_external_identity_live_ready', False))}</li>
          <li><strong>v3.3 external approval system</strong>: {_text(dip.get('v3_3_external_approval_system_percent', 0))}% ({_text(dip.get('v3_3_status_label', 'unknown'))})</li>
          <li><strong>v3.3 external approval live ready</strong>: {_text(dip.get('v3_3_external_approval_system_live_ready', False))}</li>
          <li><strong>v3.4 production case-store boundary</strong>: {_text(dip.get('v3_4_production_case_store_boundary_percent', 0))}% ({_text(dip.get('v3_4_status_label', 'unknown'))})</li>
          <li><strong>v3.4 production case store live ready</strong>: {_text(dip.get('v3_4_production_case_store_live_ready', False))}</li>
          <li><strong>v3.5 runtime control plane</strong>: {_text(dip.get('v3_5_runtime_control_plane_design_percent', 0))}% ({_text(dip.get('v3_5_status_label', 'unknown'))})</li>
          <li><strong>v3.6 advisory runtime pilot</strong>: {_text(dip.get('v3_6_advisory_runtime_pilot_percent', 0))}% ({_text(dip.get('v3_6_status_label', 'unknown'))})</li>
          <li><strong>v4.0 limited runtime authority gate</strong>: {_text(dip.get('v4_0_limited_runtime_authority_gate_percent', 0))}% ({_text(dip.get('v4_0_status_label', 'unknown'))})</li>
          <li><strong>v4.0 limited runtime authority granted</strong>: {_text(dip.get('v4_0_limited_runtime_authority_granted', False))}</li>
          <li><strong>v4.1 live identity evidence gate</strong>: {_text(dip.get('v4_1_live_identity_evidence_gate_percent', 0))}% ({_text(dip.get('v4_1_status_label', 'unknown'))})</li>
          <li><strong>v4.1 live identity authority ready</strong>: {_text(dip.get('v4_1_live_identity_authority_ready', False))}</li>
          <li><strong>v4.2 live approval provider gate</strong>: {_text(dip.get('v4_2_live_approval_provider_gate_percent', 0))}% ({_text(dip.get('v4_2_status_label', 'unknown'))})</li>
          <li><strong>v4.2 live approval provider ready</strong>: {_text(dip.get('v4_2_live_approval_provider_ready', False))}</li>
          <li><strong>v4.3 production case-store gate</strong>: {_text(dip.get('v4_3_production_case_store_gate_percent', 0))}% ({_text(dip.get('v4_3_status_label', 'unknown'))})</li>
          <li><strong>v4.3 production case store live ready</strong>: {_text(dip.get('v4_3_production_case_store_live_ready', False))}</li>
          <li><strong>v4.4 release promotion execution gate</strong>: {_text(dip.get('v4_4_release_promotion_execution_gate_percent', 0))}% ({_text(dip.get('v4_4_status_label', 'unknown'))})</li>
          <li><strong>v4.4 production deployment executed</strong>: {_text(dip.get('v4_4_prod_deployment_executed', False))}</li>
          <li><strong>v5.0 governed advisory runtime</strong>: {_text(dip.get('v5_0_governed_advisory_runtime_percent', 0))}% ({_text(dip.get('v5_0_status_label', 'unknown'))})</li>
          <li><strong>v5.0 side effects executed</strong>: {_text(dip.get('v5_0_side_effects_executed', False))}</li>
          <li><strong>v5.5 controlled runtime gate</strong>: {_text(dip.get('v5_5_controlled_runtime_execution_gate_percent', 0))}% ({_text(dip.get('v5_5_status_label', 'unknown'))})</li>
          <li><strong>v5.5 controlled runtime authorized</strong>: {_text(dip.get('v5_5_controlled_runtime_execution_authorized', False))}</li>
          <li><strong>v6.0 platform hardening assessment</strong>: {_text(dip.get('v6_0_platform_hardening_assessment_percent', 0))}% ({_text(dip.get('v6_0_status_label', 'unknown'))})</li>
          <li><strong>v6.0 platform production ready</strong>: {_text(dip.get('v6_0_platform_production_ready', False))}</li>
          <li><strong>v6.1 live identity authority</strong>: {_text(dip.get('v6_1_live_identity_authority_percent', 0))}% ({_text(dip.get('v6_1_status_label', 'unknown'))})</li>
          <li><strong>v6.1 live identity authority ready</strong>: {_text(dip.get('v6_1_live_identity_authority_ready', False))}</li>
          <li><strong>v6.1 MFA claim observed</strong>: {_text(dip.get('v6_1_mfa_claim_observed', False))}</li>
          <li><strong>v6.2 live decision approval provider</strong>: {_text(dip.get('v6_2_live_decision_approval_provider_percent', 0))}% ({_text(dip.get('v6_2_status_label', 'unknown'))})</li>
          <li><strong>v6.2 live decision approval provider ready</strong>: {_text(dip.get('v6_2_live_decision_approval_provider_ready', False))}</li>
          <li><strong>v6.2 AI approval allowed</strong>: {_text(dip.get('v6_2_ai_approval_allowed', False))}</li>
          <li><strong>v6.3 production durable case store</strong>: {_text(dip.get('v6_3_production_durable_case_store_percent', 0))}% ({_text(dip.get('v6_3_status_label', 'unknown'))})</li>
          <li><strong>v6.3 production durable case store ready</strong>: {_text(dip.get('v6_3_production_durable_case_store_ready', False))}</li>
          <li><strong>v6.4 production promotion chain</strong>: {_text(dip.get('v6_4_production_promotion_chain_percent', 0))}% ({_text(dip.get('v6_4_status_label', 'unknown'))})</li>
          <li><strong>v6.4 production promotion ready</strong>: {_text(dip.get('v6_4_production_promotion_ready', False))}</li>
          <li><strong>v7.0 controlled runtime pilot</strong>: {_text(dip.get('v7_0_controlled_runtime_pilot_percent', 0))}% ({_text(dip.get('v7_0_status_label', 'unknown'))})</li>
          <li><strong>v7.0 controlled runtime pilot authorized</strong>: {_text(dip.get('v7_0_controlled_runtime_pilot_authorized', False))}</li>
          <li><strong>v7.5 marketplace runtime governance</strong>: {_text(dip.get('v7_5_marketplace_runtime_governance_percent', 0))}% ({_text(dip.get('v7_5_status_label', 'unknown'))})</li>
          <li><strong>v7.5 marketplace runtime invocation authorized</strong>: {_text(dip.get('v7_5_marketplace_runtime_invocation_authorized', False))}</li>
          <li><strong>v7.5 unrestricted marketplace execution allowed</strong>: {_text(dip.get('v7_5_unrestricted_marketplace_execution_allowed', False))}</li>
          <li><strong>v8.0 shared context runtime governance</strong>: {_text(dip.get('v8_0_shared_context_runtime_governance_percent', 0))}% ({_text(dip.get('v8_0_status_label', 'unknown'))})</li>
          <li><strong>v8.0 runtime context exchange authorized</strong>: {_text(dip.get('v8_0_runtime_context_exchange_authorized', False))}</li>
          <li><strong>v8.0 direct database access allowed</strong>: {_text(dip.get('v8_0_direct_database_access_allowed', False))}</li>
          <li><strong>v9.0 production authority readiness review</strong>: {_text(dip.get('v9_0_production_authority_readiness_review_percent', 0))}% ({_text(dip.get('v9_0_status_label', 'unknown'))})</li>
          <li><strong>v9.0 production decision authority granted</strong>: {_text(dip.get('v9_0_production_decision_authority_granted', False))}</li>
          <li><strong>v10.0 completion plan execution</strong>: {_text(dip.get('v10_0_completion_plan_execution_percent', 0))}% ({_text(dip.get('v10_0_status_label', 'unknown'))})</li>
          <li><strong>v10.0 reviewed steps</strong>: {_text(dip.get('v10_0_reviewed_step_count', 0))}</li>
          <li><strong>v10.0 evidence gates complete</strong>: {_text(dip.get('v10_0_evidence_gate_complete_count', 0))}</li>
          <li><strong>v10.0 live completions achieved</strong>: {_text(dip.get('v10_0_live_completion_achieved_count', 0))}</li>
          <li><strong>v10.0 blocked live completions</strong>: {_text(dip.get('v10_0_blocked_live_completion_count', 0))}</li>
          <li><strong>v10.0 product vision alignment valid</strong>: {_text(dip.get('v10_0_product_vision_alignment_valid', False))}</li>
          <li><strong>v10.0 AI policy boundary preserved</strong>: {_text(dip.get('v10_0_ai_policy_boundary_preserved', False))}</li>
          <li><strong>v10.0 runtime authority blocked</strong>: {_text(dip.get('v10_0_runtime_authority_grant_blocked', False))}</li>
          <li><strong>v10.0 production authority blocked</strong>: {_text(dip.get('v10_0_production_decision_authority_blocked', False))}</li>
          <li><strong>v11.0 API-first platform foundation</strong>: {_text(dip.get('v11_0_api_first_platform_foundation_percent', 0))}% ({_text(dip.get('v11_0_status_label', 'unknown'))})</li>
          <li><strong>v11.0 REST authoritative</strong>: {_text(dip.get('v11_0_rest_authoritative', False))}</li>
          <li><strong>v11.0 WebSocket notification only</strong>: {_text(dip.get('v11_0_websocket_notification_only', False))}</li>
          <li><strong>v11.0 forced microservice topology</strong>: {_text(dip.get('v11_0_forced_microservice_topology', False))}</li>
          <li><strong>v11.0 runtime authority blocked</strong>: {_text(dip.get('v11_0_runtime_authority_blocked', False))}</li>
          <li><strong>v15.0 API foundation</strong>: {_text(dip.get('v15_0_api_foundation_percent', 0))}% ({_text(dip.get('v15_0_status_label', 'unknown'))})</li>
          <li><strong>v15.0 certified capabilities</strong>: {_text(dip.get('v12_0_certified_capability_count', 0))}</li>
          <li><strong>v15.0 cross-product database access</strong>: {_text(dip.get('v13_0_cross_product_database_access_allowed', False))}</li>
          <li><strong>v15.0 WebSocket authoritative</strong>: {_text(dip.get('v15_0_websocket_authoritative', False))}</li>
          <li><strong>v15.0 events mutate state</strong>: {_text(dip.get('v15_0_events_mutate_business_state', False))}</li>
          <li><strong>v20.0 architecture closure</strong>: {_text(dip.get('v20_0_architecture_closure_percent', 0))}% ({_text(dip.get('v20_0_status_label', 'unknown'))})</li>
          <li><strong>v20.0 certified services</strong>: {_text(dip.get('v16_0_certified_service_count', 0))}</li>
          <li><strong>v20.0 runtime invocations allowed</strong>: {_text(dip.get('v16_0_runtime_invocation_allowed_count', 0))}</li>
          <li><strong>v20.0 product direct database access</strong>: {_text(dip.get('v17_0_direct_database_access_allowed', False))}</li>
          <li><strong>v20.0 WebSocket authoritative</strong>: {_text(dip.get('v19_0_websocket_authoritative', False))}</li>
          <li><strong>v20.0 governance store backend selected</strong>: {_text(dip.get('v20_0_storage_backend_selected', False))}</li>
          <li><strong>v25.0 contract closure</strong>: {_text(dip.get('v25_0_contract_closure_percent', 0))}% ({_text(dip.get('v25_0_status_label', 'unknown'))})</li>
          <li><strong>v25.0 canonical OpenAPI</strong>: {_text(dip.get('v21_0_canonical_openapi_contract_valid', False))}</li>
          <li><strong>v25.0 adapter live invocations</strong>: {_text(dip.get('v23_0_live_invocation_allowed_count', 0))}</li>
          <li><strong>v25.0 governance-store backend selected</strong>: {_text(dip.get('v24_0_storage_backend_selected', False))}</li>
          <li><strong>v25.0 WebSocket authoritative</strong>: {_text(dip.get('v25_0_websocket_authoritative', False))}</li>
          <li><strong>Pre-runtime scope</strong>: {_text(dip.get('pre_runtime_completion_scope_percent', 0))}% ({_text(dip.get('pre_runtime_completion_scope_label', 'unknown'))})</li>
          <li><strong>Policy engine readiness</strong>: {_text(dip.get('deterministic_policy_engine_readiness_percent', 0))}%</li>
          <li><strong>Release readiness</strong>: {_text(dip.get('release_management_readiness_percent', 0))}%</li>
          <li><strong>Target repo state</strong>: {_text(dip.get('target_repo_state', 'unknown'))}</li>
          <li><strong>Blocked DIP claims</strong>: {_text(len(dip.get('blocked_claims', [])))}</li>
        </ul>
      </section>
    </div>
  </main>
</body>
</html>
"""


def write_operator_view(root: Path, out: Path, generated_at: str | None = None) -> dict[str, Any]:
    snapshot = build_snapshot(root, generated_at)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_operator_view(snapshot), encoding="utf-8")
    return snapshot
