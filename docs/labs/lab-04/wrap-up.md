# Lab 04: Wrap-up

**Lab:** [Lab 04 overview](index.md)

---

## Verify

```bash
uv run python verify.py
```

## Stretch goals

- Create a custom subagent in `.claude/agents/security-auditor.md`
- Add a skill that auto-generates alt text for images
- Try `/agents`

## Recap

| Concept | Takeaway |
|---------|----------|
| Subagents | Own context window, parent stays lean |
| Skills | Auto-loading for background knowledge, invoke-only for explicit workflows |
| Commands vs. skills | Commands = reusable prompts. Skills = auto-loading + argument hints |

---

[← Exercise 2](exercise-2.md) · **Next:** [Final Project](../../final-project.md)
