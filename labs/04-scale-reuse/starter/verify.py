"""Run this after finishing Lab 04 to check your work.

Verifies that your tests pass, the subagent audit report exists,
and both skills are set up correctly.
"""
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

    audit = starter / "ui-audit.md"
    if not audit.exists():
        failures.append(
            "ui-audit.md is missing — did you run the subagent audit?"
        )

    design_skill = starter / ".claude" / "skills" / "design-system" / "SKILL.md"
    if not design_skill.exists():
        failures.append(
            ".claude/skills/design-system/SKILL.md is missing"
        )

    polish_skill = starter / ".claude" / "skills" / "polish-page" / "SKILL.md"
    if not polish_skill.exists():
        failures.append(
            ".claude/skills/polish-page/SKILL.md is missing"
        )

    if failures:
        print("Lab 04 verification FAILED:\n")
        for f in failures:
            print(" - " + f)
        return 1
    print("Lab 04 verification passed. Nice work — subagents and skills are ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
