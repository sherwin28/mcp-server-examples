"""Test client for any MCP server.

Run: python test_client.py path/to/server.py
"""

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test(server_script: str):
    async with stdio_client(StdioServerParameters(
        command="python", args=[server_script]
    )) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")

            # Call the first tool (if any)
            if tools.tools:
                tool = tools.tools[0]
                print(f"\nCalling: {tool.name}")
                # Generate sample args based on schema (simplified)
                sample_args = {}
                for prop, schema in tool.inputSchema.get("properties", {}).items():
                    if schema.get("type") == "string":
                        sample_args[prop] = "sample"
                    elif schema.get("type") == "integer":
                        sample_args[prop] = 5
                result = await session.call_tool(tool.name, sample_args)
                print(f"Result: {result.content[0].text[:500]}")


if __name__ == "__main__":
    server_path = sys.argv[1] if len(sys.argv) > 1 else "sql_server/server.py"
    asyncio.run(test(server_path))
