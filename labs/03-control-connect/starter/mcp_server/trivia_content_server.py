"""Quiz Trivia MCP server.

Exposes zero-auth tools for Open Trivia DB:
  - list_categories() -> available OTDB categories with IDs
  - get_category_stats(category) -> OTDB question counts for one category
  - get_questions(amount, category, difficulty, question_type)
  - get_trivia(category, count) -> compatibility alias for lab instructions

No API keys required. Needs network access. If your venue has no internet,
run `python mcp_server/trivia_content_server_offline.py` instead (ships with
canned data).

Register it from your lab in `.claude/settings.json`:

  {
    "mcpServers": {
      "trivia-content": {
        "command": "python",
        "args": ["mcp_server/trivia_content_server.py"]
      }
    }
  }
"""
from __future__ import annotations

import html
from typing import Any

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("trivia-content")

OPENTDB_URL = "https://opentdb.com/api.php"
OPENTDB_CATEGORIES_URL = "https://opentdb.com/api_category.php"
OPENTDB_CATEGORY_COUNT_URL = "https://opentdb.com/api_count.php"
DEFAULT_HEADERS = {"User-Agent": "ClaudeCode-Labcamp/1.0 (educational MCP demo)"}


def _normalize_question(item: dict[str, Any], source_category: str | None) -> dict[str, Any]:
    options = [html.unescape(item["correct_answer"])] + [
        html.unescape(opt) for opt in item["incorrect_answers"]
    ]
    options_sorted = sorted(options)
    correct = html.unescape(item["correct_answer"])
    correct_index = options_sorted.index(correct)
    return {
        "text": html.unescape(item["question"]),
        "options": options_sorted,
        "correct_index": correct_index,
        "_source_category": source_category,
        "_difficulty": item.get("difficulty"),
        "_type": item.get("type"),
    }


def _fetch_categories() -> list[dict[str, Any]]:
    response = requests.get(OPENTDB_CATEGORIES_URL, headers=DEFAULT_HEADERS, timeout=10)
    response.raise_for_status()
    payload = response.json()
    return payload.get("trivia_categories", [])


def _resolve_category_id(category: str | None) -> int | None:
    if not category:
        return None
    raw = str(category).strip()
    if not raw:
        return None
    if raw.isdigit():
        return int(raw)

    categories = _fetch_categories()
    needle = raw.lower()
    for item in categories:
        name = str(item.get("name", "")).lower()
        if needle == name or needle in name:
            return int(item["id"])
    return None


@mcp.tool()
def list_categories() -> list[dict[str, Any]]:
    """List available Open Trivia DB categories and IDs."""
    return _fetch_categories()


@mcp.tool()
def get_category_stats(category: str) -> dict[str, Any]:
    """Get OTDB question-count stats for one category name or ID."""
    category_id = _resolve_category_id(category)
    if category_id is None:
        return {
            "category": category,
            "category_id": None,
            "found": False,
            "counts": None,
            "message": "category not found",
        }

    response = requests.get(
        OPENTDB_CATEGORY_COUNT_URL,
        params={"category": category_id},
        headers=DEFAULT_HEADERS,
        timeout=10,
    )
    response.raise_for_status()
    payload = response.json().get("category_question_count", {})
    return {
        "category": category,
        "category_id": category_id,
        "found": True,
        "counts": payload,
    }


@mcp.tool()
def get_questions(
    amount: int = 5,
    category: str | None = None,
    difficulty: str | None = None,
    question_type: str = "multiple",
) -> list[dict[str, Any]]:
    """Fetch trivia questions with optional category/difficulty/type filters."""
    count = max(1, min(int(amount), 20))
    params: dict[str, Any] = {"amount": count, "type": question_type}

    category_id = _resolve_category_id(category)
    if category_id is not None:
        params["category"] = category_id
    if difficulty in {"easy", "medium", "hard"}:
        params["difficulty"] = difficulty

    response = requests.get(OPENTDB_URL, params=params, headers=DEFAULT_HEADERS, timeout=10)
    response.raise_for_status()
    payload = response.json()
    results = payload.get("results", [])
    return [_normalize_question(item, category) for item in results]


@mcp.tool()
def get_trivia(category: str, count: int = 5) -> list[dict[str, Any]]:
    """Fetch real trivia questions from Open Trivia DB.

    Args:
        category: free-form topic hint (logged, but OTDB ignores unknown topics).
        count:    how many questions to return (1..20).

    Returns a list of question objects with the shape:
        { "text": str, "options": [str, str, str, str], "correct_index": int }
    """
    return get_questions(amount=count, category=category, question_type="multiple")


if __name__ == "__main__":
    mcp.run()
