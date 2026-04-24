# AWS setup for the labcamp

Scripts for **organizers** to bootstrap an AWS account so that participants can
use Claude Code on Amazon Bedrock with temporary credentials.

> Participants never use these scripts. They only receive three AWS keys and a
> region, and set them as environment variables in Claude Code's Bedrock mode.

---

## Design decisions

- **No IAM users.** The organizer logs in via **AWS SSO / IAM Identity Center**
  with an admin profile. The trust policy on `LabcampBedrockRole` authorizes
  the whole account (`arn:aws:iam::<ACCOUNT_ID>:root`), so any admin-equivalent
  principal in that account can assume the role without creating extra users.
- **All configuration lives in `aws/.env`**. Every script in this folder
  reads `AWS_PROFILE` (and `AWS_REGION`) from there and adds `--profile` +
  `--region` to every `aws` call. No ambient env vars required.
- **All operations happen in one account**, the one your SSO profile targets.

---

## What these scripts do

1. Create a dedicated IAM role (`LabcampBedrockRole`) with **minimal Bedrock
   permissions** (`InvokeModel`, `InvokeModelWithResponseStream`,
   `ListInferenceProfiles`).
2. Generate **N short-lived STS sessions** (default 3 hours, one per
   participant) by assuming that role. Distribute the three AWS credentials
   to each participant.
3. Kill-switch: attach a `Deny` policy to the role to revoke every active
   session instantly if needed.
4. Teardown: remove the role and its policies after the event.

---

## Prereqs

- AWS account with **Anthropic models enabled in Bedrock**
  (Bedrock console -> Model catalog -> pick an Anthropic model -> submit the
  one-time use-case form).
- AWS CLI v2 installed.
- An **SSO profile configured locally** (via `aws configure sso`) pointing at
  that account with admin-equivalent permissions.
- `jq` installed (used by `generate-sessions.sh`).

---

## One-time local config

```bash
cd aws
cp .env.example .env
# Edit aws/.env and set AWS_PROFILE (your SSO profile name) + AWS_REGION.

# Log in via SSO once per day (opens browser).
aws sso login --profile "$(grep ^AWS_PROFILE .env | cut -d= -f2)"
```

`aws/.env` is git-ignored. Never commit it.

---

## Quick start (organizer)

```bash
cd aws

# 1. Create role + policy (one-time, at the start of the event).
./setup-role.sh
# The script prints the role ARN. Optionally pin it in aws/.env:
#   echo 'LABCAMP_ROLE_ARN=arn:aws:iam::...:role/LabcampBedrockRole' >> .env

# 2. Generate one session per participant (default 60 sessions, 3h each).
./generate-sessions.sh --count 60
# Output: aws/out/participants.csv (mode 600, git-ignored).
# One row per participant: 3 AWS keys + region + expiration timestamp.

# 3. Distribute one row per participant via a secure channel.

# 4. Emergency stop (optional):
./kill-switch.sh
./kill-switch.sh --disable   # re-enable if it was a false alarm

# 5. After the event:
./teardown.sh
```

Each script validates `aws/.env`, confirms SSO access (`aws sts
get-caller-identity`), and aborts with a helpful message if you are not
logged in.

---

## File-by-file

| File | Purpose |
|------|---------|
| `.env.example` | Template for local config (`AWS_PROFILE`, `AWS_REGION`, optional `LABCAMP_ROLE_ARN`). |
| `_common.sh` | Sourced by every script. Loads `.env`, validates profile, exposes `aws_cli` wrapper. |
| `setup-role.sh` | Creates `LabcampBedrockRole` with `--max-session-duration 10800` and attaches `LabcampBedrockPolicy`. |
| `generate-sessions.sh` | Loops `aws sts assume-role` N times and writes `out/participants.csv`. |
| `kill-switch.sh` | Attaches / removes an inline `Deny` policy on the role. |
| `teardown.sh` | Detaches policy, deletes role and managed policy, wipes `out/`. |
| `policies/trust-policy.json` | Allows the whole account to assume the role (`ACCOUNT_ID` is substituted at runtime). |
| `policies/bedrock-policy.json` | Minimal Bedrock permissions (from Claude Code docs). |
| `policies/kill-switch-policy.json` | `Deny` on `InvokeModel*` + `CallWithBearerToken`. |

---

## Timing

| Event phase | Command |
|-------------|---------|
| Pre-event (once) | `./setup-role.sh` |
| Start of session | `./generate-sessions.sh --count 60` |
| Emergency | `./kill-switch.sh` |
| End of event | `./teardown.sh` |

Sessions expire automatically at the `Expiration` timestamp recorded in the
CSV, so the kill-switch is for immediate stop only.

---

## What participants receive

Three AWS values plus a region. They set them as environment variables and
launch Claude Code:

```bash
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...
claude
```

See [`SETUP.md`](../SETUP.md) for the participant-facing instructions.

---

## Security notes

- `aws/.env` and `aws/out/` are git-ignored. Never commit them.
- `out/participants.csv` is written with `chmod 600` (owner read/write only).
- Trust policy principal is `arn:aws:iam::<ACCOUNT_ID>:root`: this authorizes
  only principals **inside your account** that already have permission to
  call `sts:AssumeRole` on this role. In practice that's your SSO admin.
- Each session is tagged with `Labcamp=true` and `Participant=<id>` so you
  can filter them in CloudTrail if needed.
- Use a dedicated AWS account for the event when possible. This labcamp role
  is intentionally short-lived; tearing it down at the end removes all active
  credentials and avoids leaving long-lived artefacts.
