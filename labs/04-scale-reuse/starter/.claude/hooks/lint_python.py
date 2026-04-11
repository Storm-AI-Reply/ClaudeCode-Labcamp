"""PostToolUse hook: run ruff on edited Python files after a write.

Uses Python only (no bash) so the same hook works on macOS, Linux, and Windows.
"""
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
