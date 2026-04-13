# Final Project: Run Quiz Night

> You are not starting from scratch. You are **assembling**. Every lab handed you a piece. Now wire them together, fetch your content, polish your UI, and win the room.

**Time:** ~30 min

---

## What you already have

| From | What you bring in |
|------|-------------------|
| Lab 01 | Working quiz API + committed theme |
| Lab 02 | `CLAUDE.md` with your identity, `/write-questions`, `/restyle` |
| Lab 03 | Permission hooks, lint hook, Quiz Content MCP |
| Lab 04 | `design-system` skill (auto-loaded), `/polish-page` skill |

## What's already set up

- **`GET /quizzes/{id}/play`**, current question + leaderboard (functional but ugly)
- **`POST /quizzes/{id}/answer`**, wired to backend scoring
- **`GET /quizzes/{id}/join`**, QR code for phones
- `.claude/` folder with everything from Labs 01–04 pre-loaded

!!! note "Every group is playable from minute one"
    The competition is about making it *beautiful and memorable*.

## Setup

```bash
cd labs/final-project/starter
source ../../../.venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0
```

!!! warning "In-memory storage"
    Restarting `uvicorn` wipes all data. Keep the server running.

---

## Your mission

!!! tip "Do not ship the default vibe"
    Treat prompts in this page as **starting points**, not scripts to copy blindly. The strongest teams personalize topic, tone, visual identity, mechanics, and pacing so their quiz feels unmistakably theirs.

### 1. Fill your quiz with content

Target: **10 questions with images.** Each question can include an optional **`image_url`** field on `POST /quizzes/{id}/questions`; the play page uses it as a background when present (see `src/schemas/quiz.py`).

=== "Using the command"
    ```
    /write-questions <your topic>
    ```

=== "Using MCP directly"
    ```
    Use get_trivia to fetch 10 questions about <topic> and insert them into quiz 1.
    For each question, fetch a matching background image via get_topic_image.
    ```

### 2. Make it yours

```
/restyle src/templates/play.html
/restyle src/templates/join.html
```

The `design-system` skill auto-applies your theme. Any framework is fair game, keep the API contract stable.

### 3. Polish

```
/polish-page src/templates/play.html
/polish-page src/templates/join.html
```

### 4. Security pass

```
Audit the codebase for security issues. Output structured findings to
security-audit.md. Do not load file contents into this session.
```

### 5. Play-test

1. Create a quiz: `Create a quiz called "<theme>" with topic "<topic>".`
2. Open `http://<your-ip>:8000/quizzes/1/join` on a phone via QR.
3. Open `http://<your-ip>:8000/quizzes/1/play` on the laptop.
4. Answer on the phone. Verify the leaderboard updates.

---

## Handy prompts

!!! note "Customize before you run"
    Edit these prompts with your theme, audience, and style constraints. If every team runs the same text, every app converges to the same result.

```
/restyle src/templates/play.html
/polish-page src/templates/play.html
/write-questions <your topic>
Use get_trivia to fetch 10 questions about <topic> and insert them into quiz 1.
Add a results page at /quizzes/{id}/results that shows the final leaderboard.
Make the play page mobile-friendly with responsive layout.
```

---

## Scoring

| Criterion | Points |
|-----------|--------|
| **Works end-to-end**: join, answer, leaderboard | 25 |
| **Claude Code config**: CLAUDE.md, commands, hooks, skills, MCP | 25 |
| **Quiz content**: creative, entertaining, on-theme | 25 |
| **Beautiful UI**: visual craft, polish, identity | 25 |
| **Total** | **100** |

!!! tip "The winner gets bragging rights"
    The most beloved quiz is replayed as an encore.

---

## Verify

```bash
python verify.py
```
