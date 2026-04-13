# Setup

Complete these steps **before the labcamp starts**. If you run into issues, check [Troubleshooting](#troubleshooting).

You will use a **terminal** (macOS **Terminal** or **iTerm**, Windows **PowerShell** or **Git Bash**, Linux your distro’s terminal) and a **code editor** is optional for reading files.

---

## 1. Python 3.11+

=== "macOS / Linux"

    ```bash
    python3 --version
    ```

    You need **3.11** or newer. If the command fails or the version is too old, install from [python.org](https://www.python.org/downloads/) or, on macOS with [Homebrew](https://brew.sh/), `brew install python@3.12`.

=== "Windows"

    ```powershell
    py -3 --version
    ```

    You need **3.11** or newer. If `py` is missing, install from [python.org](https://www.python.org/downloads/) and tick **“Add python.exe to PATH”** (or use the **Python Launcher** after install). Some systems only have `python`; if `python --version` shows 3.11+, use that instead of `py`.

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

    Install **[Git for Windows](https://git-scm.com/download/win)**. Use **PowerShell** or **Git Bash** for the shell commands in this guide (`cd`, `git`, `python`).

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

=== "macOS / Linux"

    ```bash
    git clone https://github.com/Storm-AI-Reply/ClaudeCode-Labcamp.git
    cd ClaudeCode-Labcamp
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

=== "Windows"

    ```powershell
    git clone https://github.com/Storm-AI-Reply/ClaudeCode-Labcamp.git
    cd ClaudeCode-Labcamp
    py -3 -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

    If PowerShell blocks activation, run once: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`. In **cmd.exe** use `.venv\Scripts\activate.bat` instead of `Activate.ps1`.

---

## 5. Confirm the app runs

From the **repository root**, with the **venv activated**:

=== "macOS / Linux"

    ```bash
    cd labs/01-execution-model/starter
    uvicorn main:app --reload
    ```

=== "Windows"

    ```powershell
    cd labs\01-execution-model\starter
    uvicorn main:app --reload
    ```

Visit [http://localhost:8000/docs](http://localhost:8000/docs). You should see the quiz-night API documentation page. Stop the server with **Ctrl+C** (same on all platforms).

!!! warning "Do not run pytest during setup"
    The Lab 01 starter has intentional bugs; fixing them is the exercise.

---

## Hooks and MCP (all operating systems)

Lab hooks and the MCP server in `.claude/settings.json` use the command **`python`**. After you activate the venv, `python` should be the interpreter that has `ruff`, `mcp`, and the rest of `requirements.txt`.

If Claude Code cannot find `python`, set the hook/MCP command to your venv executable explicitly, for example `./.venv/bin/python` (macOS/Linux) or `.venv\Scripts\python.exe` (Windows).

---

## Moving between labs

`cd` into the next lab’s starter. The venv stays **active** in the same terminal session.

=== "macOS / Linux"

    ```bash
    cd ../../../labs/02-project-configuration/starter    # from Lab 01
    cd ../../../labs/03-control-connect/starter          # from Lab 02
    cd ../../../labs/04-scale-reuse/starter              # from Lab 03
    cd ../../../labs/final-project/starter               # from Lab 04
    ```

=== "Windows"

    ```powershell
    cd ..\..\..\labs\02-project-configuration\starter    # from Lab 01
    cd ..\..\..\labs\03-control-connect\starter          # from Lab 02
    cd ..\..\..\labs\04-scale-reuse\starter              # from Lab 03
    cd ..\..\..\labs\final-project\starter               # from Lab 04
    ```

---

## Resetting a lab

From inside a lab’s `starter/` folder:

```bash
git checkout -- .
```

That restores tracked files to the last commit. Requires Git ([section 2](#2-git)).

---

## Troubleshooting

??? question "`python3: command not found` (macOS/Linux)"
    Install Python 3.11+ from [python.org](https://www.python.org/downloads/). On macOS with Homebrew: `brew install python@3.12`.

??? question "`py` is not recognized (Windows)"
    Reinstall Python from [python.org](https://www.python.org/downloads/) and enable the launcher/PATH options, or use `python` if `python --version` shows 3.11+.

??? question "`git: command not found`"
    Install Git ([section 2](#2-git)) and open a **new** terminal window.

??? question "`pytest` or `uvicorn` not found"
    The venv is not active. From the repo root: `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\Activate.ps1` (Windows), then try again.

??? question "Port 8000 already in use"
    Use a different port: `uvicorn main:app --reload --port 8001`

??? question "`ModuleNotFoundError: No module named 'fastapi'`"
    You are running Python outside the venv. Activate it first, or use `python -m pip install -r requirements.txt` from the repo root with the venv activated.

??? question "Quiz data disappeared"
    The app uses **in-memory storage**. Restarting `uvicorn` wipes all data; keep the server running throughout each lab.

??? question "Claude Code rate limited"
    Each group shares one account. Wait 30 seconds and try again. Keep prompts focused.

??? question "Phones cannot connect (Final Project)"
    Start the server with `--host 0.0.0.0` and use your laptop’s local IP (not `localhost`). Phones must be on the same Wi‑Fi.

??? question "MCP server not connecting"
    Check that `"command"` is `"python"` (not `"python3"`), `"args"` is `["mcp_server/server.py"]`, you restarted Claude after editing settings, and `/mcp` lists the tools.
