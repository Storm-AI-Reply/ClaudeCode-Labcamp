# Exercise 2: MCP: Trivia + Images Servers

> Connect Claude to two MCP servers: one for trivia questions and one for Wikipedia images.

**Lab:** [Lab 03 overview](index.md)

!!! note "Visual identity"
    The Lab 03 starter is a fresh codebase — the theme you built in Lab 02 is not present. Before the exercises below, ask Claude to re-apply your visual identity: *"Apply our visual identity from CLAUDE.md to @src/templates/play.html and @src/static/style.css."*

??? info "Theory: MCP (Model Context Protocol)"

    **What it is.** An open standard for connecting AI tools to external data sources. Your starter includes two MCP servers: `trivia-content` and `wiki-images`.

    **Configuration** in `.claude/settings.json`:

    ```json
    {
      "mcpServers": {
        "trivia-content": {
          "command": "uv",
          "args": ["run", "python", "mcp_server/trivia_content_server.py"]
        },
        "wiki-images": {
          "command": "uv",
          "args": ["run", "python", "mcp_server/wiki_images_server.py"]
        }
      }
    }
    ```

    **Gotcha.** No internet? Switch to `mcp_server/trivia_content_server_offline.py` (trivia) and `mcp_server/wiki_images_server_offline.py` (images), same tool names with canned data.

    **Key commands:** `/mcp` (list tools), `claude mcp add <name> --command <cmd>`

    Further reading: [Connect Claude Code to tools via MCP](https://docs.anthropic.com/en/docs/claude-code/mcp)

---

### Hands-on

!!! tip "Template prompts are scaffolding"
    Use the sample prompts below as a baseline, then adapt topic, constraints, and voice to your own concept so your quiz content does not look like everyone else's.

#### Part 1: Register the MCP Servers

1. Run `/exit` to close Claude, then run these two commands from the `starter/` directory:
    ```bash
    claude mcp add trivia-content -s project -- uv run python mcp_server/trivia_content_server.py
    claude mcp add wiki-images -s project -- uv run python mcp_server/wiki_images_server.py
    ```
    This saves the config to `.mcp.json` in the project root (project-scoped). Relaunch `claude`.
2. Run `/mcp`. You will see both server names (`trivia-content` and `wiki-images`). Click a server name to expand it and see its status and the list of tools it exposes, with name and description for each.

#### Part 2: Fetch Real Trivia

3. Ask:
    ```
    Use the `trivia-content` MCP (`get_questions`) to fetch 10 multiple-choice
    questions for your theme and insert them into quiz 1 using the local API.
    ```
4. No quiz yet? First: `Create a quiz called "<theme>" with topic "<topic>" using POST /quizzes`.

#### Part 3: Add Images

The API persists an optional **`image_url`** on each question (`src/schemas/quiz.py`). Claude can set it when calling `POST /quizzes/{id}/questions` so the URL is stored with the question, not only in chat.

5. Ask:
    ```
    For each question in quiz 1, use the `wiki-images` MCP (`get_topic_image`)
    to fetch a matching background image and store `image_url` on that
    question record.
    ```

!!! note "Missing endpoints?"
    Some API routes may be absent — for example, a route to update `image_url` on an existing question. If Claude encounters a 404 or method-not-allowed error, ask it to investigate and add the missing route. This is an intentional gap in the starter.

#### Part 4: Reflect

6. Ask Claude to list every MCP tool call it made in this session.

!!! note "No internet?"
    Use offline servers:
    - trivia: `"args": ["mcp_server/trivia_content_server_offline.py"]`
    - images: `"args": ["mcp_server/wiki_images_server_offline.py"]`

!!! success "Checkpoint"
    - [x] `/mcp` shows both servers
    - [x] Quiz 1 has real trivia fetched via MCP
    - [x] Questions have image URLs
    - [x] Both MCP tools were called at least once

---

[← Exercise 1](exercise-1.md) · [Wrap-up →](wrap-up.md)
