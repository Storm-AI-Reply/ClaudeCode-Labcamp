# Exercise 2: Context Management

> Learn to control what Claude reads, and what it forgets, so your sessions stay fast and focused.

**Lab:** [Lab 01 overview](index.md)

??? info "Theory: Context Window & `@` References"

    **What it is.** Claude operates within a context window, a fixed amount of text it can "see" at once. Every file read, every command output, every message takes up space.

    **Why it matters.** A sloppy prompt that reads 15 files eats 10x more context than a precise prompt with `@` references pointing to 2 files.

    **Three tools:**

    1. **`@` references**, focus Claude on specific files:
        ```
        Add validation to @src/routes/quizzes.py using @src/schemas/quiz.py
        ```
    2. **`/context`**, shows token usage breakdown
    3. **`/compact`**, compresses conversation history to reclaim space

    **Gotcha.** `/compact` summarizes, it does not delete. Use `/rewind` to revisit specific earlier decisions.

    Further reading: [Common workflows docs](https://docs.anthropic.com/en/docs/claude-code/common-workflows)

---

### Hands-on

#### Part 1: Without `@` References

1. Fresh session. Ask:
    ```
    Add input validation to POST /quizzes, the title must be at least 3 characters
    and the topic must be non-empty.
    ```
2. Watch which files Claude reads.
3. Run `/context` and note the token usage.

#### Part 2: With `@` References

1. Fresh session (`/clear` or restart).
2. Same task with references:
    ```
    Add input validation to @src/routes/quizzes.py, the title must be at least 3
    characters and the topic must be non-empty. The schema is in @src/schemas/quiz.py.
    ```
3. Run `/context`, compare. Should be noticeably smaller.

#### Part 3: `/compact` During a Long Task

1. Give a bigger task:
    ```
    Validate all endpoints: title >= 3 chars, topic non-empty on POST /quizzes;
    exactly 4 options and correct_index 0-3 on POST /quizzes/{id}/questions.
    Also write tests for the new validation and update docs/api.md with the
    validation rules.
    ```
2. Midway through, run `/compact`.
3. Tell Claude to continue. Verify it picks up where it left off.

!!! success "Checkpoint"
    - [x] Validation is in place
    - [x] You ran `/context` twice and observed the difference
    - [x] You used `/compact` and Claude continued successfully

---

[← Exercise 1](exercise-1.md) · [Wrap-up: theme, verify, recap →](wrap-up.md)
