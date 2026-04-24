#!/usr/bin/env bash
# Generate N temporary AWS STS sessions (one per participant) by assuming
# the labcamp Bedrock role. Output is written to aws/out/participants.csv.
#
# Uses the AWS_PROFILE + AWS_REGION defined in aws/.env. The role ARN can
# come from aws/.env (LABCAMP_ROLE_ARN=...) or from --role-arn.
#
# Prereqs:
#   - ./setup-role.sh has been run.
#   - You are logged in via SSO (aws sso login --profile $AWS_PROFILE).
#
# Usage:
#   ./generate-sessions.sh --count 60
#
# Optional flags:
#   --role-arn    (default: $LABCAMP_ROLE_ARN from aws/.env)
#   --duration    (default: 10800 -> 3 hours; capped by role max-session-duration)
#   --prefix      (default: participant)
#   --out         (default: aws/out/participants.csv)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_common.sh
source "${SCRIPT_DIR}/_common.sh"

OUT_DEFAULT="${SCRIPT_DIR}/out/participants.csv"

COUNT=60
ROLE_ARN="${LABCAMP_ROLE_ARN:-}"
DURATION=10800
PREFIX="participant"
OUT_FILE="${OUT_DEFAULT}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --count)     COUNT="$2"; shift 2 ;;
    --role-arn)  ROLE_ARN="$2"; shift 2 ;;
    --duration)  DURATION="$2"; shift 2 ;;
    --prefix)    PREFIX="$2"; shift 2 ;;
    --out)       OUT_FILE="$2"; shift 2 ;;
    -h|--help)
      grep -E "^# " "$0" | sed 's/^# //'
      exit 0 ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1 ;;
  esac
done

if [[ -z "$ROLE_ARN" ]]; then
  echo "Error: role ARN missing." >&2
  echo "Set LABCAMP_ROLE_ARN in aws/.env or pass --role-arn <arn>." >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "Error: 'jq' is required. Install it and retry." >&2
  exit 1
fi

mkdir -p "$(dirname "$OUT_FILE")"

echo "participant_id,aws_access_key_id,aws_secret_access_key,aws_session_token,aws_region,expires_at" > "$OUT_FILE"

WIDTH=${#COUNT}
if (( WIDTH < 2 )); then WIDTH=2; fi

echo "==> Generating ${COUNT} sessions (duration ${DURATION}s, region ${AWS_REGION}, profile ${AWS_PROFILE})"
for i in $(seq -f "%0${WIDTH}g" 1 "$COUNT"); do
  SESSION_NAME="${PREFIX}-${i}"

  CREDS="$(aws_cli sts assume-role \
    --role-arn "$ROLE_ARN" \
    --role-session-name "$SESSION_NAME" \
    --duration-seconds "$DURATION" \
    --tags "Key=Labcamp,Value=true" "Key=Participant,Value=${SESSION_NAME}" \
    --output json)"

  AK="$(echo "$CREDS" | jq -r '.Credentials.AccessKeyId')"
  SK="$(echo "$CREDS" | jq -r '.Credentials.SecretAccessKey')"
  ST="$(echo "$CREDS" | jq -r '.Credentials.SessionToken')"
  EX="$(echo "$CREDS" | jq -r '.Credentials.Expiration')"

  echo "${SESSION_NAME},${AK},${SK},${ST},${AWS_REGION},${EX}" >> "$OUT_FILE"
  echo "  - ${SESSION_NAME} ok (expires ${EX})"
done

chmod 600 "$OUT_FILE"

cat <<EOF

Done. Wrote ${COUNT} sessions to:
  ${OUT_FILE}

File permissions set to 600 (owner read/write only).
Do NOT commit this file. The aws/out/ folder is gitignored.

Distribute one row per participant via a secure channel.
EOF
