# V5 Target Installation And Live Evidence Roadmap

Status as of 2026-05-23: secure tooling implemented; live target evidence is
blocked pending user-owned 1Password sign-in, target secret references, and
target-system installation.

## Boundary

The 1Password CLI is installed locally. This repository does not contain
plaintext secrets and this implementation does not inspect existing 1Password
vault items.

v5 separates:

- secure tooling completion,
- live claim completion.

## Safe Command Pattern

```bash
cp secrets/edi-v5.op.env.example secrets/edi-v5.op.env
EDI_OP_VAULT=<dedicated-vault> op run --env-file=secrets/edi-v5.op.env -- python3 -m edi v5 build --live-check
```

## Live Evidence Still Required

- target credentials installed,
- scheduled connectors observed running,
- target repositories enforcing PR checks,
- autonomous production enforcement active,
- complete live runtime truth with coverage and blind spots.
