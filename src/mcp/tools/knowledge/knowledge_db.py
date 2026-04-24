from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import List, Tuple

from src.utils.logging_config import get_logger
from src.utils.resource_finder import get_user_data_dir

logger = get_logger(__name__)


def _db_path() -> Path:
    data = get_user_data_dir(create=True)
    return data / "knowledge.db"


def _connect() -> sqlite3.Connection:
    p = _db_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(p))
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
    except Exception:
        pass
    return conn


def ensure_schema() -> None:
    conn = _connect()
    try:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS docs (id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT UNIQUE, mtime REAL, content TEXT);"
        )
        # Try to create FTS (optional)
        try:
            conn.execute(
                "CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts USING fts5(path, content, content='docs', content_rowid='id');"
            )
        except Exception as e:
            logger.warning(f"FTS not available: {e}")
        conn.commit()
    finally:
        conn.close()


def ingest_text_file(file_path: Path, max_chars: int = 200_000) -> None:
    ensure_schema()
    p = file_path
    if not p.exists() or not p.is_file():
        return

    try:
        stat = p.stat()
        text = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return

    if len(text) > max_chars:
        text = text[:max_chars]

    conn = _connect()
    try:
        cur = conn.execute("SELECT id, mtime FROM docs WHERE path=?", (str(p),))
        row = cur.fetchone()
        if row:
            doc_id, old_mtime = row
            if float(old_mtime or 0) >= float(stat.st_mtime):
                return
            conn.execute("UPDATE docs SET mtime=?, content=? WHERE id=?", (stat.st_mtime, text, doc_id))
        else:
            conn.execute("INSERT INTO docs(path, mtime, content) VALUES(?,?,?)", (str(p), stat.st_mtime, text))
        conn.commit()

        # If FTS exists, keep it in sync via simple rebuild for this doc (best-effort)
        try:
            conn.execute("INSERT INTO docs_fts(rowid, path, content) VALUES((SELECT id FROM docs WHERE path=?), ?, ?) ON CONFLICT(rowid) DO UPDATE SET path=excluded.path, content=excluded.content", (str(p), str(p), text))
            conn.commit()
        except Exception:
            pass

    finally:
        conn.close()


def ingest_dir(root: Path) -> int:
    root = root.resolve()
    ensure_schema()
    count = 0
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".md", ".txt"}:
            continue
        ingest_text_file(p)
        count += 1
    return count


def search(query: str, top_k: int = 5) -> List[Tuple[str, str]]:
    ensure_schema()
    q = (query or "").strip()
    if not q:
        return []
    top_k = max(1, min(int(top_k or 5), 10))

    conn = _connect()
    try:
        # Prefer FTS if it exists
        try:
            cur = conn.execute(
                "SELECT path, snippet(docs_fts, 1, '[', ']', '…', 20) AS snip FROM docs_fts WHERE docs_fts MATCH ? LIMIT ?",
                (q, top_k),
            )
            rows = cur.fetchall()
            if rows:
                return [(r[0], r[1]) for r in rows]
        except Exception:
            pass

        like = f"%{q}%"
        cur = conn.execute(
            "SELECT path, substr(content, max(1, instr(content, ?) - 80), 240) AS snip FROM docs WHERE content LIKE ? LIMIT ?",
            (q, like, top_k),
        )
        rows = cur.fetchall()
        return [(r[0], r[1]) for r in rows]
    finally:
        conn.close()
