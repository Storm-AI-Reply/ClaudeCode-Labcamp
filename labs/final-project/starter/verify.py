"""Run this to check that your capstone is ready to compete.

Verifies that tests pass and all Claude Code configuration pieces
are in place: CLAUDE.md, commands, hooks, MCP, and skills.
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

    if not (starter / "CLAUDE.md").exists():
        failures.append("CLAUDE.md is missing")

    commands_dir = starter / ".claude" / "commands"
    cmd_files = list(commands_dir.glob("*.md")) if commands_dir.exists() else []
    if not cmd_files:
        failures.append("no custom commands found in .claude/commands/")

    settings_path = starter / ".claude" / "settings.json"
    if settings_path.exists():
        try:
            settings = json.loads(settings_path.read_text())
        except json.JSONDecodeError:
            settings = {}

        hooks = settings.get("hooks", {})
        if not hooks.get("PreToolUse"):
            failures.append("PreToolUse hooks are empty")
        if not hooks.get("PostToolUse"):
            failures.append("PostToolUse hooks are empty")
        if not settings.get("mcpServers"):
            failures.append("no MCP servers registered")
    else:
        failures.append(".claude/settings.json is missing")

    skills_dir = starter / ".claude" / "skills"
    skill_files = list(skills_dir.rglob("SKILL.md")) if skills_dir.exists() else []
    if not skill_files:
        failures.append("no skills found in .claude/skills/")

    if failures:
        print("Final project verification FAILED:\n")
        for f in failures:
            print(" - " + f)
        return 1
    print("All checks passed. You're ready to compete — good luck!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
