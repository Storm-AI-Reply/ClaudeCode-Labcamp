"""Offline fallback for the Quiz Trivia MCP.

Use this when the labcamp venue has no internet. Exposes trivia tools only
and returns canned data instead of calling external APIs.

Register it in `.claude/settings.json`:

  {
    "mcpServers": {
      "trivia-content": {
        "command": "python",
        "args": ["mcp_server/trivia_content_server_offline.py"]
      }
    }
  }
"""
from __future__ import annotations

import random
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("trivia-content-offline")

_CANNED: list[dict[str, Any]] = [
    {
        "text": "What year was the first Super Mario Bros. released?",
        "options": ["1983", "1985", "1987", "1990"],
        "correct_index": 1,
    },
    {
        "text": "Which console was released first?",
        "options": ["Sega Genesis", "SNES", "NES", "Neo Geo"],
        "correct_index": 2,
    },
    {
        "text": "Who painted the ceiling of the Sistine Chapel?",
        "options": ["Raphael", "Michelangelo", "Leonardo", "Donatello"],
        "correct_index": 1,
    },
    {
        "text": "What is the capital of Australia?",
        "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
        "correct_index": 2,
    },
    {
        "text": "What does HTTP stand for?",
        "options": [
            "HyperText Transfer Protocol",
            "High Transfer Text Protocol",
            "Hyper Transport Text Protocol",
            "HyperText Transport Protocol",
        ],
        "correct_index": 0,
    },
]

@mcp.tool()
def get_trivia(category: str, count: int = 5) -> list[dict[str, Any]]:
    """Return canned trivia questions."""
    count = max(1, min(int(count), len(_CANNED)))
    return random.sample(_CANNED, count)


if __name__ == "__main__":
    mcp.run()
