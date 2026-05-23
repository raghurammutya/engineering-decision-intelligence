#!/usr/bin/env bash
set -euo pipefail

vault="${EDI_OP_VAULT:-EDI-V5}"
env_file="${EDI_OP_ENV_FILE:-secrets/edi-v5.op.env}"
target_id="${EDI_V5_TARGET_ID:-edi-product}"

if [[ ! -f "$env_file" ]]; then
  echo "missing_env_file=$env_file" >&2
  echo "Create it from secrets/edi-v5.op.env.example and keep op:// references only." >&2
  exit 1
fi

echo "v5_target_id=$target_id"
EDI_OP_VAULT="$vault" EDI_V5_TARGET_ID="$target_id" op run --env-file="$env_file" -- python3 -m edi v5 build --live-check
python3 -m edi api snapshot
python3 -m edi validate
