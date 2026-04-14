# quiz-night: design contract

This file is the contract between your group and Claude. When Claude edits
this codebase, it should follow everything below without being reminded.

> The visual identity below is a placeholder, replace the values with
> your group's real theme to make Claude apply your identity automatically.

## Project basics

- **App:** `quiz-night`, a trivia quiz builder and runner (FastAPI + Jinja2).
- **Run locally:** `uv run uvicorn main:app --reload`
- **Tests:** `uv run pytest` (run from this starter directory)
- **Lint:** `uv run ruff check .`
- **Dependencies:** managed by uv. Run `uv sync` once from the repo root.

## Code conventions

- Every `QuestionCreate` must have **exactly 4 options**. Enforced in
  `src/schemas/quiz.py` via `field_validator`.
- `correct_index` must be in `0..3`. Enforced via `Field(ge=0, le=3)`.
- All HTML is served from `src/templates/`. Do not inline HTML in Python.
- All CSS lives in `src/static/style.css`. Do not emit `<style>` tags in
  templates.
- Errors raised by services are `AppError` subclasses; response shape is set
  by `register_exception_handlers` in `src/middleware/errors.py`, do not
  return ad-hoc error dicts from route handlers.

## Visual identity (placeholder: replace with your group's sticky)

- **Theme name:** Quiz Night, Default
- **Palette:**
  - `--color-bg: #0a0a0f`
  - `--color-surface: #16161f`
  - `--color-accent: #ff4d5e`
  - `--color-text: #f5f5f7`
  - `--color-muted: #8a8a99`
- **Typography:**
  - Display: `"Space Grotesk", sans-serif`, 600 weight, -0.02em tracking
  - Body: `"Inter", sans-serif`, 400 weight
- **Animation:** snappy (180ms), respect `prefers-reduced-motion: reduce`.

## Voice & tone

Quiz questions should sound **playful and slightly dry**, like a well-read
friend running the round, not a game show host. Avoid exclamation marks.
Never condescend to the player.

## Hard constraints

- **Never write to `live/`.** This directory holds snapshots of quizzes that
  are currently being played. Editing a file in `live/` mid-round will break
  player sessions.
- **Never return a tuple from a FastAPI route handler.** Raise an `AppError`
  subclass instead, or use `HTTPException`.

## Do / Never

- **DO** use CSS variables from the palette above.
- **DO** add tests under `tests/` whenever you change a route.
- **NEVER** bypass `QuestionCreate` validation by accepting `dict`.
- **NEVER** add inline styles to templates.
