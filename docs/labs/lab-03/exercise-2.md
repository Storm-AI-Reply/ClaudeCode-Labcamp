# Exercise 2: MCP: Quiz Content Server

> Connect Claude to an MCP server that fetches real trivia questions and Wikipedia images.

**Lab:** [Lab 03 overview](index.md)

??? info "Theory: MCP (Model Context Protocol)"

    **What it is.** An open standard for connecting AI tools to external data sources. Your starter includes a Quiz Content MCP server with two tools: `get_trivia` and `get_topic_image`.

    **Configuration** in `.claude/settings.json`:

    ```json
    {
      "mcpServers": {
        "quiz-content": {
          "command": "python",
          "args": ["mcp_server/server.py"]
        }
      }
    }
    ```

    **Gotcha.** No internet? Use `mcp_server/server_offline.py`, same interface, canned data.

    **Key commands:** `/mcp` (list tools), `claude mcp add <name> --command <cmd>`

    Further reading: [Connect Claude Code to tools via MCP](https://docs.anthropic.com/en/docs/claude-code/mcp)

---

### Hands-on

#### Part 1: Register the MCP Server

1. Add to `.claude/settings.json`:
    ```json
    {
      "mcpServers": {
        "quiz-content": {
          "command": "python",
          "args": ["mcp_server/server.py"]
        }
      }
    }
    ```
2. Restart Claude.
3. Run `/mcp`, you should see `get_trivia` and `get_topic_image`.

!!! tip "Rotate the driver"
    Hand the keyboard to the next person.

#### Part 2: Fetch Real Trivia

4. Ask:
    ```
    Use the quiz-content MCP to fetch 10 trivia questions matching our theme.
    Insert them into quiz 1 using the local API.
    ```
5. No quiz yet? First: `Create a quiz called "<theme>" with topic "<topic>" using POST /quizzes`.

#### Part 3: Add Images

The API persists an optional **`image_url`** on each question (`src/schemas/quiz.py`). Claude can set it when calling `POST /quizzes/{id}/questions` so the URL is stored with the question, not only in chat.

6. Ask:
    ```
    For each question in quiz 1, fetch a matching background image using
    get_topic_image and store the URL on the question record.
    ```

#### Part 4: Reflect

7. Ask Claude to list every MCP tool call it made in this session.

!!! note "No internet?"
    Change `"args"` to `["mcp_server/server_offline.py"]`, same tools, canned data.

!!! success "Checkpoint"
    - [x] `/mcp` shows both tools
    - [x] Quiz 1 has real trivia fetched via MCP
    - [x] Questions have image URLs
    - [x] Both MCP tools were called at least once

---

[← Exercise 1](exercise-1.md) · [Wrap-up →](wrap-up.md)
