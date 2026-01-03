"""FastMCP glue that exposes the Jina reader fetcher as an MCP tool."""

from __future__ import annotations

from typing import Final

from fastmcp import FastMCP
from fastmcp.server import Context

from .reader import gather_and_index_cache_files
from .search import search_index

SERVER_NAME: Final[str] = "Minsearch FastMCP"
INSTRUCTIONS: Final[str] = (
    "Use the minsearch index markdown files in git repositories."
)


def build_server() -> FastMCP:
    """Create the FastMCP server and register the fetch tool."""

    import argparse

    parser = argparse.ArgumentParser(description="Index and search markdown files.")
    parser.add_argument("--cache", type=str, help="Path to the dir with JSON cache files.")

    args = parser.parse_args()
    indices = gather_and_index_cache_files(data_dir=args.cache)

    server = FastMCP(name=SERVER_NAME, instructions=INSTRUCTIONS)

    @server.tool(
        title="Query fastmcp-main repo through minsearch",
        description="Fetch the most relevant markdown files by query",
    )
    def query(query: str, top_k: int, ctx: Context) -> list[str]:
        ctx.info("Requesting '%s' via the Minsearch index" % query)
        return search_index(query, indices["fastmcp-main"], top_k=top_k)

    return server


def main() -> None:
    """Entrypoint that runs the FastMCP server over stdio."""

    server = build_server()
    server.run()
