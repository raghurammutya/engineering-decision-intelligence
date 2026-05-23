# Autonomous Enforcement

Generated: `2026-05-23T08:42:30+00:00`

Target id: `edi-product`
Enforcement score: `85.7%`
Minimum required score: `100.0%`
Autonomous production enforcement active: `False`
Fail closed: `True`

| Evidence | State | Value |
| --- | --- | --- |
| Approved autonomy policy exists | present | `policies/autonomy-policy.json` |
| Target branch protection is active | present | `True` |
| Required reviews or status checks are active | present | `{'required_status_checks_observed': True, 'pull_request_reviews_observed': True}` |
| Scheduled connector guard has run | present | `True` |
| Production environment protection is configured | missing_or_not_live | `False` |
| Rollback playbook exists | present | `docs/playbooks/production-rollback.md` |
| Break-glass playbook exists | present | `docs/playbooks/production-break-glass.md` |
