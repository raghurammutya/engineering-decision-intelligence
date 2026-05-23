# Remediation Operations Summary

Generated: `2026-05-23T15:53:29+00:00`

| from | to | requires |
| --- | --- | --- |
| open | owner_review_required | ['owner_assignment'] |
| owner_review_required | accepted_risk | ['owner_approval', 'expiry'] |
| owner_review_required | remediation_in_progress | ['remediation_plan'] |
| remediation_in_progress | verified | ['verification_evidence'] |
| accepted_risk | expired | ['expiry_reached'] |
