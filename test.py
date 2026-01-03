"""Simple test that exercises the Jina reader helper."""

from __future__ import annotations

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from jina_reader_tool.reader import fetch_markdown

TEST_URL = "https://github.com/alexeygrigorev/minsearch"


def test_fetch_minsearch() -> int:
    """Fetch the MinSearch README via Jina reader and report the character length."""

    content = fetch_markdown(TEST_URL)
    length = len(content)
    print("Fetched %d characters from %s" % (length, TEST_URL))
    assert length > 0, "Expected non-empty response"
    return length


if __name__ == "__main__":
    test_fetch_minsearch()
