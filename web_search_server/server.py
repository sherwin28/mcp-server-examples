"""Web search MCP server with citations."""

import asyncio
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("web-search-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search",
            description="Search the web and return top results with URLs",
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
            name="fetch_url",
            description="Fetch a URL and return its content",
            inputSchema={
                "type": "object",
                "properties": {"url": {"type": "string"}},
                "required": ["url"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "search":
        return await _search(arguments["query"], arguments.get("limit", 5))
    elif name == "fetch_url":
        return await _fetch(arguments["url"])
    raise ValueError(f"Unknown tool: {name}")


async def _search(query: str, limit: int) -> list[TextContent]:
    """Search using DuckDuckGo HTML (no API key required)."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query},
            timeout=10,
        )
        # Parse results (simplified - production should use BeautifulSoup)
        results = [
            f"{i}. {url}\n   {snippet}"
            for i, (url, snippet) in enumerate(_parse_ddg(resp.text)[:limit], 1)
        ]
        return [TextContent(type="text", text="\n\n".join(results))]


async def _fetch(url: str) -> list[TextContent]:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(url, timeout=10)
        # Strip HTML tags (basic)
        import re
        text = re.sub(r"<[^>]+>", "", resp.text)
        return [TextContent(type="text", text=text[:5000])]


def _parse_ddg(html: str) -> list[tuple[str, str]]:
    """Parse DuckDuckGo HTML results. Production: use BeautifulSoup."""
    import re
    pattern = r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>([^<]+)</a>'
    return [(url, title) for url, title in re.findall(pattern, html)]


async def main():
    async with stdio_server() as (r, w):
        await server.run(r, w, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
