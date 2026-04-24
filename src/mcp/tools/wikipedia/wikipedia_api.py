from __future__ import annotations

import asyncio
import html
import re
from typing import Any, Dict, List

import requests


def _strip_html(text: str) -> str:
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    return " ".join(text.split())


async def wiki_search(query: str, lang: str = "vi", max_results: int = 5) -> Dict[str, Any]:
    query = (query or "").strip()
    if not query:
        return {"status": "error", "message": "Thieu query"}

    base = f"https://{lang}.wikipedia.org"
    url = base + "/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "utf8": 1,
        "format": "json",
        "srlimit": max(1, min(int(max_results), 10)),
    }

    def _req():
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        return r.json()

    try:
        data = await asyncio.to_thread(_req)
        items = (((data or {}).get("query") or {}).get("search") or [])[: max_results]
        results: List[Dict[str, str]] = []
        for it in items:
            title = it.get("title", "")
            snippet = _strip_html(it.get("snippet", ""))
            page_url = base + "/wiki/" + requests.utils.quote(title.replace(" ", "_"))
            results.append({"title": title, "url": page_url, "snippet": snippet})
        return {"status": "success", "query": query, "results": results}
    except Exception as e:
        return {"status": "error", "message": f"Wikipedia search error: {e}"}


async def wiki_summary(title: str, lang: str = "vi", max_chars: int = 4000) -> Dict[str, Any]:
    title = (title or "").strip()
    if not title:
        return {"status": "error", "message": "Thieu title"}

    base = f"https://{lang}.wikipedia.org"
    # REST summary endpoint expects a URL-encoded title.
    endpoint = base + "/api/rest_v1/page/summary/" + requests.utils.quote(title)

    def _req():
        r = requests.get(endpoint, timeout=15, headers={"accept": "application/json"})
        r.raise_for_status()
        return r.json()

    try:
        data = await asyncio.to_thread(_req)
        extract = (data or {}).get("extract") or ""
        extract = extract.strip()
        if max_chars and len(extract) > max_chars:
            extract = extract[: max_chars].rstrip() + "..."

        url = ""
        content_urls = (data or {}).get("content_urls") or {}
        desktop = content_urls.get("desktop") or {}
        url = desktop.get("page") or ""
        return {"status": "success", "title": title, "url": url, "text": extract}
    except Exception as e:
        return {"status": "error", "message": f"Wikipedia summary error: {e}"}

