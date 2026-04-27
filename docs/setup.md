# Setup

Complete these steps **before the labcamp starts**. If you run into issues, check [Troubleshooting](#troubleshooting).

You will use a **terminal** (macOS **Terminal** or **iTerm**, Windows **PowerShell** or **Git Bash**, Linux your distro's terminal) and a **code editor** is optional for reading files.

---

## 1. Install uv

[uv](https://docs.astral.sh/uv/) is a fast Python package manager. It also installs Python for you — no separate Python install required.

=== "macOS / Linux"

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    Restart your terminal, then verify:

    ```bash
    uv --version
    ```

=== "Windows"

    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

    Restart your terminal, then verify:

    ```powershell
    uv --version
    ```

!!! tip "uv handles Python too"
    `uv sync` will automatically download and use Python 3.11+ if it is not already installed on your system.

---

## 2. Git

You need **Git** to **clone** this repository and to **reset** a lab with `git checkout`.

```bash
git --version
```

If that prints a version, skip to [Claude Code](#3-install-claude-code).

=== "macOS"

    Run **Command Line Tools** (includes Git):

    ```bash
    xcode-select --install
    ```

    Or install Git via [Homebrew](https://brew.sh/): `brew install git`.

=== "Windows"

    Install **[Git for Windows](https://git-scm.com/download/win)**. Use **PowerShell** or **Git Bash** for the shell commands in this guide.

=== "Linux"

    ```bash
    # Debian / Ubuntu
    sudo apt update && sudo apt install git

    # Fedora
    sudo dnf install git

    # Arch
    sudo pacman -S git
    ```

---

## 3. Install Claude Code

=== "macOS / Linux"

    ```bash
    curl -fsSL https://claude.ai/install.sh | bash
    claude --version
    ```

=== "Windows"

    ```powershell
    irm https://claude.ai/install.ps1 | iex
    claude --version
    ```

!!! warning "Do not run `claude` yet"
    The labcamp uses **Amazon Bedrock**, not an Anthropic account login. You will configure it in [section 5](#5-configure-claude-code-for-amazon-bedrock).

---

## 4. Clone and install dependencies

The commands below are **identical on all operating systems**:

```bash
git clone https://github.com/Storm-AI-Reply/ClaudeCode-Labcamp.git
cd ClaudeCode-Labcamp
uv sync
```

`uv sync` reads `pyproject.toml`, creates a virtual environment, and installs all dependencies in one step — no manual venv creation or activation needed.

---

## 5. Configure Claude Code for Amazon Bedrock

Reference: [Claude Code on Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock).

The organizers will hand you:

- `AWS_BEARER_TOKEN_BEDROCK`
- `AWS_REGION`

In the terminal where you will launch `claude`, use the same simple Bedrock API key flow described in the official docs: export the bearer token and start Claude Code.

### Bedrock API key (bearer token)

Official reference (Option E): [Claude Code on Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock#2-configure-aws-credentials).

=== "macOS / Linux"

    ```bash
    # Required for Claude Code + Bedrock
    export CLAUDE_CODE_USE_BEDROCK=1
    export AWS_REGION=eu-west-1
    export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
    ```

=== "Windows (PowerShell)"

    ```powershell
    # Required for Claude Code + Bedrock
    $env:CLAUDE_CODE_USE_BEDROCK = "1"
    $env:AWS_REGION = "eu-west-1"
    $env:AWS_BEARER_TOKEN_BEDROCK = "your-bedrock-api-key"
    ```

!!! warning "No spaces around `=`"
    Use `export FOO=bar`, not `export FOO = bar`. On PowerShell the syntax differs (`$env:VAR = "value"`) but the same rule applies: no extra spaces inside the assignment.

!!! note "New terminal tab or window?"
    Environment variables do not persist across sessions. If you open a new terminal, re-export the entire block above and relaunch `claude` before continuing.

If your shell is already configured for Bedrock and region, the essential key step is:

```bash
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

Then launch Claude Code:

```bash
claude
```

You should land directly at the prompt with no Anthropic login step.

!!! note "Your credentials are temporary and personal"
    They are issued just for you. Do not share them. If they stop working (expired or revoked), ask an organizer for a fresh set.

!!! tip "Split terminal"
    Keep two panes open side by side: one for Claude Code, one for shell work (starting the server, running `curl`, checking logs). This avoids spending tokens asking Claude to run commands you can run directly. In VS Code or any IDE, right-click the terminal tab → **Split Terminal**.

---

## 6. Confirm the app runs

From the **repository root**:

```bash
cd labs/01-execution-model/starter
uv run uvicorn main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs). You should see the quiz-night API documentation page. Stop the server with **Ctrl+C** (same on all platforms).

!!! warning "Do not run pytest during setup"
    The Lab 01 starter has intentional bugs; fixing them is the exercise.

---

## Hooks and MCP (all operating systems)

Lab hooks and MCP servers in `.claude/settings.json` use `uv run python`. Since `uv run` resolves the virtual environment automatically, no manual activation is ever required.

Example hook command:
```json
{ "type": "command", "command": "uv run python .claude/hooks/guard_live.py" }
```

Example MCP server:
```json
{ "command": "uv", "args": ["run", "python", "mcp_server/trivia_content_server.py"] }
```

---

## Moving between labs

Before switching labs: run `/exit` inside Claude Code, then run the `cd` command in your shell, and relaunch `claude` in the new directory.

These paths assume you are at the `starter/` root. If you are deeper in the directory tree, navigate back to `starter/` first.

```bash
cd ../../../labs/02-project-configuration/starter    # from Lab 01 starter
cd ../../../labs/03-control-connect/starter          # from Lab 02 starter
cd ../../../labs/04-scale-reuse/starter              # from Lab 03 starter
cd ../../../labs/final-project/starter               # from Lab 04 starter
```

---

## Resetting a lab

From inside a lab's `starter/` folder:

```bash
git checkout -- .
```

That restores tracked files to the last commit. Requires Git ([section 2](#2-git)).

---

## Troubleshooting

??? question "`uv: command not found`"
    Restart your terminal after installation. If still missing, re-run the installer from [astral.sh/uv](https://astral.sh/uv).

??? question "`uv run` fails with `No such file or directory`"
    Run `uv sync` from the repo root first to create the virtual environment and install dependencies.

??? question "`git: command not found`"
    Install Git ([section 2](#2-git)) and open a **new** terminal window.

??? question "`uv run pytest` or `uv run uvicorn` shows `ModuleNotFoundError`"
    Run `uv sync` from the repo root. Make sure you are running from within the cloned repo.

??? question "Port 8000 already in use"
    Use a different port: `uv run uvicorn main:app --reload --port 8001`

??? question "Quiz data disappeared"
    The app uses **in-memory storage**. Restarting `uvicorn` wipes all data; keep the server running throughout each lab.

??? question "`claude` starts but asks for an Anthropic login"
    Your `CLAUDE_CODE_USE_BEDROCK=1` env var is missing in this terminal. Re-export the block from [section 5](#5-configure-claude-code-for-amazon-bedrock) and start `claude` again.

??? question "Bedrock error: `ExpiredTokenException` or `AccessDenied`"
    Your Bedrock API key expired or was revoked. Ask an organizer for a fresh key and re-export it.

??? question "Bedrock error mentions bearer token / `CallWithBearerToken` denied"
    Your Bedrock API key path was blocked by an organizer kill switch. Ask for a new token or for the group revoke policy to be disabled.

??? question "Bedrock error: model not available in region"
    You are using a region that doesn't match the one the organizers assigned. Re-export `AWS_REGION` with the value on your sheet.

??? question "Phones cannot connect (Final Project)"
    Start the server with `--host 0.0.0.0` and use your laptop's local IP (not `localhost`). Phones must be on the same Wi‑Fi.

??? question "MCP server not connecting"
    Check that `"command"` is `"uv"` and `"args"` starts with `["run", "python", ...]`, the configured path matches your MCP server file, you restarted Claude after editing settings, and `/mcp` lists the tools.
