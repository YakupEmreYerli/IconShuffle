"""Drive an MCP server on the demo phone with the MCP SDK's client, as an MCP client would.

    python packaging/mcp_smoke.py COMMAND [ARGS...]

For example ``dist/iconshuffle/iconshuffle mcp --demo`` (the frozen desktop app) or
``ios-homescreen mcp --demo``. It lists the tools, reads the home screen, plans an A-Z
sort, applies it and reads again. Exits 0 when every step worked.
"""

from __future__ import annotations

import asyncio
import sys

from mcp import Client
from mcp.client.stdio import StdioServerParameters

TOOLS = {
    "find_phone",
    "read_home_screen",
    "list_apps",
    "plan_layout",
    "sort_pages",
    "apply_layout",
    "list_backups",
    "plan_restore",
    "restore_backup",
}


async def smoke(command: list[str]) -> None:
    server = StdioServerParameters(command=command[0], args=command[1:])
    async with Client(server, read_timeout_seconds=60) as client:
        names = {tool.name for tool in (await client.list_tools()).tools}
        assert names >= TOOLS, f"missing tools: {sorted(TOOLS - names)}"
        print(f"tools: {', '.join(sorted(names))}")

        async def call(name: str, arguments: dict | None = None) -> dict:
            result = await client.call_tool(name, arguments or {})
            assert not result.is_error, f"{name}: {result.content}"
            return result.structured_content or {}

        found = await call("find_phone")
        assert found["found"], found
        assert found["demo"], found
        read = await call("read_home_screen")
        print(f"read: {read['summary']}")
        plan = await call("sort_pages")
        assert plan["plan_id"], plan
        print(f"plan: {plan['summary']}")
        refused = await client.call_tool("apply_layout", {"plan_id": plan["plan_id"]})
        assert refused.is_error, "apply_layout wrote without confirm"
        applied = await call("apply_layout", {"plan_id": plan["plan_id"], "confirm": True})
        assert applied["status"] == "applied", applied
        print(f"applied, backup {applied['backup']}")
        again = await call("sort_pages")
        assert again["unchanged"], again
    print("mcp smoke test: ok")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    asyncio.run(smoke(sys.argv[1:]))
