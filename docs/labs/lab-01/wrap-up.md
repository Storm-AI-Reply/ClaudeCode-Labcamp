# Lab 01: Wrap-up

**Lab:** [Lab 01 overview](index.md)

---

## Pick your theme

*5 minutes, end of lab*

Decide, for yourself:

1. **Topic**, what will your quiz be about? (e.g., "90s video games", "Renaissance art", "obscure flags")
2. **Visual identity**, Brutalist newspaper · 80s synthwave · Art deco poster · Terminal/hacker · Retro arcade · Swiss minimalist · Maximalist zine · … or invent your own
3. Jot both down somewhere you'll keep near your laptop for the rest of the day.

!!! note "Every subsequent lab builds on this choice"
    Lab 02: teach Claude your identity. Lab 03: pull real content. Lab 04: make Claude write on-brand code by default. For the final project you will regroup in a team of 5 and pick a shared theme; the one you choose now is *yours* for Labs 02-04.

---

## Verify

```bash
uv run python verify.py
```

## Stretch goals

- Try `claude --permission-mode acceptEdits` and observe the difference
- Refactor `quiz_service.py` with and without a plan, compare tool call counts
- Explore `/help`

## Recap

| Concept | Takeaway |
|---------|----------|
| Agentic loop | Claude works in cycles of tool calls and observations, not one-shot answers |
| Plan Mode | Review before execution, your preflight check |
| Context management | `@` references, `/context`, `/compact` keep sessions efficient |

---

[← Exercise 2](exercise-2.md) · **Next:** [Lab 02: Project Configuration](../lab-02/index.md)
