#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/.env"

load_env_file_defaults() {
  local file_path="$1"
  local line
  local key
  local value

  [[ -f "${file_path}" ]] || return 0

  while IFS= read -r line || [[ -n "${line}" ]]; do
    # Skip blanks and comments.
    [[ -z "${line}" || "${line}" == \#* ]] && continue
    [[ "${line}" == *=* ]] || continue

    key="${line%%=*}"
    value="${line#*=}"

    # Trim simple surrounding quotes.
    if [[ "${value}" == \"*\" && "${value}" == *\" ]]; then
      value="${value:1:-1}"
    elif [[ "${value}" == \'*\' && "${value}" == *\' ]]; then
      value="${value:1:-1}"
    fi

    # Keep already exported env vars as override.
    if [[ -z "${!key:-}" ]]; then
      export "${key}=${value}"
    fi
  done < "${file_path}"
}

load_env_file_defaults "${ENV_FILE}"

AWS_PROFILE_VALUE="${AWS_PROFILE:-default}"
AWS_REGION_VALUE="${AWS_REGION:-eu-west-1}"
KEY_COUNT_VALUE="${KEY_COUNT:-60}"
PARTICIPANT_PREFIX_VALUE="${PARTICIPANT_PREFIX:-participant}"
TOKEN_TTL_SECONDS_VALUE="${TOKEN_TTL_SECONDS:-43200}"
OUTPUT_DIR_VALUE="${OUTPUT_DIR:-keys}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile)
      AWS_PROFILE_VALUE="$2"
      shift 2
      ;;
    --region)
      AWS_REGION_VALUE="$2"
      shift 2
      ;;
    --count)
      KEY_COUNT_VALUE="$2"
      shift 2
      ;;
    --prefix)
      PARTICIPANT_PREFIX_VALUE="$2"
      shift 2
      ;;
    --expires-in-seconds)
      TOKEN_TTL_SECONDS_VALUE="$2"
      shift 2
      ;;
    --output-dir)
      OUTPUT_DIR_VALUE="$2"
      shift 2
      ;;
    --help|-h)
      cat <<'EOF'
Usage: ./generate-bedrock-short-term-keys.sh [options]

Options:
  --profile <name>             AWS profile (default from .env or "default")
  --region <region>            AWS region (default from .env or "eu-west-1")
  --count <n>                  Number of keys (default from .env or 60)
  --prefix <value>             Participant prefix (default: participant)
  --expires-in-seconds <sec>   Requested token TTL, max 43200 (12h)
  --output-dir <path>          Output folder (default: keys)
  --help                       Show this help
EOF
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Run ./generate-bedrock-short-term-keys.sh --help" >&2
      exit 2
      ;;
  esac
done

if ! command -v uv >/dev/null 2>&1; then
  echo "Error: uv is required. Install it first: https://docs.astral.sh/uv/" >&2
  exit 1
fi

if ! command -v python >/dev/null 2>&1; then
  echo "Error: python is required in PATH." >&2
  exit 1
fi

if [[ "${KEY_COUNT_VALUE}" -le 0 ]]; then
  echo "Error: KEY_COUNT/--count must be > 0." >&2
  exit 1
fi

if [[ "${TOKEN_TTL_SECONDS_VALUE}" -le 0 || "${TOKEN_TTL_SECONDS_VALUE}" -gt 43200 ]]; then
  echo "Error: TOKEN_TTL_SECONDS/--expires-in-seconds must be between 1 and 43200." >&2
  exit 1
fi

echo "Running Bedrock short-term key batch generator..."
if [[ -f "${ENV_FILE}" ]]; then
  echo "Loaded defaults from ./.env"
fi
echo "AWS_PROFILE=${AWS_PROFILE_VALUE}"
echo "AWS_REGION=${AWS_REGION_VALUE}"
echo "COUNT=${KEY_COUNT_VALUE}"
echo "PREFIX=${PARTICIPANT_PREFIX_VALUE}"
echo "TTL_SECONDS=${TOKEN_TTL_SECONDS_VALUE}"
echo "OUTPUT_DIR=${OUTPUT_DIR_VALUE}"
echo "Tip: override at runtime, for example:"
echo "  AWS_PROFILE=my-sso AWS_REGION=eu-west-1 ./generate-bedrock-short-term-keys.sh"
echo ""

csv_escape() {
  local value="${1:-}"
  value="${value//\"/\"\"}"
  printf '"%s"' "${value}"
}

now_utc() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

output_dir_path="${SCRIPT_DIR}/${OUTPUT_DIR_VALUE}"
mkdir -p "${output_dir_path}"

timestamp="$(date -u +"%Y%m%d-%H%M%S")"
output_csv="${output_dir_path}/bedrock-short-term-keys-${timestamp}.csv"

{
  printf '%s\n' '"participant_id","aws_profile","region","bearer_token","created_at_utc","expires_at_utc","status","note"'
} > "${output_csv}"

ok_count=0
error_count=0

for ((i=1; i<=KEY_COUNT_VALUE; i++)); do
  participant_id="${PARTICIPANT_PREFIX_VALUE}_${i}"
  created_at_utc="$(now_utc)"
  # Short-term key validity is capped by Bedrock at 12h and by source AWS credentials.
  expires_at_utc="~${TOKEN_TTL_SECONDS_VALUE}s from creation (max 12h, session-limited)"

  set +e
  token="$(
    AWS_PROFILE="${AWS_PROFILE_VALUE}" AWS_REGION="${AWS_REGION_VALUE}" TOKEN_TTL_SECONDS="${TOKEN_TTL_SECONDS_VALUE}" \
      uv run --with aws-bedrock-token-generator python - <<'PY'
from datetime import timedelta
import os
from aws_bedrock_token_generator import provide_token

print(
    provide_token(
        region=os.environ["AWS_REGION"],
        expiry=timedelta(seconds=int(os.environ["TOKEN_TTL_SECONDS"])),
    )
)
PY
  )"
  status_code=$?
  set -e

  if [[ ${status_code} -eq 0 ]]; then
    status="OK"
    note=""
    ((ok_count+=1))
    echo "[${i}/${KEY_COUNT_VALUE}] generated ${participant_id}"
  else
    status="ERROR"
    note="token generation failed"
    token=""
    ((error_count+=1))
    echo "[${i}/${KEY_COUNT_VALUE}] failed ${participant_id}" >&2
  fi

  {
    csv_escape "${participant_id}"; printf ','
    csv_escape "${AWS_PROFILE_VALUE}"; printf ','
    csv_escape "${AWS_REGION_VALUE}"; printf ','
    csv_escape "${token}"; printf ','
    csv_escape "${created_at_utc}"; printf ','
    csv_escape "${expires_at_utc}"; printf ','
    csv_escape "${status}"; printf ','
    csv_escape "${note}"; printf '\n'
  } >> "${output_csv}"
done

chmod 600 "${output_csv}" || true

echo ""
echo "Done."
echo "- Success: ${ok_count}"
echo "- Failed: ${error_count}"
echo "- CSV: ${output_csv}"
echo ""
echo "Important: keep file private, it contains live bearer tokens."

if [[ ${error_count} -gt 0 ]]; then
  exit 1
fi
