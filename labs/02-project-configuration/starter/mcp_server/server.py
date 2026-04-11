"""Quiz Content MCP server.

Exposes two zero-auth tools:
  - get_trivia(category, count) — real questions from Open Trivia DB (opentdb.com)
  - get_topic_image(topic)     — main image URL from the closest Wikipedia article

No API keys required. Needs network access. If your venue has no internet,
run `python mcp_server/server_offline.py` instead (ships with canned data).

Register it from your lab in `.claude/settings.json`:

  {
    "mcpServers": {
      "quiz-content": {
        "command": "python",
        "args": ["mcp_server/server.py"]
      }
    }
  }
"""
from __future__ import annotations

import html
from typing import Any

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("quiz-content")

OPENTDB_URL = "https://opentdb.com/api.php"
WIKI_SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
WIKI_SEARCH_URL = "https://en.wikipedia.org/w/api.php"


@mcp.tool()
def get_trivia(category: str, count: int = 5) -> list[dict[str, Any]]:
    """Fetch real trivia questions from Open Trivia DB.

    Args:
        category: free-form topic hint (logged, but OTDB ignores unknown topics).
        count:    how many questions to return (1..20).

    Returns a list of question objects with the shape:
        { "text": str, "options": [str, str, str, str], "correct_index": int }
    """
    count = max(1, min(int(count), 20))
    response = requests.get(
        OPENTDB_URL,
        params={"amount": count, "type": "multiple"},
        timeout=10,
    )
    response.raise_for_status()
    payload = response.json()
    questions: list[dict[str, Any]] = []
    for item in payload.get("results", []):
        options = [html.unescape(item["correct_answer"])] + [
            html.unescape(opt) for opt in item["incorrect_answers"]
        ]
        options_sorted = sorted(options)
        correct_index = options_sorted.index(html.unescape(item["correct_answer"]))
        questions.append(
            {
                "text": html.unescape(item["question"]),
                "options": options_sorted,
                "correct_index": correct_index,
                "_source_category": category,
            }
        )
    return questions


@mcp.tool()
def get_topic_image(topic: str) -> dict[str, Any]:
    """Return the main image URL for the closest-matching Wikipedia article.

    Returns: { "topic": str, "title": str, "image_url": str | None, "page_url": str }
    """
    search = requests.get(
        WIKI_SEARCH_URL,
        params={
            "action": "query",
            "list": "search",
            "srsearch": topic,
            "format": "json",
            "srlimit": 1,
        },
        timeout=10,
    ).json()

    hits = search.get("query", {}).get("search", [])
    if not hits:
        return {"topic": topic, "title": None, "image_url": None, "page_url": None}

    title = hits[0]["title"]
    summary = requests.get(
        WIKI_SUMMARY_URL.format(title=title.replace(" ", "_")),
        timeout=10,
    ).json()
    image_url = (summary.get("originalimage") or {}).get("source") or (
        summary.get("thumbnail") or {}
    ).get("source")
    page_url = (summary.get("content_urls", {}).get("desktop") or {}).get("page")
    return {
        "topic": topic,
        "title": title,
        "image_url": image_url,
        "page_url": page_url,
    }


if __name__ == "__main__":
    mcp.run()
