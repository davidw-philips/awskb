#!/usr/bin/env python3
"""
awskb: CLI tool to interact with the AWS Knowledge MCP Server.

Provides dynamic, token-efficient discovery and execution of AWS Knowledge
MCP tools directly from the remote endpoint (https://knowledge-mcp.global.api.aws).
Runs on Windows, macOS, and Linux using only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

MCP_ENDPOINT = os.environ.get("AWSKB_ENDPOINT", "https://knowledge-mcp.global.api.aws")
USER_AGENT = "awskb-cli/0.1.0"


def send_mcp_request(method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Send a JSON-RPC 2.0 request to the remote MCP HTTP server."""
    payload: Dict[str, Any] = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
    }
    if params is not None:
        payload["params"] = params

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        MCP_ENDPOINT,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": USER_AGENT,
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            resp_body = response.read().decode("utf-8")
            return json.loads(resp_body)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"Error: HTTP {e.code} from MCP endpoint: {err_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error connecting to MCP endpoint ({MCP_ENDPOINT}): {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error communicating with MCP endpoint: {e}", file=sys.stderr)
        sys.exit(1)


def list_tools() -> List[Dict[str, Any]]:
    """Fetch the list of tools available on the MCP endpoint."""
    res = send_mcp_request("tools/list")
    if "error" in res:
        print(f"MCP error: {res['error']}", file=sys.stderr)
        sys.exit(1)
    return res.get("result", {}).get("tools", [])


def match_tool(name: str, tools: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Match tool name either exactly or stripped of the 'aws___' prefix."""
    target = name.strip().lower()
    for tool in tools:
        t_name = tool.get("name", "").lower()
        short_name = t_name.replace("aws___", "")
        if target == t_name or target == short_name:
            return tool
    return None


def show_help(tools: List[Dict[str, Any]]) -> None:
    """Print the CLI help including dynamically fetched tools from the MCP server."""
    print("usage: awskb [-h] [--help] [--tool TOOL_NAME description] [call TOOL_NAME [ARGS_JSON]]\n")
    print("AWS Knowledge Base CLI - Dynamically query AWS documentation, SDKs, regions, and skills.\n")
    print("Flags / Commands:")
    print("  --help, -h                  Show this help menu and list available tools from the MCP endpoint")
    print("  --tool <name> description   Print description, schema, and usage guidance for a specific tool")
    print("  call <tool_name> [args]     Call an MCP tool with JSON arguments (e.g. '{\"search_phrase\": \"...\"}')\n")
    print("Available Tools from MCP Endpoint (https://knowledge-mcp.global.api.aws):")

    for tool in tools:
        t_name = tool.get("name", "")
        short_name = t_name.replace("aws___", "")
        desc = tool.get("description", "").split("\n")[0].strip()
        print(f"  • {short_name:<28} ({t_name})")
        if desc:
            print(f"    {desc}")
    print("\nRun 'awskb --tool <tool_name> description' to view full parameter documentation.")


def show_tool_description(tool_name: str, tools: List[Dict[str, Any]]) -> None:
    """Print the detailed description and schema for a given tool."""
    tool = match_tool(tool_name, tools)
    if not tool:
        print(f"Error: Tool '{tool_name}' not found on MCP endpoint.", file=sys.stderr)
        print("Available tools:", file=sys.stderr)
        for t in tools:
            print(f"  - {t.get('name')}", file=sys.stderr)
        sys.exit(1)

    print(f"Tool: {tool.get('name')}")
    print("=" * 60)
    print(f"\nDescription:\n{tool.get('description', 'No description available.')}\n")
    print("-" * 60)
    print("Input Schema:")
    print(json.dumps(tool.get("inputSchema", {}), indent=2))
    print("=" * 60)


def call_tool(tool_name: str, args_str: Optional[str], tools: List[Dict[str, Any]]) -> None:
    """Execute a tool call against the MCP endpoint and format output."""
    tool = match_tool(tool_name, tools)
    actual_name = tool.get("name") if tool else tool_name

    arguments: Dict[str, Any] = {}
    if args_str:
        try:
            arguments = json.loads(args_str)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON arguments: {e}", file=sys.stderr)
            sys.exit(1)

    res = send_mcp_request("tools/call", {"name": actual_name, "arguments": arguments})
    if "error" in res:
        print(f"MCP Call Error: {json.dumps(res['error'], indent=2)}", file=sys.stderr)
        sys.exit(1)

    result_data = res.get("result", {})
    if result_data.get("isError"):
        print("Tool returned error status:", file=sys.stderr)

    content_list = result_data.get("content", [])
    if not content_list:
        print(json.dumps(result_data, indent=2))
        return

    for item in content_list:
        if item.get("type") == "text":
            text = item.get("text", "")
            try:
                # Try pretty-printing if inner content is JSON
                parsed = json.loads(text)
                print(json.dumps(parsed, indent=2))
            except Exception:
                print(text)
        else:
            print(json.dumps(item, indent=2))


def main() -> None:
    args = sys.argv[1:]

    # Handle --tool <tool_name> description (support description as sub-arg or standalone)
    if "--tool" in args:
        idx = args.index("--tool")
        if idx + 1 >= len(args):
            print("Error: --tool requires a tool name. e.g.: awskb --tool search_documentation description", file=sys.stderr)
            sys.exit(1)
        tool_name = args[idx + 1]
        tools = list_tools()
        show_tool_description(tool_name, tools)
        sys.exit(0)

    # Handle help or no arguments
    if not args or "-h" in args or "--help" in args:
        tools = list_tools()
        show_help(tools)
        sys.exit(0)

    # Handle 'call <tool_name> [json_args]'
    if args[0] == "call":
        if len(args) < 2:
            print("Error: 'call' requires a tool name. e.g.: awskb call list_regions", file=sys.stderr)
            sys.exit(1)
        tool_name = args[1]
        args_json = args[2] if len(args) > 2 else None
        tools = list_tools()
        call_tool(tool_name, args_json, tools)
        sys.exit(0)

    # Handle shorthand: awskb <tool_name> [json_args]
    tools = list_tools()
    matched = match_tool(args[0], tools)
    if matched:
        args_json = args[1] if len(args) > 1 else None
        call_tool(args[0], args_json, tools)
        sys.exit(0)

    print(f"Unknown command or option: {' '.join(args)}", file=sys.stderr)
    print("Run 'awskb --help' for usage instructions.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
