from __future__ import annotations

from typing import Any, Dict

from src.utils.logging_config import get_logger

from .search import duckduckgo_search, fetch_url
from ..wikipedia.wikipedia_api import wiki_search, wiki_summary
from ..arxiv.arxiv_api import arxiv_fetch, arxiv_search

logger = get_logger(__name__)


class WebSearchToolsManager:
    def __init__(self):
        self._initialized = False

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        try:
            # web.search
            query_props = PropertyList(
                [
                    Property("query", PropertyType.STRING),
                    Property(
                        "max_results",
                        PropertyType.INTEGER,
                        default_value=5,
                        min_value=1,
                        max_value=10,
                    ),
                ]
            )

            def search_wrapper(args: Dict[str, Any]) -> str:
                q = args.get("query", "")
                n = args.get("max_results", 5)
                out = duckduckgo_search(q, n)
                if out.get("status") != "success":
                    return out.get("message", "search failed")

                results = out.get("results", [])
                if not results:
                    return "Khong tim thay ket qua web phu hop."

                lines = [f"Ket qua web cho: {out.get('query')}"]
                for i, r in enumerate(results, 1):
                    title = r.get("title", "")
                    url = r.get("url", "")
                    snip = r.get("snippet", "")
                    block = f"{i}) {title}\n{url}"
                    if snip:
                        block += f"\n   {snip}"
                    lines.append(block)
                return "\n".join(lines)

            add_tool(
                (
                    "web.search",
                    "Tim kiem web (DuckDuckGo). Tra ve link + snippet.",
                    query_props,
                    search_wrapper,
                )
            )

            # web.fetch
            fetch_props = PropertyList(
                [
                    Property("url", PropertyType.STRING),
                    Property(
                        "max_chars",
                        PropertyType.INTEGER,
                        default_value=8000,
                        min_value=500,
                        max_value=50000,
                    ),
                ]
            )

            def fetch_wrapper(args: Dict[str, Any]) -> str:
                u = args.get("url", "")
                m = args.get("max_chars", 8000)
                out = fetch_url(u, m)
                if out.get("status") != "success":
                    return out.get("message", "fetch failed")
                return f"URL: {out.get('url')}\n\n{out.get('text', '')}"

            add_tool(
                (
                    "web.fetch",
                    "Tai noi dung 1 trang web va trich text.",
                    fetch_props,
                    fetch_wrapper,
                )
            )

            # wikipedia.search
            wiki_search_props = PropertyList(
                [
                    Property("query", PropertyType.STRING),
                    Property("lang", PropertyType.STRING, default_value="vi"),
                    Property(
                        "max_results",
                        PropertyType.INTEGER,
                        default_value=5,
                        min_value=1,
                        max_value=10,
                    ),
                ]
            )

            async def wiki_search_wrapper(args: Dict[str, Any]) -> str:
                q = (args.get("query") or "").strip()
                lang = (args.get("lang") or "vi").strip() or "vi"
                n = int(args.get("max_results") or 5)
                out = await wiki_search(q, lang=lang, max_results=n)
                if out.get("status") != "success":
                    return out.get("message", "wikipedia.search failed")
                results = out.get("results", [])
                if not results:
                    return "Khong tim thay ket qua phu hop tren Wikipedia."
                lines = [f"Wikipedia ({lang}) ket qua cho: {q}"]
                for i, r in enumerate(results, 1):
                    title = r.get("title", "")
                    url = r.get("url", "")
                    snip = r.get("snippet", "")
                    block = f"{i}) {title}\n{url}"
                    if snip:
                        block += f"\n   {snip}"
                    lines.append(block)
                return "\n".join(lines)

            add_tool(
                (
                    "wikipedia.search",
                    "Search Wikipedia (vi/en).",
                    wiki_search_props,
                    wiki_search_wrapper,
                )
            )

            # wikipedia.summary
            wiki_summary_props = PropertyList(
                [
                    Property("title", PropertyType.STRING),
                    Property("lang", PropertyType.STRING, default_value="vi"),
                    Property(
                        "max_chars",
                        PropertyType.INTEGER,
                        default_value=4000,
                        min_value=500,
                        max_value=20000,
                    ),
                ]
            )

            async def wiki_summary_wrapper(args: Dict[str, Any]) -> str:
                title = (args.get("title") or "").strip()
                lang = (args.get("lang") or "vi").strip() or "vi"
                max_chars = int(args.get("max_chars") or 4000)
                out = await wiki_summary(title, lang=lang, max_chars=max_chars)
                if out.get("status") != "success":
                    return out.get("message", "wikipedia.summary failed")
                url = out.get("url", "")
                text = out.get("text", "")
                if url:
                    return f"{title}\n{url}\n\n{text}"
                return f"{title}\n\n{text}"

            add_tool(
                (
                    "wikipedia.summary",
                    "Fetch Wikipedia page summary (vi/en).",
                    wiki_summary_props,
                    wiki_summary_wrapper,
                )
            )

            # arxiv.search
            arxiv_search_props = PropertyList(
                [
                    Property("query", PropertyType.STRING),
                    Property(
                        "max_results",
                        PropertyType.INTEGER,
                        default_value=5,
                        min_value=1,
                        max_value=10,
                    ),
                ]
            )

            async def arxiv_search_wrapper(args: Dict[str, Any]) -> str:
                q = (args.get("query") or "").strip()
                n = int(args.get("max_results") or 5)
                out = await arxiv_search(q, max_results=n)
                if out.get("status") != "success":
                    return out.get("message", "arxiv.search failed")
                results = out.get("results", [])
                if not results:
                    return "Khong tim thay ket qua arXiv phu hop."
                lines = [f"arXiv ket qua cho: {q}"]
                for i, r in enumerate(results, 1):
                    title = r.get("title", "")
                    url = r.get("url", "")
                    authors = ", ".join((r.get("authors") or [])[:6])
                    published = r.get("published", "")
                    summary = (r.get("summary", "") or "").strip()
                    if len(summary) > 500:
                        summary = summary[:500].rstrip() + "..."
                    block = f"{i}) {title}\n{url}"
                    if authors:
                        block += f"\n   Authors: {authors}"
                    if published:
                        block += f"\n   Published: {published}"
                    if summary:
                        block += f"\n   {summary}"
                    lines.append(block)
                return "\n".join(lines)

            add_tool(
                (
                    "arxiv.search",
                    "Search arXiv papers (Atom API).",
                    arxiv_search_props,
                    arxiv_search_wrapper,
                )
            )

            # arxiv.fetch
            arxiv_fetch_props = PropertyList([Property("id_or_url", PropertyType.STRING)])

            async def arxiv_fetch_wrapper(args: Dict[str, Any]) -> str:
                raw = (args.get("id_or_url") or "").strip()
                out = await arxiv_fetch(raw)
                if out.get("status") != "success":
                    return out.get("message", "arxiv.fetch failed")
                r = out.get("result", {}) or {}
                title = r.get("title", "")
                url = r.get("url", "")
                authors = ", ".join((r.get("authors") or [])[:10])
                published = r.get("published", "")
                summary = (r.get("summary", "") or "").strip()
                if len(summary) > 4000:
                    summary = summary[:4000].rstrip() + "..."
                lines = [title]
                if url:
                    lines.append(url)
                if authors:
                    lines.append(f"Authors: {authors}")
                if published:
                    lines.append(f"Published: {published}")
                if summary:
                    lines.append("")
                    lines.append(summary)
                return "\n".join(lines)

            add_tool(
                (
                    "arxiv.fetch",
                    "Fetch a single arXiv paper by id or URL.",
                    arxiv_fetch_props,
                    arxiv_fetch_wrapper,
                )
            )

            self._initialized = True
            logger.info("[WebSearch] tools registered")
        except Exception as e:
            logger.error(f"[WebSearch] init_tools failed: {e}", exc_info=True)
            raise


_manager = None


def get_web_search_manager():
    global _manager
    if _manager is None:
        _manager = WebSearchToolsManager()
    return _manager

