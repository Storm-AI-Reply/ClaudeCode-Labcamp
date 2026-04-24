#!/usr/bin/env bash
# Emergency stop: attach an inline Deny policy to the labcamp role,
# blocking all Bedrock invocations for every active STS session
# generated from that role.
#
# Uses the AWS_PROFILE + AWS_REGION defined in aws/.env.
#
# Usage:
#   ./kill-switch.sh                    # enable kill-switch
#   ./kill-switch.sh --disable          # remove kill-switch
#
# Optional flags:
#   --role-name   (default: LabcampBedrockRole)
#   --policy-name (default: LabcampKillSwitch)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_common.sh
source "${SCRIPT_DIR}/_common.sh"

POLICIES_DIR="${SCRIPT_DIR}/policies"

ROLE_NAME="LabcampBedrockRole"
POLICY_NAME="LabcampKillSwitch"
ACTION="enable"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --role-name)   ROLE_NAME="$2"; shift 2 ;;
    --policy-name) POLICY_NAME="$2"; shift 2 ;;
    --disable)     ACTION="disable"; shift ;;
    -h|--help)
      grep -E "^# " "$0" | sed 's/^# //'
      exit 0 ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1 ;;
  esac
done

if [[ "$ACTION" == "enable" ]]; then
  echo "==> Attaching inline Deny policy ${POLICY_NAME} to role ${ROLE_NAME} (profile ${AWS_PROFILE})"
  aws_cli iam put-role-policy \
    --role-name "${ROLE_NAME}" \
    --policy-name "${POLICY_NAME}" \
    --policy-document "file://${POLICIES_DIR}/kill-switch-policy.json"
  echo "Kill-switch ACTIVE. All existing sessions for ${ROLE_NAME} can no longer invoke Bedrock."
else
  echo "==> Removing inline Deny policy ${POLICY_NAME} from role ${ROLE_NAME} (profile ${AWS_PROFILE})"
  aws_cli iam delete-role-policy \
    --role-name "${ROLE_NAME}" \
    --policy-name "${POLICY_NAME}"
  echo "Kill-switch REMOVED. Existing sessions can invoke Bedrock again."
fi
