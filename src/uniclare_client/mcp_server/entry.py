# src/uniclare_client/mcp_server/entry.py
import sys


def run():
    try:
        from uniclare_client.mcp_server.server import main
    except ModuleNotFoundError as e:
        if e.name == "fastmcp":
            sys.exit(
                "Missing MCP deps. Install: uv tool install 'uniclare-client[mcp]'"
            )
        raise
    main()
