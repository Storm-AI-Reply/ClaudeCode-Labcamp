# Exercise 2: MCP: Trivia + Images Servers

> Connect Claude to two MCP servers: one for trivia questions and one for Wikipedia images.

**Lab:** [Lab 03 overview](index.md)

??? info "Theory: MCP (Model Context Protocol)"

    **What it is.** An open standard for connecting AI tools to external data sources. Your starter includes two MCP servers: `trivia-content` and `wiki-images`.

    **Configuration** in `.claude/settings.json`:

    ```json
    {
      "mcpServers": {
        "trivia-content": {
          "command": "python",
          "args": ["mcp_server/trivia_content_server.py"]
        },
        "wiki-images": {
          "command": "python",
          "args": ["mcp_server/wiki_images_server.py"]
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
    Use the sample prompts below as a baseline, then adapt topic, constraints, and voice to your group's concept so your quiz content does not look like everyone else's.

#### Part 1: Register the MCP Servers

1. Add to `.claude/settings.json`:
    ```json
    {
      "mcpServers": {
        "trivia-content": {
          "command": "python",
          "args": ["mcp_server/trivia_content_server.py"]
        },
        "wiki-images": {
          "command": "python",
          "args": ["mcp_server/wiki_images_server.py"]
        }
      }
    }
    ```
2. Restart Claude.
3. Run `/mcp`, you should see trivia tools (`get_trivia`, `get_questions`, `list_categories`) and image tool (`get_topic_image`).

!!! tip "Rotate the driver"
    Hand the keyboard to the next person.

#### Part 2: Fetch Real Trivia

4. Ask:
    ```
    Use the `trivia-content` MCP (`get_questions`) to fetch 10 multiple-choice
    questions for our theme and insert them into quiz 1 using the local API.
    ```
5. No quiz yet? First: `Create a quiz called "<theme>" with topic "<topic>" using POST /quizzes`.

#### Part 3: Add Images

The API persists an optional **`image_url`** on each question (`src/schemas/quiz.py`). Claude can set it when calling `POST /quizzes/{id}/questions` so the URL is stored with the question, not only in chat.

6. Ask:
    ```
    For each question in quiz 1, use the `wiki-images` MCP (`get_topic_image`)
    to fetch a matching background image and store `image_url` on that
    question record.
    ```

#### Part 4: Reflect

7. Ask Claude to list every MCP tool call it made in this session.

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
