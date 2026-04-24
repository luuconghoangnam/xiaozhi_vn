from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from src.utils.logging_config import get_logger

from .knowledge_db import ingest_dir, search

logger = get_logger(__name__)


class KnowledgeToolsManager:
    def __init__(self):
        self._initialized = False

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        try:
            ingest_props = PropertyList([
                Property("dir", PropertyType.STRING),
            ])

            def ingest_wrapper(args: Dict[str, Any]) -> str:
                d = (args.get("dir") or "").strip()
                if not d:
                    return "Thiếu đường dẫn thư mục để ingest."
                p = Path(d).absolute()
                if not p.exists():
                    return f"Không thấy thư mục: {p}"
                n = ingest_dir(p)
                return f"Đã ingest {n} file (md/txt) từ: {p}"

            add_tool((
                "knowledge.ingest_dir",
                "Nạp tài liệu (md/txt) vào kho tri thức local (SQLite) để AI tra cứu.",
                ingest_props,
                ingest_wrapper,
            ))

            search_props = PropertyList([
                Property("query", PropertyType.STRING),
                Property("top_k", PropertyType.INTEGER, default_value=5, min_value=1, max_value=10),
            ])

            def search_wrapper(args: Dict[str, Any]) -> str:
                q = args.get("query", "")
                k = args.get("top_k", 5)
                hits = search(q, k)
                if not hits:
                    return "Không tìm thấy đoạn phù hợp trong kho tri thức local."
                lines = [f"Kết quả tra cứu (local knowledge) cho: {q}"]
                for i, (path, snip) in enumerate(hits, 1):
                    lines.append(f"{i}) {path}\n   {snip}")
                return "\n".join(lines)

            add_tool((
                "knowledge.search",
                "Tra cứu kho tri thức local (SQLite). Trả về trích đoạn + đường dẫn file.",
                search_props,
                search_wrapper,
            ))

            self._initialized = True
            logger.info("[Knowledge] tools registered")
        except Exception as e:
            logger.error(f"[Knowledge] init_tools failed: {e}", exc_info=True)
            raise


_manager = None


def get_knowledge_manager():
    global _manager
    if _manager is None:
        _manager = KnowledgeToolsManager()
    return _manager
