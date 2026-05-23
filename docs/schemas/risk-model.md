# Risk Model Draft

## Risk Dimensions

| Dimension | Meaning |
| --- | --- |
| mutation_risk | ability to change operational state |
| environment_risk | dev, test, staging, prod exposure |
| secret_risk | reads or writes sensitive values |
| ownership_risk | missing, stale, or ambiguous owner |
| evidence_risk | missing or stale proof |
| rollback_risk | missing rollback path or evidence |
| policy_drift_risk | observed behavior diverges from intended policy |
| ai_autonomy_risk | agentic capability, tool access, or autonomous execution |

## Risk Levels

| Level | Meaning |
| --- | --- |
| Low | informational or low operational consequence |
| Medium | owner review required |
| High | evidence required before promotion or expansion |
| Critical | controlled admission or block required |

## First MVP High-Risk Signals

- direct production mutation path,
- secret-sensitive automation,
- deployment path outside canonical promotion,
- database migration or destructive operation,
- broker/order write capability,
- runtime shell execution,
- missing owner on mutation-capable automation,
- missing rollback or promotion evidence.
