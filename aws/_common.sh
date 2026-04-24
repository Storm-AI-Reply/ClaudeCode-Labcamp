#!/usr/bin/env bash
# Shared helpers for the labcamp AWS scripts.
# Sourced by setup-role.sh, generate-sessions.sh, kill-switch.sh, teardown.sh.
#
# Responsibilities:
#   - Load aws/.env (AWS_PROFILE, AWS_REGION, optional LABCAMP_ROLE_ARN).
#   - Validate that AWS_PROFILE is set and that the CLI can reach AWS.
#   - Expose a single `aws_cli` wrapper that every script uses instead of `aws`.

set -euo pipefail

_COMMON_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_ENV_FILE="${_COMMON_DIR}/.env"

if [[ -f "$_ENV_FILE" ]]; then
  set -o allexport
  # shellcheck disable=SC1090
  source "$_ENV_FILE"
  set +o allexport
else
  echo "Error: ${_ENV_FILE} not found." >&2
  echo "Copy aws/.env.example to aws/.env and fill in AWS_PROFILE + AWS_REGION." >&2
  exit 1
fi

if [[ -z "${AWS_PROFILE:-}" ]]; then
  echo "Error: AWS_PROFILE is empty. Set it in aws/.env." >&2
  exit 1
fi

if [[ -z "${AWS_REGION:-}" ]]; then
  echo "Error: AWS_REGION is empty. Set it in aws/.env." >&2
  exit 1
fi

export AWS_PROFILE
export AWS_REGION
export AWS_DEFAULT_REGION="$AWS_REGION"

# Thin wrapper: every `aws_cli ...` call carries --profile and --region so the
# scripts never depend on the caller's ambient environment.
aws_cli() {
  aws --profile "$AWS_PROFILE" --region "$AWS_REGION" "$@"
}

# Best-effort preflight. If this fails, the user is not logged in via SSO.
if ! aws_cli sts get-caller-identity >/dev/null 2>&1; then
  cat >&2 <<EOF
Error: cannot call AWS with profile "${AWS_PROFILE}" in region "${AWS_REGION}".

If you use AWS SSO, run:
  aws sso login --profile ${AWS_PROFILE}

Then re-run this script.
EOF
  exit 1
fi
