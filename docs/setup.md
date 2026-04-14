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
    claude   # authenticate when prompted, then exit with /exit
    ```

=== "Windows"

    ```powershell
    irm https://claude.ai/install.ps1 | iex
    claude --version
    claude   # authenticate when prompted, then exit with /exit
    ```

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

## 5. Confirm the app runs

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

`cd` into the next lab's starter. No activation needed — `uv run` finds the environment automatically.

```bash
cd ../../../labs/02-project-configuration/starter    # from Lab 01
cd ../../../labs/03-control-connect/starter          # from Lab 02
cd ../../../labs/04-scale-reuse/starter              # from Lab 03
cd ../../../labs/final-project/starter               # from Lab 04
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

??? question "Claude Code rate limited"
    Each group shares one account. Wait 30 seconds and try again. Keep prompts focused.

??? question "Phones cannot connect (Final Project)"
    Start the server with `--host 0.0.0.0` and use your laptop's local IP (not `localhost`). Phones must be on the same Wi‑Fi.

??? question "MCP server not connecting"
    Check that `"command"` is `"uv"` and `"args"` starts with `["run", "python", ...]`, the configured path matches your MCP server file, you restarted Claude after editing settings, and `/mcp` lists the tools.
