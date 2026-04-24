from __future__ import annotations

from typing import Any, Dict

from src.utils.logging_config import get_logger

from .arxiv_api import arxiv_fetch, arxiv_search

logger = get_logger(__name__)


class ArxivToolsManager:
    def __init__(self):
        self._initialized = False

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        try:
            search_props = PropertyList(
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

            async def search_wrapper(args: Dict[str, Any]) -> str:
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
                    authors = ", ".join(r.get("authors", [])[:6])
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
                    "Search arXiv papers (Atom API). Returns title, url, authors, summary.",
                    search_props,
                    search_wrapper,
                )
            )

            fetch_props = PropertyList([Property("id_or_url", PropertyType.STRING)])

            async def fetch_wrapper(args: Dict[str, Any]) -> str:
                raw = (args.get("id_or_url") or "").strip()
                out = await arxiv_fetch(raw)
                if out.get("status") != "success":
                    return out.get("message", "arxiv.fetch failed")
                r = out.get("result", {}) or {}
                title = r.get("title", "")
                url = r.get("url", "")
                authors = ", ".join(r.get("authors", [])[:10])
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
                    fetch_props,
                    fetch_wrapper,
                )
            )

            self._initialized = True
            logger.info("[arXiv] tools registered")
        except Exception as e:
            logger.error(f"[arXiv] init_tools failed: {e}", exc_info=True)
            raise


_manager = None


def get_arxiv_manager():
    global _manager
    if _manager is None:
        _manager = ArxivToolsManager()
    return _manager

