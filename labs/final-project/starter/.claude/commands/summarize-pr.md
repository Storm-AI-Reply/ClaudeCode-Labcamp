---
description: Summarize the current git diff as a structured PR description.
---

You are preparing a pull request description for the current branch.

1. Run `git status` and `git diff` (use `git diff main...HEAD` if the branch
   has diverged from `main`).
2. Read the diff carefully. Do **not** guess, only describe changes you can
   see in the diff.
3. Produce a PR description with exactly these sections, in this order:

```markdown
## What
- bullet list of changes, grouped by area (routes, services, tests, docs, ...)

## Why
- 1–3 bullets explaining the motivation and the user-visible impact

## Risk
- bullets calling out anything that could break: new dependencies, migrations,
  changed API contracts, deleted code, perf concerns. If there are no risks,
  say "Low, refactor/test only."
```

Keep it tight: no filler, no restating file names already obvious from the diff.
