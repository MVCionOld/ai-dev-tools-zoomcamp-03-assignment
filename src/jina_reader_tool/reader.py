"""Helpers that call the Jina reader proxy via httpx and cfscrape."""

from __future__ import annotations

from os import environ
from typing import Final

import cfscrape
import httpx
from requests.exceptions import RequestException

JINA_READER_BASE: Final[str] = "https://r.jina.ai/"
DEFAULT_TIMEOUT: Final[int] = 30

CHROME_HEADERS: Final[dict[str, str]] = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "max-age=0",
    "Pragma": "no-cache",
    "Sec-CH-UA": '"Chromium";v="130", "Not A(Brand";v="24", "Google Chrome";v="130"',
    "Sec-CH-UA-Arch": "x86",
    "Sec-CH-UA-Bitness": "64",
    "Sec-CH-UA-Full-Version": "130.0.0.0",
    "Sec-CH-UA-Full-Version-List": '"Chromium";v="130.0.0.0", "Not A(Brand";v="24.0.0.0"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Model": "",
    "Sec-CH-UA-Platform": "macOS",
    "Sec-CH-UA-Platform-Version": "14.0.0",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "Origin": "https://r.jina.ai",
    "Referer": "https://r.jina.ai/",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
}


CLIENT = httpx.Client(http2=True, headers=CHROME_HEADERS)
SCRAPER = cfscrape.create_scraper()
SCRAPER.headers.update(CHROME_HEADERS)
CF_CLEARANCE_COOKIE: Final[str] = "cf_clearance"
CF_CLEARANCE_ENV: Final[str] = "CF_CLEARANCE"


def _apply_cf_clearance_cookie() -> None:
    cf_value = environ.get(CF_CLEARANCE_ENV)
    if not cf_value:
        return
    CLIENT.cookies.set(CF_CLEARANCE_COOKIE, cf_value, domain="r.jina.ai", path="/")
    CLIENT.cookies.set("cf_chl_rc_ni", "2", domain="r.jina.ai", path="/")
    SCRAPER.cookies.set(CF_CLEARANCE_COOKIE, cf_value, domain="r.jina.ai", path="/")
    SCRAPER.cookies.set("cf_chl_rc_ni", "2", domain="r.jina.ai", path="/")


class JinaReaderError(RuntimeError):
    """Indicates a failure while talking to the Jina reader."""


def _normalize_url(target: str) -> str:
    target = target.strip()
    if not target:
        raise ValueError("URL must not be empty")
    if not target.startswith("http://") and not target.startswith("https://"):
        raise ValueError("URL must start with http:// or https://")
    return target


def build_jina_reader_url(target: str) -> str:
    """Return the absolute URL that routes the target through Jina reader."""

    target = _normalize_url(target)
    return f"{JINA_READER_BASE}{target}"


def _fetch_with_httpx(url: str) -> str:
    _apply_cf_clearance_cookie()
    response = CLIENT.get(url, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    return response.text


def _fetch_with_cfscrape(url: str) -> str:
    _apply_cf_clearance_cookie()
    try:
        response = SCRAPER.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
    except RequestException as exc:
        raise JinaReaderError("Cloudflare refused the request via cfscrape") from exc
    return response.text


def fetch_markdown(target: str) -> str:
    """Fetch the markdown-rendered text for a target page via Jina reader."""

    url = build_jina_reader_url(target)
    try:
        return _fetch_with_httpx(url)
    except httpx.HTTPStatusError as exc:
        if exc.response is not None and exc.response.status_code == 403:
            return _fetch_with_cfscrape(url)
        raise JinaReaderError("Failed to fetch content from Jina reader") from exc
    except httpx.HTTPError as exc:
        raise JinaReaderError("Failed to fetch content from Jina reader") from exc
