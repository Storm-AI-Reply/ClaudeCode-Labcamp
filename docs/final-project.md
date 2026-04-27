# Final Project: Run Quiz Night

> Labs 01-04 were yours alone. The final project is a team sport. Form a team of 5, pick a shared theme, and ship the **most beautiful and original quiz in the room**.

**Time:** ~30 min

---

## How teams work

- **Team size:** 5 people.
- **Starting point:** everyone on the team clones / moves to `labs/final-project/starter`. It is a clean baseline with all the Claude Code features from the previous labs already wired up (CLAUDE.md, slash commands, hooks, MCP servers, skills).
- **Bring your best pieces from Labs 01-04.** Your individual work is reusable: if you built a better skill, command, hook, prompt, UI pattern, or feature, integrate it into the team project.
- **Why the shared starter exists:** to align the team quickly on one codebase, not to throw away personal work. Start from a common base, then import and merge what already worked well in your individual labs.
- **The starter is a baseline, not the destination.** Do not ship what the starter gives you. Pick a shared theme, rethink the visual identity, add your own mechanics, sounds, animations, copy, pacing. Just keep the API contract stable so phones can still join and answer.

!!! tip "Aim for original, not complete"
    A rough, weird, opinionated quiz beats a polished generic one. The best 30 minutes you can spend are on the 2 or 3 ideas only your team would have.

---

## What the starter gives you

The team never has to rebuild the plumbing. The starter already contains:

| Pre-configured asset | Where | What it does |
|----------------------|-------|--------------|
| `CLAUDE.md` design contract | `./CLAUDE.md` | App description, code conventions, placeholder visual identity, hard constraints. **Replace the identity section with your team's theme.** |
| Slash commands | `.claude/commands/` | `/summarize-pr`, `/write-questions`, `/restyle` |
| Hooks | `.claude/hooks/` + `settings.json` | `guard_live.py` (protects `live/`), `lint_python.py` (runs ruff after edits) |
| MCP servers | `mcp_server/` + `.mcp.json` | `trivia-content` (real trivia questions), `wiki-images` (Wikipedia images) |
| Skills | `.claude/skills/` | `design-system` (auto-loads on HTML/CSS), `polish-page` (invoke-only audit) |
| Playable app | `src/` | `GET /join` (QR code) · `GET /play` (question + leaderboard) · `POST /answer` already wired |

!!! note "Every team is playable from minute one"
    The competition is about making it **beautiful, on-theme, and memorable**, not about fixing the plumbing.

!!! tip "Reuse is encouraged"
    Treat your individual labs as a library of ideas and assets. Copy what is useful, adapt it to the shared team theme, and build from there.

---

## Setup

```bash
cd labs/final-project/starter
uv run uvicorn main:app --reload --host 0.0.0.0
```

Keep this terminal running. Phones join via `http://<your-laptop-ip>:8000/quizzes/1/join` while you play.

!!! warning "In-memory storage"
    Restarting `uvicorn` wipes all data. Keep the server running throughout the demo.

---

## Your Claude Code toolbox

You are not obliged to use every feature. Use the ones that actually pay off in 30 minutes. These are the moments where each feature tends to shine, pick the ones that fit your plan:

- **Plan Mode (`Shift+Tab`)** — anything multi-step or risky (new results page, layout overhaul, refactor). Read the plan, tweak it, then execute.
- **`@` references + `/compact`** — when you feel Claude slowing down or burning context on files it doesn't need.
- **`CLAUDE.md`** — update the visual identity and voice & tone sections with your team's theme so every session starts on-brand.
- **Custom slash commands** (`/write-questions`, `/restyle`, or new ones) — for any prompt you'll run more than twice.
- **Hooks** (`guard_live.py`, `lint_python.py`) — already active. Add your own `PostToolUse` hook if you want auto-format or tests on every edit.
- **MCP servers** (`trivia-content`, `wiki-images`) — fetch real content instead of asking Claude to invent it.
- **Subagents** — for parallel audits (UI vs CSS, accessibility vs performance), or when a task would otherwise drown your main context.
- **Skills** (`design-system`, `polish-page`) — edit the `design-system` SKILL.md to lock your theme in; `/polish-page` on any template for an accessibility pass.

!!! tip "Rule of thumb"
    If a feature saves you repetition or saves context, use it. We saw each of these in the labs precisely because, in 30 minutes, they make a difference.

---

## Suggested split (5 people, 30 min)

This is a **suggestion**, not an obligation. Divide however you like. Feature hints in parentheses are just to give you a starting point.

| Role | Focus | Claude Code features that help |
|------|-------|-------------------------------|
| **Content lead** | Questions, tone, topic angle | `/write-questions`, `trivia-content` MCP, `CLAUDE.md` voice & tone |
| **Visual lead** | Theme, palette, typography, hero shots | `design-system` skill, `/restyle`, `wiki-images` MCP |
| **Game mechanics** | Timer, scoring, play page polish | Plan Mode, `@` references, subagents for audits |
| **UX & accessibility** | Focus, contrast, mobile layout, motion | `/polish-page` skill, `polish-page` on `join.html` and `play.html` |
| **Integrator / demo** | Merging edits, security pass, end-to-end test | `/summarize-pr`, hooks, security audit subagent |

Sync every 10 minutes. Keep the server running the whole time.

---

## Go beyond the starter

The starter is deliberately minimal. A few seeds you can steal, stack, or ignore:

- **Animated countdown timer** per question (honor `prefers-reduced-motion`).
- **Sound effects** on correct / wrong / round end. A single well-chosen sound changes everything.
- **Results page** with podium and highlight of the funniest wrong answer.
- **Team mode** — two teams, alternating players, shared score.
- **Power-ups** — 50:50, double points, time freeze.
- **Round themes** — first 3 questions easy, last 3 brutal; or a boss question worth 3x.
- **Custom join screen** — instead of a bare QR, a themed landing that hooks people before they play.
- **Confetti, emojis, animated backgrounds** — go bigger than the default palette if it fits your theme.

You do not need to do all of these. Pick one or two and execute them well.

---

## Handy prompts (starting points, not scripts)

!!! note "Customize before you run"
    Edit these prompts with your theme, audience, and style constraints. If every team runs the same text, every app converges to the same result.

```
/restyle src/templates/play.html
/polish-page src/templates/play.html
/write-questions <your topic>

Use the `trivia-content` MCP (`get_questions`) to fetch 10 multiple-choice
questions about <topic> and insert them into quiz 1.
For each question, use the `wiki-images` MCP (`get_topic_image`) and store
`image_url` on the question so the play page uses it as a background.

Add a results page at /quizzes/{id}/results that shows the final
leaderboard with a podium for the top 3.

Spawn a subagent to audit src/templates/ and src/static/style.css against
our design-system skill. Report the top 3 fixes.
```

---

## Scoring (100 points total)

| Criterion | Points |
|-----------|--------|
| **Works end-to-end**: join, answer, leaderboard | 25 |
| **Claude Code config**: smart use of CLAUDE.md, commands, hooks, skills, MCP, subagents where they help | 25 |
| **Quiz content**: creative, entertaining, on-theme | 25 |
| **Beautiful and original UI**: visual craft, polish, identity — *does it look like your team?* | 25 |
| **Total** | **100** |

!!! tip "The starter alone does not win"
    Shipping the starter unchanged scores poorly on the last two criteria. The winning quizzes have a strong point of view, a distinct look, and at least one mechanic the room will remember. The most beloved quiz gets replayed as an encore.

---

## Verify

```bash
uv run python verify.py
```
