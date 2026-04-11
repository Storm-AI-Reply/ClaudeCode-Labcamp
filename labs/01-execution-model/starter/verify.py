"""Run this after finishing Lab 01 to check your work.

Verifies that the bugs are fixed (pytest passes) and that input
validation is wired into the question schema.
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

    schema = (starter / "src" / "schemas" / "quiz.py").read_text()
    if "options" not in schema or "correct_index" not in schema:
        failures.append("src/schemas/quiz.py missing options/correct_index fields")
    if "field_validator" not in schema and "model_validator" not in schema and "Field(" not in schema:
        failures.append(
            "QuestionCreate needs a validator or Field constraints "
            "ensuring options has exactly 4 entries and correct_index is 0..3"
        )

    if failures:
        print("Lab 01 verification FAILED:\n")
        for f in failures:
            print(" - " + f)
        return 1
    print("Lab 01 passed. Don't forget to pick your theme and stick it on the laptop!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
