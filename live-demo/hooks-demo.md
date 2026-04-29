# Hooks – live demo

```bash
cat > .claude/settings.json << 'EOF'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read|Edit|Write|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "INPUT=$(cat); FILE=$(echo \"$INPUT\" | jq -r '.tool_input.file_path // .tool_input.command // \"\"'); echo \"$FILE\" | grep -q 'labs/04-scale-reuse/starter/live' && echo '{\"continue\":false,\"stopReason\":\"⛔ Access denied: questa cartella è off-limits durante il live demo.\"}' || true"
          }
        ]
      }
    ]
  }
}
EOF
```

Verify with:
```
/hooks
```

Trigger it:
```
Leggi il file @labs/04-scale-reuse/starter/live/.gitkeep
```
