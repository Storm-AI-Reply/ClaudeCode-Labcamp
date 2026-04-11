# Exercise 1: Subagents for Parallel UI Audits

> Your app has multiple templates. Reading every file in your main session burns context. Subagents work in their own context window and return only a summary.

**Lab:** [Lab 04 overview](index.md)

??? info "Theory: Subagents"

    **What it is.** Specialized AI assistants in their own context window. Claude delegates matching tasks to them.

    **Built-in subagents:**

    | Agent | Model | Purpose |
    |---|---|---|
    | Explore | Haiku (fast) | Read-only codebase search |
    | Plan | Same as parent | Research for plan mode |
    | General-purpose | Same as parent | Multi-step read + write tasks |

    You can also create custom subagents in `.claude/agents/`.

    **Gotcha.** Subagents cannot spawn other subagents, the parent orchestrates everything.

    **Key commands:** `/agents` (list), `/context` (check usage savings)

    Further reading: [Create custom subagents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)

---

### Hands-on

#### Part 1: Baseline

1. Start Claude, run `/context`. Note the number.

#### Part 2: Subagent Audit

2. Ask:
    ```
    Spawn a subagent to audit every file in src/templates/ against the visual
    identity in CLAUDE.md. For each file, report: file name, severity
    (high/medium/low), and specific issues. Save the report as ui-audit.md.
    ```
3. Run `/context`, template contents should not have accumulated.

!!! tip "Rotate the driver"
    Hand the keyboard to the next person.

#### Part 3: Parallel Subagents

4. Spawn two at once:
    ```
    Spawn two subagents in parallel:
    1. One audits all files in src/templates/ against our visual identity.
    2. One audits src/static/style.css against our design system.
    Merge both reports and identify the top 3 fixes.
    ```

#### Part 4: Inline Comparison

5. Fresh session, same audit inline (no subagent).
6. Run `/context`. Compare.
7. Discuss: when would you use subagents vs. inline?

!!! success "Checkpoint"
    - [x] `ui-audit.md` exists with theme-specific findings
    - [x] Parallel reports were received and merged
    - [x] Context difference is quantified

---

[← Lab 04 overview](index.md) · [Exercise 2: Skills →](exercise-2.md)
