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


def render_operator_view(snapshot: dict[str, Any]) -> str:
    product = snapshot["product"]
    executive = snapshot["executive"]
    risk = snapshot["risk"]
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

    lane_items = "\n".join(f"<li>{_text(lane)}</li>" for lane in action_lanes) or "<li>No action lanes available.</li>"
    owner_items = "\n".join(
        f"<li><strong>{_text(key)}</strong>: {_text(value)}</li>"
        for key, value in sorted(owner_counts.items())
    ) or "<li>No owner review counts available.</li>"
    telemetry_items = "\n".join(
        f"<li><strong>{_text(key)}</strong>: {_text(value)}</li>"
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
