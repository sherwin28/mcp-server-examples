"""PDF MCP server - extract text and tables from PDFs."""

import asyncio
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Requires: pip install pypdf2 pdfplumber

server = Server("pdf-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="extract_text",
            description="Extract plain text from a PDF file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute path to PDF"},
                },
                "required": ["path"],
            },
        ),
        Tool(
            name="extract_tables",
            description="Extract tables from a PDF as CSV",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute path to PDF"},
                    "page": {"type": "integer", "description": "Page number (1-indexed)"},
                },
                "required": ["path"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "extract_text":
        return await _extract_text(arguments["path"])
    elif name == "extract_tables":
        return await _extract_tables(arguments["path"], arguments.get("page"))
    raise ValueError(f"Unknown tool: {name}")


async def _extract_text(path: str) -> list[TextContent]:
    import pypdf
    reader = pypdf.PdfReader(path)
    text = "\n".join([page.extract_text() for page in reader.pages])
    return [TextContent(type="text", text=text[:5000])]


async def _extract_tables(path: str, page: int = None) -> list[TextContent]:
    import pdfplumber
    tables = []
    with pdfplumber.open(path) as pdf:
        pages = [pdf.pages[page - 1]] if page else pdf.pages
        for p in pages:
            for table in p.extract_tables():
                tables.append("\n".join([",".join(row) for row in table]))
    return [TextContent(type="text", text="\n\n".join(tables))]


async def main():
    async with stdio_server() as (r, w):
        await server.run(r, w, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
