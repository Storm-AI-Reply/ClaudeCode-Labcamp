"""PreToolUse hook: blocks writes to the live/ directory.

Claude Code calls this script before every file write or edit.
If the target path is under live/, the script denies the operation.
"""
import json
import sys


def main() -> None:
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
