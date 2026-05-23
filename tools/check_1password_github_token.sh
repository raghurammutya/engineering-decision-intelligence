#!/usr/bin/env bash
set -euo pipefail

vault="${EDI_OP_VAULT:-EDI-V5}"
item="${EDI_OP_GITHUB_ITEM:-EDI GitHub}"
field="${EDI_OP_GITHUB_FIELD:-token}"

tmp_env="$(mktemp)"
tmp_response="$(mktemp)"
cleanup() {
  rm -f "$tmp_env" "$tmp_response"
}
trap cleanup EXIT

cat >"$tmp_env" <<EOF
EDI_GITHUB_TOKEN="op://${vault}/${item}/${field}"
EOF
chmod 600 "$tmp_env"

echo "onepassword_reference=op://${vault}/${item}/${field}"

op run --env-file="$tmp_env" -- bash -s -- "$tmp_response" <<'EOF'
set -euo pipefail

response_file="$1"
: "${EDI_GITHUB_TOKEN:?missing EDI_GITHUB_TOKEN}"

code="$(
  curl -sS -o "$response_file" -w "%{http_code}" \
    -H "Authorization: Bearer ${EDI_GITHUB_TOKEN}" \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    https://api.github.com/rate_limit
)"

echo "github_http_status=${code}"
test "$code" = "200"
EOF

echo "github_token_check=ok"
