"""FastMCP glue that exposes the Jina reader fetcher as an MCP tool."""

from __future__ import annotations

from typing import Final

from fastmcp import FastMCP
from fastmcp.server import Context

from .reader import fetch_markdown

SERVER_NAME: Final[str] = "Jina Reader FastMCP"
INSTRUCTIONS: Final[str] = (
    "Use the Jina reader to fetch any public web page as markdown via an MCP tool."
)


def build_server() -> FastMCP:
    """Create the FastMCP server and register the fetch tool."""

    server = FastMCP(name=SERVER_NAME, instructions=INSTRUCTIONS)

    @server.tool(
        title="Read a page through Jina",
        description="Fetch the markdown view of any URL routed through https://r.jina.ai/",
    )
    def read_page(url: str, ctx: Context) -> str:
        ctx.info("Requesting %s via the Jina reader" % url)
        return fetch_markdown(url)

    return server


def main() -> None:
    """Entrypoint that runs the FastMCP server over stdio."""

    server = build_server()
    server.run()
