# Exercise 1: Permissions & Hooks

> In Lab 02, CLAUDE.md *asked* Claude not to write to `live/`. Now you will *enforce* it.

**Lab:** [Lab 03 overview](index.md)

??? info "Theory: Permission Modes"

    | Mode | Behavior |
    |------|----------|
    | `default` | Ask on first use of each tool type |
    | `acceptEdits` | Auto-accept file edits, ask for bash |
    | `plan` | Read-only analysis, no modifications |
    | `auto` | Auto-approve with safety checks |
    | `bypassPermissions` | Skip all prompts (use with caution) |

    Configure in `.claude/settings.json` or override per-session: `claude --permission-mode <name>` / `Shift+Tab`.

    Further reading: [Permission modes docs](https://docs.anthropic.com/en/docs/claude-code/permission-modes)

??? info "Theory: Hooks"

    **What it is.** Shell commands that run automatically before or after Claude's tool calls. `PreToolUse` fires before (can block). `PostToolUse` fires after (can send feedback).

    **Configuration** in `.claude/settings.json`:

    ```json
    {
      "hooks": {
        "PreToolUse": [{
          "matcher": "Write|Edit",
          "hooks": [{ "type": "command", "command": "uv run python .claude/hooks/guard_live.py" }]
        }]
      }
    }
    ```

    **PreToolUse**: deny by printing:

    ```json
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "live/ is protected"
      }
    }
    ```

    **PostToolUse**: send feedback:

    ```json
    {"decision": "block", "reason": "ruff found lint errors: ..."}
    ```

    **Gotcha.** Scripts must exit 0. Non-zero = hook error, not a deny.

    Further reading: [Hooks reference](https://docs.anthropic.com/en/docs/claude-code/hooks) · [Hooks guide](https://docs.anthropic.com/en/docs/claude-code/hooks-guide)

---

### Hands-on

#### Part 1: Try Permission Modes

1. Open `.claude/settings.json`. Note `defaultMode` is `"default"`.
2. Try three rounds of *"Add a comment to main.py"*:
    - `default`, asks before writing
    - `acceptEdits`, writes without asking
    - `plan`, analyzes but does not edit
3. Reset to `"default"`.

!!! tip "Rotate the driver"
    Hand the keyboard to the next person.

#### Part 2: PreToolUse Hook: Guard `live/`

1. Create `.claude/hooks/guard_live.py`:
    ```python
    import json
    import sys

    def main():
        data = json.load(sys.stdin)
        tool_input = data.get("tool_input", {})
        file_path = tool_input.get("file_path", "") or tool_input.get("path", "")

        if file_path.startswith("live/") or "/live/" in file_path:
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": "live/ is protected during quiz play",
                }
            }))

    if __name__ == "__main__":
        main()
    ```
2. Wire it into `.claude/settings.json`:
    ```json
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [{ "type": "command", "command": "uv run python .claude/hooks/guard_live.py" }]
          }
        ],
        "PostToolUse": []
      }
    }
    ```
3. Test:
    - *"Edit live/quiz-001.json and add a test question."* → **denied**
    - *"Edit src/routes/quizzes.py and add a comment."* → **allowed**

!!! tip "Rotate the driver"
    Hand the keyboard to the next person.

#### Part 3: PostToolUse Hook: Auto-Lint

1. Create `.claude/hooks/lint_python.py`:
    ```python
    """PostToolUse hook: run ruff on edited Python files after a write."""
    from __future__ import annotations

    import json
    import subprocess
    import sys
    from pathlib import Path


    def main() -> None:
        data = json.load(sys.stdin)
        tool_input = data.get("tool_input", {})
        file_path = tool_input.get("file_path", "") or tool_input.get("path", "")
        if not file_path or not str(file_path).endswith(".py"):
            return
        path = Path(file_path)
        if not path.is_file():
            return
        result = subprocess.run(
            ["ruff", "check", str(path)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            out = (result.stdout + result.stderr).strip()
            print(json.dumps({"decision": "block", "reason": f"ruff found issues:\n{out}"}))


    if __name__ == "__main__":
        main()
    ```
2. Add to `.claude/settings.json`:
    ```json
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "uv run python .claude/hooks/lint_python.py" }]
      }
    ]
    ```
3. Test: *"Add a function to src/utils.py that uses a bare except clause."*
    Watch: Claude writes it → ruff catches it → Claude fixes it automatically.

!!! success "Checkpoint"
    - [x] `live/` write is blocked (denied, with reason visible)
    - [x] Lint hook fires after Python writes
    - [x] `.claude/settings.json` has both hooks configured

---

[← Lab 03 overview](index.md) · [Exercise 2: MCP →](exercise-2.md)
