# Exercise 1: The Agentic Loop & Plan Mode

> The quiz-night API has 5 intentional bugs. You will fix them three different ways to see how Claude's execution model works.

**Lab:** [Lab 01 overview](index.md)

??? info "Theory: The Agentic Loop"

    **What it is.** Claude Code is an *agentic* coding assistant. When you give it a task, it does not produce a single answer; it enters a loop: read the prompt, decide which tool to use (read a file, run a command, edit code), observe the result, then decide the next step. This loop repeats until the task is complete or Claude decides it needs your input.

    **Why it matters.** Understanding this loop is essential because it determines how Claude spends your context window. A vague task may cause Claude to read dozens of files; a precise task lets it go straight to work.

    **How it works.** When you press Enter, Claude Code:

    1. Analyzes your request and the current context
    2. Chooses a **tool** (Read, Write/Edit, Bash, Grep/Glob, etc.)
    3. Executes the tool and reads the **observation**
    4. Decides the next step: another tool call, or a response to you

    **Key actions:**

    - **Esc**: interrupt Claude mid-step
    - **Esc Esc** or **/rewind**: undo the last step
    - **Shift+Tab**: cycle through permission modes

    Further reading: [Quickstart docs](https://docs.anthropic.com/en/docs/claude-code/quickstart)

??? info "Theory: Plan Mode"

    **What it is.** A permission mode where Claude reads your code and writes a plan, but makes **no edits** and runs **no side-effecting commands**. You review, ask for changes, then approve.

    **Why it matters.** The worst failure mode is not "it did nothing," it is "it did the wrong thing for 20 minutes before you noticed." Plan Mode is your preflight check.

    **How to enter:**

    === "Inside a session"
        Press `Shift+Tab` until the status line shows the plan mode indicator.

    === "From the CLI"
        ```bash
        claude --permission-mode plan
        ```

    You can also set it as default:

    ```json
    { "permissions": { "defaultMode": "plan" } }
    ```

    **Gotcha.** Plan Mode does not prevent Claude from *reading* sensitive files, only from modifying them.

    Further reading: [Permission modes docs](https://docs.anthropic.com/en/docs/claude-code/permission-modes)

---

### Hands-on

#### Part 1: Default Mode (watch the loop)

1. Start Claude Code:
    ```bash
    claude
    ```
2. Give Claude the task:
    ```
    This API has bugs. Fix them so pytest passes.
    ```
3. Watch Claude work. Notice each tool call, it reads files, runs `pytest`, edits code, and re-runs `pytest`.
4. When pytest passes, note how many tool calls it took.

#### Part 2: Plan Mode (think before doing)

1. Reset: `git checkout -- .`
2. Enter Plan Mode via `Shift+Tab` or:
    ```bash
    claude --permission-mode plan
    ```
3. Same task: `This API has bugs. Fix them so pytest passes.`
4. Read the plan.
5. Modify it, e.g., *"Start with the route handler bug instead."*
6. Switch back to default mode (`Shift+Tab`) and tell Claude to execute.

#### Part 3: Interrupt & Rewind (your safety net)

1. Reset: `git checkout -- .`
2. Default mode, same task.
3. After 1–2 tool calls, press `Esc` to interrupt.
4. Add: *"Also add a docstring to every function you touch."*
5. Let Claude continue. Try `/rewind` to undo the last step.
6. Let Claude finish.

!!! success "Checkpoint"
    - [x] `pytest` passes (all 6 tests green)
    - [x] You cycled through permission modes with `Shift+Tab`
    - [x] You modified a plan in Plan Mode
    - [x] You interrupted with `Esc` and used `/rewind`

---

[← Lab 01 overview](index.md) · [Exercise 2: Context management →](exercise-2.md)
