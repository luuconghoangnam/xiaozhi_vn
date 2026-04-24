from __future__ import annotations

from typing import Any, Dict

from src.utils.logging_config import get_logger

from .wikipedia_api import wiki_search, wiki_summary

logger = get_logger(__name__)


class WikipediaToolsManager:
    def __init__(self):
        self._initialized = False

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        try:
            # wikipedia.search
            search_props = PropertyList(
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

            async def search_wrapper(args: Dict[str, Any]) -> str:
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
                    snippet = (r.get("snippet") or "").strip()
                    block = f"{i}) {title}\n{url}"
                    if snippet:
                        block += f"\n   {snippet}"
                    lines.append(block)
                return "\n".join(lines)

            add_tool(
                (
                    "wikipedia.search",
                    "Search Wikipedia (vi/en). Returns title, url, snippet.",
                    search_props,
                    search_wrapper,
                )
            )

            # wikipedia.summary
            summary_props = PropertyList(
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

            async def summary_wrapper(args: Dict[str, Any]) -> str:
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
                    summary_props,
                    summary_wrapper,
                )
            )

            self._initialized = True
            logger.info("[Wikipedia] tools registered")
        except Exception as e:
            logger.error(f"[Wikipedia] init_tools failed: {e}", exc_info=True)
            raise


_manager = None


def get_wikipedia_manager():
    global _manager
    if _manager is None:
        _manager = WikipediaToolsManager()
    return _manager

