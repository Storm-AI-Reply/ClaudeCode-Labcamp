#!/usr/bin/env bash
# Remove the labcamp role, its attached managed policy, and the kill-switch
# inline policy. Run AFTER the event.
#
# Uses the AWS_PROFILE + AWS_REGION defined in aws/.env.
#
# Usage:
#   ./teardown.sh
#
# Optional flags:
#   --role-name        (default: LabcampBedrockRole)
#   --bedrock-policy   (default: LabcampBedrockPolicy)
#   --kill-switch-name (default: LabcampKillSwitch)
#   --keep-csv         (skip deleting aws/out/ credentials)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_common.sh
source "${SCRIPT_DIR}/_common.sh"

ROLE_NAME="LabcampBedrockRole"
POLICY_NAME="LabcampBedrockPolicy"
KILL_SWITCH_NAME="LabcampKillSwitch"
KEEP_CSV=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --role-name)        ROLE_NAME="$2"; shift 2 ;;
    --bedrock-policy)   POLICY_NAME="$2"; shift 2 ;;
    --kill-switch-name) KILL_SWITCH_NAME="$2"; shift 2 ;;
    --keep-csv)         KEEP_CSV=1; shift ;;
    -h|--help)
      grep -E "^# " "$0" | sed 's/^# //'
      exit 0 ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1 ;;
  esac
done

ACCOUNT_ID="$(aws_cli sts get-caller-identity --query Account --output text)"
POLICY_ARN="arn:aws:iam::${ACCOUNT_ID}:policy/${POLICY_NAME}"

echo "==> Using profile ${AWS_PROFILE} in account ${ACCOUNT_ID}"

echo "==> Detaching managed policy ${POLICY_ARN} (if attached)"
aws_cli iam detach-role-policy \
  --role-name "${ROLE_NAME}" \
  --policy-arn "${POLICY_ARN}" 2>/dev/null || true

echo "==> Removing inline kill-switch (if present)"
aws_cli iam delete-role-policy \
  --role-name "${ROLE_NAME}" \
  --policy-name "${KILL_SWITCH_NAME}" 2>/dev/null || true

echo "==> Deleting managed policy ${POLICY_ARN} (if exists)"
aws_cli iam delete-policy --policy-arn "${POLICY_ARN}" 2>/dev/null || true

echo "==> Deleting role ${ROLE_NAME} (if exists)"
aws_cli iam delete-role --role-name "${ROLE_NAME}" 2>/dev/null || true

if [[ "$KEEP_CSV" -eq 0 ]]; then
  if [[ -d "${SCRIPT_DIR}/out" ]]; then
    echo "==> Removing aws/out/ (credentials CSV)"
    rm -rf "${SCRIPT_DIR}/out"
  fi
else
  echo "==> Keeping aws/out/ as requested"
fi

echo "Teardown done."
