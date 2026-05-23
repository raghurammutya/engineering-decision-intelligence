# Reusable Packaging Summary

Generated: `2026-05-23T05:32:41+00:00`

Records: `6`

| item | path | command |
| --- | --- | --- |
| cli | edi/__main__.py | python3 -m edi validate |
| scanner | tools/operational_state_scan.py | python3 -m edi scan --repo <repo> --out <out> |
| v2 | edi/v2.py | python3 -m edi v2 build |
| v3 | edi/v3.py | python3 -m edi v3 build |
| policy_pack | policies/ | python3 -m edi validate |
| connector_inputs | connector-inputs/ | python3 -m edi v3 build --check |
