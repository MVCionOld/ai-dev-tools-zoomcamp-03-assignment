_README for the repository._

# ai-dev-tools-zoomcamp-03-assignment

## Jina reader FastMCP tool

This project exposes a FastMCP server that turns the Jina reader proxy (https://r.jina.ai) into an MCP tool. The tool simply forwards the requested public URL through the reader, so the client receives the markdown-rendered contents of the page while the MCP server tracks progress messages. Because r.jina.ai sits behind Cloudflare and prefers HTTP/2, the helper first talks over `httpx[http2]` with a browser-like header set and, if Cloudflare still returns a challenge, retries using `cfscrape` so that the MCP tool feels like a real browser.
It also respects the `CF_CLEARANCE` environment variable; when set, the helper injects that value as the `cf_clearance` cookie so you can bootstrap the challenge status from a browser session.

### Setup via uv

1. Install [uv](https://github.com/pypa/uv) if you have not already: `pip install uv`.
2. Run `uv install` from the repository root to provision dependencies (`fastmcp`, `httpx[http2]`, and `cfscrape`) exactly as pinned in `uv.lock`.
3. You can launch the FastMCP server with `python main.py` or `uv run main`; the server defaults to the stdio transport.

### Tool surface

- `read_page(url: str)` – uses the helper in `src/jina_reader_tool/reader.py` to make an HTTP GET against `https://r.jina.ai/<url>`, records progress with `Context.info()`, and returns the raw markdown text for the requested page.

### Testing

`python test.py` fetches `https://github.com/alexeygrigorev/minsearch` via the Jina reader bundle, asserts the response is non-empty, and prints the character count. If the Jina reader request is blocked (Cloudflare 403), the helper raises `JinaReaderError` and the test fails before printing a count.
