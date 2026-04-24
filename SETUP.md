# Setup

Complete these steps **before the labcamp starts**. For the full formatted guide, use the **[labcamp documentation site](https://storm-ai-reply.github.io/ClaudeCode-Labcamp/setup/)** ([repository](https://github.com/Storm-AI-Reply/ClaudeCode-Labcamp)).

## 1. Install uv

**macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart your terminal, then verify: `uv --version`

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart your terminal, then verify: `uv --version`

> uv will also install Python 3.11+ automatically when needed — no separate Python install required.

## 2. Install Git

```bash
git --version
```

If missing: [git-scm.com/downloads](https://git-scm.com/downloads). On macOS: `xcode-select --install`.

## 3. Install Claude Code

**macOS / Linux:**

```bash
curl -fsSL https://claude.ai/install.sh | bash
claude --version
```

**Windows (PowerShell):**

```powershell
irm https://claude.ai/install.ps1 | iex
claude --version
```

> Do **not** run `claude` yet. The labcamp uses Amazon Bedrock, not an Anthropic login. You'll configure it in step 5.

## 4. Clone and set up

```bash
git clone https://github.com/Storm-AI-Reply/ClaudeCode-Labcamp.git
cd ClaudeCode-Labcamp
uv sync
```

`uv sync` creates the virtual environment and installs all dependencies in one step.

## 5. Configure Claude Code for Amazon Bedrock

Reference: [Claude Code on Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md).

The organizers will hand you:

- `AWS_BEARER_TOKEN_BEDROCK`
- `AWS_REGION`

Export them in the terminal where you will launch `claude`:

```bash
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1
export AWS_BEARER_TOKEN_BEDROCK=...
```

Then start Claude Code:

```bash
claude
```

You should land directly at the prompt with no Anthropic login step.

> **Your API key is personal**. Do not share it. If it expires or is revoked, ask an organizer for a fresh key.

## 6. Verify the app runs

```bash
cd labs/01-execution-model/starter
uv run uvicorn main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs), you should see the quiz-night API docs. Press `Ctrl+C` to stop.

> **Do not run `uv run pytest` during setup.** The Lab 01 starter has intentional bugs, fixing them is the exercise.

## Moving between labs

`cd` into the next lab's starter. No activation needed — just use `uv run`:

```bash
cd ../../../labs/02-project-configuration/starter    # from Lab 01
cd ../../../labs/03-control-connect/starter           # from Lab 02
cd ../../../labs/04-scale-reuse/starter               # from Lab 03
cd ../../../labs/final-project/starter                # from Lab 04
```

## Resetting a lab

```bash
git checkout -- .
```

Resets all files in the current directory to their original state.

---

## Troubleshooting

**`uv: command not found`**
Restart your terminal after installation. If still missing, re-run the installer.

**`uv run pytest` or `uv run uvicorn` fails with `No such file or directory`**
Run `uv sync` from the repo root first to install dependencies.

**Port 8000 already in use**
Use a different port: `uv run uvicorn main:app --reload --port 8001`

**`ModuleNotFoundError: No module named 'fastapi'`**
Run `uv sync` from the repo root.

**Quiz data disappeared**
The app uses in-memory storage. Restarting `uvicorn` wipes all data, keep the server running throughout each lab.

**`claude` starts but asks for an Anthropic login**
Your `CLAUDE_CODE_USE_BEDROCK=1` env var is missing in this terminal. Re-export the block from step 5 and start `claude` again.

**Bedrock error: `ExpiredTokenException` or `AccessDenied`**
Your Bedrock API key expired or was revoked. Ask an organizer for a fresh key and re-export it.

**Bedrock error mentions `CallWithBearerToken` denied**
The organizer emergency revoke is active. Ask for a new key or for the revoke policy to be disabled.

**Bedrock error: model not available in region**
You are using a region that doesn't match the one the organizers assigned. Re-export `AWS_REGION` with the value on your sheet.

**Phones cannot connect (Final Project)**
Start the server with `--host 0.0.0.0` and use your laptop's local IP address (not `localhost`). Phones must be on the same Wi-Fi.

**MCP server not connecting**
Check that `"command"` is `"uv"` and `"args"` starts with `["run", "python", ...]`, you restarted Claude after editing settings, and `/mcp` lists the tools.
