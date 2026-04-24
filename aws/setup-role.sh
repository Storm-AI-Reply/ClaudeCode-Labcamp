#!/usr/bin/env bash
# Create the Bedrock role used by labcamp participants.
# Run ONCE per event, before generating participant sessions.
#
# Uses the AWS_PROFILE + AWS_REGION defined in aws/.env.
# No IAM users are created; the trust policy authorizes the whole account
# (`arn:aws:iam::<ACCOUNT_ID>:root`) so any admin-equivalent principal logged
# in via SSO can call sts:AssumeRole against the role.
#
# Usage:
#   ./setup-role.sh
#
# Optional flags:
#   --role-name       (default: LabcampBedrockRole)
#   --bedrock-policy  (default: LabcampBedrockPolicy)
#   --max-duration    (default: 10800  -> 3 hours)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_common.sh
source "${SCRIPT_DIR}/_common.sh"

POLICIES_DIR="${SCRIPT_DIR}/policies"

ROLE_NAME="LabcampBedrockRole"
POLICY_NAME="LabcampBedrockPolicy"
MAX_DURATION=10800

while [[ $# -gt 0 ]]; do
  case "$1" in
    --role-name)       ROLE_NAME="$2"; shift 2 ;;
    --bedrock-policy)  POLICY_NAME="$2"; shift 2 ;;
    --max-duration)    MAX_DURATION="$2"; shift 2 ;;
    -h|--help)
      grep -E "^# " "$0" | sed 's/^# //'
      exit 0 ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1 ;;
  esac
done

ACCOUNT_ID="$(aws_cli sts get-caller-identity --query Account --output text)"
CALLER_ARN="$(aws_cli sts get-caller-identity --query Arn --output text)"

echo "==> Using profile ${AWS_PROFILE} in account ${ACCOUNT_ID} (${AWS_REGION})"
echo "    Caller identity: ${CALLER_ARN}"

TMP_TRUST="$(mktemp)"
trap 'rm -f "$TMP_TRUST"' EXIT

sed "s|ACCOUNT_ID|${ACCOUNT_ID}|g" \
  "${POLICIES_DIR}/trust-policy.json" > "$TMP_TRUST"

echo "==> Creating role ${ROLE_NAME} (max session ${MAX_DURATION}s)"
aws_cli iam create-role \
  --role-name "${ROLE_NAME}" \
  --assume-role-policy-document "file://${TMP_TRUST}" \
  --max-session-duration "${MAX_DURATION}" \
  --description "Temporary role used by Claude Code labcamp participants on Bedrock" \
  >/dev/null

echo "==> Creating managed policy ${POLICY_NAME}"
POLICY_ARN="$(aws_cli iam create-policy \
  --policy-name "${POLICY_NAME}" \
  --policy-document "file://${POLICIES_DIR}/bedrock-policy.json" \
  --description "Minimal Bedrock permissions for Claude Code labcamp" \
  --query 'Policy.Arn' \
  --output text)"

echo "==> Attaching ${POLICY_ARN} to ${ROLE_NAME}"
aws_cli iam attach-role-policy \
  --role-name "${ROLE_NAME}" \
  --policy-arn "${POLICY_ARN}"

ROLE_ARN="arn:aws:iam::${ACCOUNT_ID}:role/${ROLE_NAME}"

cat <<EOF

Role ready.

  Role ARN:          ${ROLE_ARN}
  Policy ARN:        ${POLICY_ARN}
  Max session:       ${MAX_DURATION}s
  Region:            ${AWS_REGION}
  Profile used:      ${AWS_PROFILE}

Next steps:
  1. (Optional) Pin the role ARN in aws/.env so you don't have to pass --role-arn:
       echo 'LABCAMP_ROLE_ARN=${ROLE_ARN}' >> aws/.env
  2. Generate N participant sessions:
       ./generate-sessions.sh --count 60
  3. Kill-switch (emergency stop):
       ./kill-switch.sh --role-name ${ROLE_NAME}
  4. Teardown after the event:
       ./teardown.sh --role-name ${ROLE_NAME} --bedrock-policy ${POLICY_NAME}

EOF
