"""Run this after finishing Lab 03 to check your work.

Verifies that tests pass, both hooks are configured, MCP servers
are registered, and the guard script exists.
"""
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    starter = Path(__file__).resolve().parent
    failures: list[str] = []

    result = subprocess.run(
        ["pytest", "-q"], cwd=starter, capture_output=True, text=True
    )
    if result.returncode != 0:
        failures.append("pytest failed:\n" + result.stdout + result.stderr)

    settings_path = starter / ".claude" / "settings.json"
    if not settings_path.exists():
        failures.append(".claude/settings.json is missing")
    else:
        try:
            settings = json.loads(settings_path.read_text())
        except json.JSONDecodeError as e:
            failures.append(f".claude/settings.json is not valid JSON: {e}")
            settings = {}

        hooks = settings.get("hooks", {})
        pre = hooks.get("PreToolUse", [])
        post = hooks.get("PostToolUse", [])

        if not pre:
            failures.append("PreToolUse hooks are empty — did you add the live/ guard?")
        elif "guard_live" not in json.dumps(pre) and "live" not in json.dumps(pre):
            failures.append("PreToolUse hook doesn't seem to reference a live/ guard script")

        if not post:
            failures.append("PostToolUse hooks are empty — did you add the ruff lint hook?")
        elif "ruff" not in json.dumps(post):
            failures.append("PostToolUse hook doesn't seem to invoke ruff")

        if not settings.get("mcpServers"):
            failures.append(
                "no MCP servers registered under mcpServers in .claude/settings.json"
            )

    guard_script = starter / ".claude" / "hooks" / "guard_live.py"
    if not guard_script.exists():
        failures.append(".claude/hooks/guard_live.py is missing")

    if failures:
        print("Lab 03 verification FAILED:\n")
        for f in failures:
            print(" - " + f)
        return 1
    print("Lab 03 passed. Your guardrails are active and MCP servers are connected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
