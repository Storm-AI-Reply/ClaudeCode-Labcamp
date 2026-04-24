# Bedrock short-term keys (batch)

Genera token Bedrock temporanei (max 12h) in batch e salva tracciamento partecipanti in `CSV`.

## Variabili modificabili

Prima volta:

```bash
cp .env.bedrock.example .env
```

Poi modifica `.env`:

```bash
AWS_PROFILE=default
AWS_REGION=eu-west-1
KEY_COUNT=60
PARTICIPANT_PREFIX=participant
TOKEN_TTL_SECONDS=43200
OUTPUT_DIR=keys
```

Nota: nel file `.env` scrivi senza `export` (esempio `AWS_PROFILE=default`).

## Comandi pronti

Esegui con variabili ambiente:

```bash
./generate-bedrock-short-term-keys.sh
```

Oppure override al volo:

```bash
AWS_PROFILE=my-sso AWS_REGION=eu-west-1 KEY_COUNT=60 ./generate-bedrock-short-term-keys.sh
```

## Output

- `keys/bedrock-short-term-keys-<timestamp>.csv`

Colonne: `participant_id`, `aws_profile`, `region`, `bearer_token`, `created_at_utc`, `expires_at_utc`, `status`, `note`.
