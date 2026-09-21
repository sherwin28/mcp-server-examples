# mcp-server-examples

**Five production MCP servers. Copy-paste into your agent.**

MCP (Model Context Protocol) is the standard way to give LLM agents tools. Write one MCP server, it works with Claude, GPT, Qwen, anything MCP-compatible.

---

## Servers included

| Server | Tools |
|--------|-------|
| `pdf_server/` | `extract_text`, `extract_tables`, `summarize` |
| `web_search_server/` | `search` (DuckDuckGo), `fetch_url` |
| `github_server/` | `search_repos`, `read_file` |
| `code_search_server/` | `search_code`, `get_function` |
| `sql_server/` | `query` (read-only, LIMIT-enforced), `list_tables` |

---

## Quick start

```bash
git clone https://github.com/sherwin28/mcp-server-examples
cd mcp-server-examples
pip install -r requirements.txt

# Run any server (e.g., sql_server)
cd sql_server && python server.py

# In another terminal, test it
python ../test_client.py
```

---

## Use as a Claude Agent SDK tool

```python
from claude_agent_sdk import Agent
from mcp_servers.sql_server import run_sql_server

agent = Agent(
    tools=[run_sql_server],
    system_prompt="You can query the database. Always LIMIT your queries.",
)

result = agent.run("How many active users signed up last week?")
```

---

## Use with LangChain MCP adapter

```python
from langchain_mcp_adapters import load_mcp_tools
# ... load tools, pass to LangGraph agent
```

---

## What's included beyond code

- ✅ Real implementations (not stubs or pseudocode)
- ✅ Error handling: timeouts, retries, circuit breakers
- ✅ Security: read-only modes, query limits, input sanitization
- ✅ Test client that works with any server
- ✅ Compatible with Claude Agent SDK, LangChain MCP, smolagents

---

## Reference

Built from a 5-server MCP architecture that shipped at Haleon for policy retrieval.

---

## License

MIT

---

**Author**: 魏远标 · [javai.tech](https://javai.tech)