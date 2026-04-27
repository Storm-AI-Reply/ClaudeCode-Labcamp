# Exercise 2: Custom Commands That Do Real Work

> Custom commands are reusable prompt templates. You will build three that you'll use in the final project.

**Lab:** [Lab 02 overview](index.md)

??? info "Theory: Custom Slash Commands"

    **What it is.** Markdown files in `.claude/commands/` that create reusable `/command-name` invocations. Commands accept arguments via `$ARGUMENTS`.

    **Example:**

    ```markdown
    ---
    description: Generate quiz questions on a topic.
    argument-hint: <topic>
    ---

    Generate 5 quiz questions about: $ARGUMENTS
    Read CLAUDE.md for voice & tone rules...
    ```

    `/write-questions 90s video games` → Claude replaces `$ARGUMENTS` with `90s video games`.

    **Gotcha.** If a command and a skill share the same name, the skill takes precedence.

    Further reading: [Extend Claude with skills](https://docs.anthropic.com/en/docs/claude-code/skills)

---

### Hands-on

#### Part 1: `/summarize-pr` (no arguments)

1. Create `.claude/commands/summarize-pr.md`:
    ```markdown
    ---
    description: Summarize the current git diff as a structured PR description.
    ---

    You are preparing a pull request description for the current branch.

    1. Run `git status` and `git diff`.
    2. Read the diff carefully. Do not guess, only describe changes you can see.
    3. Produce a PR description with exactly these sections:

    ## What
    - bullet list of changes, grouped by area

    ## Why
    - 1–3 bullets explaining the motivation

    ## Risk
    - anything that could break. If no risks, say "Low, refactor only."
    ```
2. Test: make a small edit, then run `/summarize-pr`.

!!! note
    `/summarize-pr` summarises the full `git diff`. If you haven't committed between labs, the output will include changes from Lab 01. This is expected.

#### Part 2: `/write-questions` (parameterized)

You already asked Claude to generate questions manually in Exercise 1. This command formalises that one-off request — write the prompt once, run it any time without repeating yourself.

1. Create `.claude/commands/write-questions.md`:
    ```markdown
    ---
    description: Generate 5 quiz questions on a topic, using your voice & tone.
    argument-hint: <topic>
    ---

    Generate exactly 5 quiz questions about: $ARGUMENTS

    Before writing, read CLAUDE.md and extract the voice & tone rules and the
    schema constraints (4 options, correct_index 0–3).

    Output a JSON array that can be passed to POST /quizzes/{id}/questions.
    After the JSON, add a one-line note on editorial choices.
    ```
2. Test: `/write-questions 90s video games`. Tune until consistent.

#### Part 3: `/restyle` (domain-specific)

`/restyle` is the reusable version of the manual theming you did in Exercise 1. Instead of a one-off request, you are codifying the action into a command any team member can invoke consistently.

1. Create `.claude/commands/restyle.md`:
    ```markdown
    ---
    description: Rewrite a template's HTML/CSS to match the visual identity in CLAUDE.md.
    argument-hint: <file-path>
    ---

    Restyle the file at: $ARGUMENTS

    1. Read CLAUDE.md and pull out the Visual identity section.
    2. Read the target file. Understand its structure before touching it.
    3. Rewrite so all colors come from CSS variables in src/static/style.css,
       typography matches the fonts in CLAUDE.md, and no inline styles remain.
    4. Preserve all Jinja variables, form fields, and element IDs.
    5. Summarize what you changed in 2–3 bullets.
    ```
2. Test: `/restyle src/templates/play.html`.
3. Verify the result at `http://127.0.0.1:8000/quizzes/1/play` (make sure the dev server is running: `uv run uvicorn main:app --reload`). No quiz yet? Ask Claude to create one first.

!!! success "Checkpoint"
    - [x] All three commands appear in the `/` menu
    - [x] `/write-questions` produces 5 valid, on-voice questions
    - [x] `/restyle` visibly transforms a template

---

[← Exercise 1](exercise-1.md) · [Wrap-up →](wrap-up.md)
