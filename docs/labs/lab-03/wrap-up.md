# Lab 03: Wrap-up

**Lab:** [Lab 03 overview](index.md)

---

## Verify

```bash
python verify.py
```

## Stretch goals

- Write a third MCP tool in `server.py`
- Try the offline fallback
- What would a `SessionStart` hook be useful for?

## Recap

| Concept | Takeaway |
|---------|----------|
| Permission modes | Tune Claude's autonomy from `plan` to `bypassPermissions` |
| Hooks | PreToolUse blocks, PostToolUse auto-lints |
| MCP | Connects Claude to external data |
| Convention → Guardrail | Lab 02 *asked*. The hook now *enforces*. |

---

[← Exercise 2](exercise-2.md) · **Next:** [Lab 04: Scale & Reuse](../lab-04/index.md)
