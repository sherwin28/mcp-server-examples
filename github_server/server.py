"""GitHub MCP server - read-only repo operations."""

import asyncio
import os
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import httpx

server = Server("github-server")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_repos",
            description="Search GitHub repositories",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 5},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="read_file",
            description="Read a file from a GitHub repo",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "path": {"type": "string"},
                },
                "required": ["owner", "repo", "path"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "search_repos":
        return await _search_repos(arguments["query"], arguments.get("limit", 5))
    elif name == "read_file":
        return await _read_file(arguments["owner"], arguments["repo"], arguments["path"])
    raise ValueError(f"Unknown tool: {name}")


def _headers():
    h = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        h["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return h


async def _search_repos(query: str, limit: int) -> list[TextContent]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://api.github.com/search/repositories",
            params={"q": query, "per_page": limit},
            headers=_headers(),
            timeout=10,
        )
        items = resp.json().get("items", [])
        text = "\n".join([
            f"- {i['full_name']} ⭐{i['stargazers_count']}\n  {i['description'] or '(no description)'}"
            for i in items
        ])
        return [TextContent(type="text", text=text)]


async def _read_file(owner: str, repo: str, path: str) -> list[TextContent]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",
            headers=_headers(),
            timeout=10,
        )
        if resp.status_code == 200:
            import base64
            data = resp.json()
            content = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
            return [TextContent(type="text", text=content[:5000])]
        return [TextContent(type="text", text=f"Error {resp.status_code}: {resp.text}")]


async def main():
    async with stdio_server() as (r, w):
        await server.run(r, w, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
