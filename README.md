# MCP Server Examples

**Practical Model Context Protocol (MCP) server implementations**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)]()
[![MCP](https://img.shields.io/badge/MCP-2025--06--18-purple.svg)]()

---

## What this is

Five production-grade MCP server examples, each in its own directory, with working code and test clients. Use these as copy-paste starters for your own AI agents.

## Servers included

| Server | Purpose | Tools |
|--------|---------|-------|
| `pdf_server/` | Extract text + tables from PDFs | `extract_text`, `extract_tables`, `summarize` |
| `sql_server/` | Safe SQL queries (read-only) | `query`, `list_tables`, `describe_table` |
| `web_search_server/` | Web search with citations | `search`, `fetch_url` |
| `code_search_server/` | Codebase semantic search | `search_code`, `get_function`, `get_class` |
| `github_server/` | GitHub repo operations | `search_repos`, `read_file`, `list_issues` |

## Why MCP

MCP (Model Context Protocol) is the standard way to give LLM agents tools. Instead of writing tool-calling JSON for each provider, you write one MCP server and it works with Claude, GPT, Qwen, and any MCP-compatible client.

## Features

- ✅ **Real implementations** (not stubs)
- ✅ **Error handling** patterns (timeouts, retries, circuit breakers)
- ✅ **Security**: read-only modes, query limits, input sanitization
- ✅ **Test clients** included
- ✅ **Compatible** with Claude Agent SDK, LangChain MCP adapters

## Quick start

```bash
git clone https://github.com/sherwin28/mcp-server-examples.git
cd mcp-server-examples
pip install -r requirements.txt

# Run the SQL server (read-only)
cd sql_server
python server.py

# In another terminal, run test client
python ../test_client.py
```

## Use as a library

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async with stdio_client(StdioServerParameters(
    command="python", args=["sql_server/server.py"]
)) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        result = await session.call_tool("query", {"sql": "SELECT * FROM users LIMIT 10"})
        print(result.content)
```

## Tech Stack

- Python 3.11 / asyncio
- MCP SDK
- Claude Agent SDK
- SQLAlchemy async

## License

MIT

## Author

**魏远标** — AI Architect · [javai.tech](https://javai.tech)
