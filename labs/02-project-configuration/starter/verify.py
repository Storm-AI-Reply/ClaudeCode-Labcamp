"""Run this after finishing Lab 02 to check your work.

Verifies that tests still pass, your CLAUDE.md has the key sections,
and all three custom commands are in place.
"""
import subprocess
import sys
from pathlib import Path


REQUIRED_COMMANDS = {"summarize-pr", "write-questions", "restyle"}
REQUIRED_CLAUDEMD_MARKERS = [
    "visual identity",
    "live/",
    "options",
]


def main() -> int:
    starter = Path(__file__).resolve().parent
    failures: list[str] = []

    result = subprocess.run(
        ["pytest", "-q"], cwd=starter, capture_output=True, text=True
    )
    if result.returncode != 0:
        failures.append("pytest failed:\n" + result.stdout + result.stderr)

    claudemd = starter / "CLAUDE.md"
    if not claudemd.exists():
        failures.append("CLAUDE.md not found at lab root")
    else:
        content = claudemd.read_text().lower()
        for marker in REQUIRED_CLAUDEMD_MARKERS:
            if marker.lower() not in content:
                failures.append(f"CLAUDE.md is missing section or keyword: {marker!r}")

    commands_dir = starter / ".claude" / "commands"
    if not commands_dir.is_dir():
        failures.append(".claude/commands/ directory missing")
    else:
        found = {p.stem for p in commands_dir.glob("*.md")}
        missing = REQUIRED_COMMANDS - found
        if missing:
            failures.append(
                "missing required custom commands in .claude/commands/: "
                + ", ".join(sorted(missing))
            )

    if failures:
        print("Lab 02 verification FAILED:\n")
        for f in failures:
            print(" - " + f)
        return 1
    print("Lab 02 passed. Claude now knows your theme and you have 3 reusable commands.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
