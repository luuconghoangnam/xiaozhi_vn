from __future__ import annotations

import re
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup

from src.utils.logging_config import get_logger

logger = get_logger(__name__)


def _clean_text(s: str) -> str:
    s = re.sub(r"\s+", " ", (s or "").strip())
    return s


def duckduckgo_search(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Lightweight web search via DuckDuckGo HTML (no API key).

    Returns: {status, query, results:[{title,url,snippet}]}
    """
    q = (query or "").strip()
    if not q:
        return {"status": "error", "message": "Missing query", "results": []}

    try:
        max_results = int(max_results or 5)
    except Exception:
        max_results = 5
    max_results = max(1, min(max_results, 10))

    url = "https://duckduckgo.com/html/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml",
    }

    try:
        resp = requests.get(url, params={"q": q}, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        logger.warning(f"duckduckgo_search request failed: {e}")
        return {"status": "error", "message": f"web search failed: {e}", "results": []}

    soup = BeautifulSoup(resp.text, "html.parser")

    results: List[Dict[str, str]] = []
    for res in soup.select("div.result"):
        a = res.select_one("a.result__a")
        if not a:
            continue
        title = _clean_text(a.get_text() or "")
        href = (a.get("href") or "").strip()
        if not href:
            continue
        sn = res.select_one("a.result__snippet, div.result__snippet")
        snippet = _clean_text(sn.get_text() if sn else "")
        results.append({"title": title, "url": href, "snippet": snippet})
        if len(results) >= max_results:
            break

    return {"status": "success", "query": q, "results": results}


def fetch_url(url: str, max_chars: int = 8000) -> Dict[str, Any]:
    """Fetch a URL and extract readable text (very lightweight)."""
    u = (url or "").strip()
    if not u:
        return {"status": "error", "message": "Missing url"}

    try:
        max_chars = int(max_chars or 8000)
    except Exception:
        max_chars = 8000
    max_chars = max(500, min(max_chars, 50000))

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    try:
        resp = requests.get(u, headers=headers, timeout=20)
        resp.raise_for_status()
    except Exception as e:
        return {"status": "error", "message": f"fetch failed: {e}"}

    ct = (resp.headers.get("content-type") or "").lower()
    if "text/html" in ct:
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = soup.get_text(" ")
    else:
        text = resp.text

    text = _clean_text(text)
    if len(text) > max_chars:
        text = text[:max_chars] + "…"

    return {"status": "success", "url": u, "text": text}
