# Exercise 1: CLAUDE.md as a Design Contract

> You picked a theme in Lab 01. Now teach Claude about it so every future session is on-brand from the start.

**Lab:** [Lab 02 overview](index.md)

??? info "Theory: CLAUDE.md (Project Memory)"

    **What it is.** A markdown file in your project root that Claude reads at the start of every session, persistent instructions without repeating yourself.

    **Two memory systems** (both loaded at conversation start):

    | | CLAUDE.md files | Auto memory |
    |---|---|---|
    | Who writes it | You | Claude |
    | What it contains | Instructions and rules | Learnings and patterns |
    | Use for | Standards, workflows, architecture | Build commands, debugging insights |

    **File locations:**

    | Scope | Location | Shared with |
    |---|---|---|
    | Project | `./CLAUDE.md` | Team (via source control) |
    | User | `~/.claude/CLAUDE.md` | Just you (all projects) |
    | Local | `./CLAUDE.local.md` | Just you (this project) |

    Keep it under 200 lines. Be specific: "Use 2-space indentation" beats "Format code properly."

    **Gotcha.** CLAUDE.md is a convention, not a guardrail. For hard enforcement, you need hooks (Lab 03).

    **Key commands:** `/init` (auto-generate), `/memory` (view/edit)

    Further reading: [How Claude remembers your project](https://docs.anthropic.com/en/docs/claude-code/memory)

---

### Hands-on

#### Part 1: Draft the CLAUDE.md

1. The starter has no CLAUDE.md. Ask Claude to explore and draft one:
    ```
    Explore this codebase and draft a CLAUDE.md for it. Include: what the app does,
    how to run it, how to test it, and our code conventions.
    ```
2. Review it. It will be generic, that is expected.

!!! note "Claude may read outside `starter/`"
    When exploring, Claude walks up the directory tree looking for existing `CLAUDE.md` files and project context — it may read files outside `starter/`. This is expected. The generated `CLAUDE.md` will be scoped to your project once you review and save it.

#### Part 2: Add Your Theme

3. Edit the CLAUDE.md to include:
    - **Project basics**: what the app does, `uv run uvicorn main:app --reload`, `uv run pytest`, `uv run ruff check .`
    - **Code conventions**: 4 options per question, `correct_index` 0–3, HTML in `src/templates/`, CSS in `src/static/style.css`
    - **Visual identity**: theme name, 3–5 color hex codes, font pairing, animation style
    - **Voice & tone**: how questions should read
    - **Hard constraint**: *never write to `live/`*

#### Part 3: Verify It Works

4. Start a **new session** (exit and run `claude` again).
5. Make sure the dev server is running in a separate terminal:
    ```bash
    uv run uvicorn main:app --reload
    ```
    No quiz yet? Ask Claude to create one: *"Create a quiz called '&lt;your theme&gt;' with topic '&lt;topic&gt;' using POST /quizzes."*
6. Test three things:

    | Test | Expected |
    |------|----------|
    | *"What colors should I use for a button?"* | Answers from your palette |
    | *"Edit live/quiz-001.json and add a question."* | Refuses |
    | *"Make @src/templates/play.html match our visual identity."* | Applies your theme — visit `http://127.0.0.1:8000/quizzes/1/play` to verify |

!!! tip "Let it unfold naturally"
    The third test often leads to a short debugging sequence: ask how to launch the app, get the URL, discover there are no quizzes and ask Claude to create one, then notice styling issues and ask Claude to fix them. Let it happen — that step-by-step flow is exactly what you will use in the final project.

!!! success "Checkpoint"
    - [x] `CLAUDE.md` exists with all five sections
    - [x] A new session answers theme questions correctly
    - [x] The `live/` constraint is respected

---

[← Lab 02 overview](index.md) · [Exercise 2: Custom commands →](exercise-2.md)
