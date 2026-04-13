# Setup

Complete these steps **before the labcamp starts**. For the full formatted guide (tabs for macOS/Linux/Windows), use the **[labcamp documentation site](https://storm-ai-reply.github.io/ClaudeCode-Labcamp/setup/)** ([repository](https://github.com/Storm-AI-Reply/ClaudeCode-Labcamp)).

## 1. Install Python 3.11+

```bash
python3 --version   # must be 3.11 or higher
```

If you need to install it: [python.org/downloads](https://www.python.org/downloads/)

## 2. Install Claude Code

**macOS / Linux:**

```bash
curl -fsSL https://claude.ai/install.sh | bash
claude --version
claude   # authenticate when prompted, then exit with /exit
```

**Windows (PowerShell):**

```powershell
irm https://claude.ai/install.ps1 | iex
```

## 3. Clone and set up

```bash
git clone https://github.com/Storm-AI-Reply/ClaudeCode-Labcamp.git
cd ClaudeCode-Labcamp
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 4. Verify the app runs

```bash
cd labs/01-execution-model/starter
uvicorn main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs), you should see the quiz-night API docs. Press `Ctrl+C` to stop.

> **Do not run `pytest` during setup.** The Lab 01 starter has intentional bugs, fixing them is the exercise.

## Moving between labs

`cd` into the next lab's starter. The venv stays active:

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

**`python3: command not found`**
Install Python 3.11+ from [python.org](https://www.python.org/downloads/). On macOS: `brew install python@3.12`.

**`pytest` or `uvicorn` not found**
The venv is not activated. Run `source .venv/bin/activate` from the repo root.

**Port 8000 already in use**
Use a different port: `uvicorn main:app --reload --port 8001`

**`ModuleNotFoundError: No module named 'fastapi'`**
You are running Python outside the venv. Activate it first.

**Quiz data disappeared**
The app uses in-memory storage. Restarting `uvicorn` wipes all data, keep the server running throughout each lab.

**Claude Code rate limited**
Each group shares one account. Wait 30 seconds and try again. Keep prompts focused.

**Phones cannot connect (Final Project)**
Start the server with `--host 0.0.0.0` and use your laptop's local IP address (not `localhost`). Phones must be on the same Wi-Fi.

**MCP server not connecting**
Check that `"command"` is `"python"` (not `"python3"`), `"args"` is `["mcp_server/server.py"]`, you restarted Claude after editing settings, and `/mcp` lists the tools.
