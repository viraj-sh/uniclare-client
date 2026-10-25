import argparse
import sys


def run() -> None:
    try:
        from uniclare_client.interfaces.mcp.server import main
    except ModuleNotFoundError as e:
        if e.name == "fastmcp":
            sys.exit(
                "Missing MCP deps. Install: uv tool install 'uniclare-client[mcp]'"
            )
        raise

    parser = argparse.ArgumentParser(prog="uniclare-mcp")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    main(host=args.host, port=args.port)
