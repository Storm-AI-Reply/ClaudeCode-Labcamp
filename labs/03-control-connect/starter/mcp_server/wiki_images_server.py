"""Quiz Images MCP server.

Exposes one zero-auth Wikipedia tool:
  - get_topic_image(topic) -> main image URL from the closest article

Register it from your lab in `.claude/settings.json`:

  {
    "mcpServers": {
      "wiki-images": {
        "command": "python",
        "args": ["mcp_server/wiki_images_server.py"]
      }
    }
  }
"""
from __future__ import annotations

from typing import Any

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("wiki-images")

WIKI_SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
WIKI_SEARCH_URL = "https://en.wikipedia.org/w/api.php"
DEFAULT_HEADERS = {"User-Agent": "ClaudeCode-Labcamp/1.0 (educational MCP demo)"}


@mcp.tool()
def get_topic_image(topic: str) -> dict[str, Any]:
    """Return the main image URL for the closest-matching Wikipedia article.

    Returns: { "topic": str, "title": str, "image_url": str | None, "page_url": str | None }
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
        headers=DEFAULT_HEADERS,
        timeout=10,
    ).json()

    hits = search.get("query", {}).get("search", [])
    if not hits:
        return {"topic": topic, "title": None, "image_url": None, "page_url": None}

    title = hits[0]["title"]
    summary = requests.get(
        WIKI_SUMMARY_URL.format(title=title.replace(" ", "_")),
        headers=DEFAULT_HEADERS,
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
