"""Offline fallback for Quiz Images MCP.

Use this when the labcamp venue has no internet. Exposes `get_topic_image`
with canned URLs and a placeholder fallback.
"""
from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("wiki-images-offline")

_IMAGES: dict[str, str] = {
    "super mario": "https://upload.wikimedia.org/super-mario.png",
    "sistine chapel": "https://upload.wikimedia.org/sistine.png",
    "canberra": "https://upload.wikimedia.org/canberra.png",
    "http": "https://upload.wikimedia.org/http.png",
}


@mcp.tool()
def get_topic_image(topic: str) -> dict[str, Any]:
    """Return a canned image URL if available, otherwise a placeholder."""
    key = topic.lower().strip()
    for name, url in _IMAGES.items():
        if name in key:
            return {
                "topic": topic,
                "title": name.title(),
                "image_url": url,
                "page_url": None,
            }
    return {
        "topic": topic,
        "title": topic.title(),
        "image_url": "https://placehold.co/1200x630?text=" + topic.replace(" ", "+"),
        "page_url": None,
    }


if __name__ == "__main__":
    mcp.run()
