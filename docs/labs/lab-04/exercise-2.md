# Exercise 2: Skills for Frontend Craft

> Build two skills, one that auto-loads your design system, another that polishes pages on demand.

**Lab:** [Lab 04 overview](index.md)

??? info "Theory: Skills (SKILL.md)"

    **What it is.** A skill is a reusable capability stored under `.claude/skills/<skill-name>/SKILL.md`. It combines metadata (YAML frontmatter) + instructions (markdown body) so Claude can apply a focused playbook when relevant.

    **How it differs from other tools:**

    - `CLAUDE.md` = broad, always-on project guidance.
    - **Command** (`.claude/commands/*.md`) = explicit slash command you run.
    - **Skill** = targeted knowledge/procedure that can auto-load by relevance or be slash-invoked.

    **How loading works (important):**

    - Skills are **discovered from the skill directories**, then loaded when needed.
    - They are not all dumped into context at session start.
    - If a skill name conflicts with a command name, the skill wins.

    **Minimum anatomy of `SKILL.md`:**

    - Frontmatter: `name`, `description` (plus optional behavior flags).
    - Body: concrete rules/checklists/examples Claude should follow.
    - Keep each skill single-purpose and specific; split large topics into multiple skills.

    **Use case example:**

    - You create a `design-system` skill with your colors, spacing, and typography.
    - Later you ask: "Build a new leaderboard page."
    - Claude auto-loads that skill and applies your visual rules without you repeating them.

    Further reading: [Extend Claude with skills](https://code.claude.com/docs/en/skills.md) · [Explore the `.claude` directory](https://code.claude.com/docs/en/claude-directory.md) · [Commands reference](https://code.claude.com/docs/en/commands.md)

---

### Hands-on

!!! tip "Make the skill yours"
    Do not keep placeholder values. Replace tokens, typography, spacing, and tone with your real creative direction so Claude applies a distinct identity automatically.

#### Part 1: `design-system` Skill (Auto-Load Only)

1. Create `.claude/skills/design-system/SKILL.md`:
    ```markdown
    ---
    name: design-system
    description: The visual design system for this quiz app, color tokens, typography, spacing, animation rules. Use whenever writing or editing HTML, CSS, templates, or any user-facing markup.
    user-invocable: false
    ---

    # Design System, <Your Theme Name>

    ## Color tokens
    --color-bg: #0a0a0f;
    --color-surface: #16161f;
    --color-accent: #ff4d5e;
    --color-text: #f5f5f7;
    --color-muted: #8a8a99;

    ## Typography
    Display: "Space Grotesk", sans-serif, 600 weight, -0.02em tracking
    Body: "Inter", sans-serif, 400 weight
    Mono: "JetBrains Mono", monospace

    ## Spacing rhythm
    4px base, multiples of 4 only.

    ## Animation
    - Respect prefers-reduced-motion: reduce
    - Default transition: 180ms cubic-bezier(0.2, 0.8, 0.2, 1)

    ## Do / Never
    DO: use CSS variables, semantic HTML, visible focus rings
    NEVER: inline styles, animations without reduced-motion fallback
    ```
2. **Replace** placeholders with your own real values.
3. New session → ask Claude to add a `/quizzes/{id}/winner` page. Don't mention the theme. Verify it auto-applies.
4. Run `/context` to confirm the skill loaded.

#### Part 2: `polish-page` Skill (Invoke-Only)

1. Create `.claude/skills/polish-page/SKILL.md`:
    ```markdown
    ---
    name: polish-page
    description: Run a structured UI polish pass on an HTML file.
    argument-hint: <file-path>
    disable-model-invocation: true
    ---

    # Polish Page

    Audit $ARGUMENTS against these rules:

    1. **Contrast**, WCAG AA (4.5:1 body, 3:1 large text)
    2. **Focus states**, visible focus ring on every interactive element
    3. **Keyboard navigation**, no mouse-only flows; logical tab order
    4. **Reduced motion**, animations in @media (prefers-reduced-motion: no-preference)
    5. **Touch targets**, >= 44x44px on mobile
    6. **Typography hierarchy**: consistent with design-system skill

    Output: file:line, severity (critical/high/medium), finding, fix.
    Auto-fix the safe ones. Report the rest. End with summary and score (1-10).
    ```
2. Test: `/polish-page src/templates/play.html`.

#### Part 3: Reflect: Command vs Skill

| | `/restyle` | `/polish-page` | `design-system` |
|---|---|---|---|
| Type | Command | Skill (invoke-only) | Skill (auto-load) |
| Auto-loads? | No | No | Yes |
| Best for | Free-form restyling | Accessibility audit | Background knowledge |

!!! note "Rule of thumb"
    Commands for reusable prompts. Skills when knowledge should load itself or you want argument hints.

!!! success "Checkpoint"
    - [x] `design-system` auto-loads on HTML/CSS work
    - [x] `/polish-page` appears in the `/` menu but does not auto-load
    - [x] The play page looks better than before

---

[← Exercise 1](exercise-1.md) · [Wrap-up →](wrap-up.md)
