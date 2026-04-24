from __future__ import annotations

from typing import Any, Dict

from src.utils.logging_config import get_logger

from .search import duckduckgo_search, fetch_url

logger = get_logger(__name__)


class WebSearchToolsManager:
    def __init__(self):
        self._initialized = False

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        try:
            # web.search
            query_props = PropertyList([
                Property("query", PropertyType.STRING),
                Property("max_results", PropertyType.INTEGER, default_value=5, min_value=1, max_value=10),
            ])

            def search_wrapper(args: Dict[str, Any]) -> str:
                q = args.get("query", "")
                n = args.get("max_results", 5)
                out = duckduckgo_search(q, n)
                if out.get("status") != "success":
                    return out.get("message", "search failed")

                results = out.get("results", [])
                if not results:
                    return "Không tìm thấy kết quả web phù hợp."

                lines = [f"Kết quả web cho: {out.get('query')}"]
                for i, r in enumerate(results, 1):
                    title = r.get("title", "")
                    url = r.get("url", "")
                    snip = r.get("snippet", "")
                    block = f"{i}) {title}\n{url}"
                    if snip:
                        block += f"\n   {snip}"
                    lines.append(block)
                return "\n".join(lines)

            add_tool((
                "web.search",
                "Tìm kiếm web (DuckDuckGo) không cần API key. Trả về danh sách link + snippet.",
                query_props,
                search_wrapper,
            ))

            # web.fetch
            fetch_props = PropertyList([
                Property("url", PropertyType.STRING),
                Property("max_chars", PropertyType.INTEGER, default_value=8000, min_value=500, max_value=50000),
            ])

            def fetch_wrapper(args: Dict[str, Any]) -> str:
                u = args.get("url", "")
                m = args.get("max_chars", 8000)
                out = fetch_url(u, m)
                if out.get("status") != "success":
                    return out.get("message", "fetch failed")
                return f"URL: {out.get('url')}\n\n{out.get('text', '')}"

            add_tool((
                "web.fetch",
                "Tải nội dung 1 trang web và trích text để AI đọc nhanh.",
                fetch_props,
                fetch_wrapper,
            ))

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
