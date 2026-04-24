from __future__ import annotations

import asyncio
import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, List

import requests


ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


def _clean_text(s: str) -> str:
    s = (s or "").strip()
    s = re.sub(r"\s+", " ", s)
    return s


def _parse_feed(xml_text: str) -> List[Dict[str, Any]]:
    root = ET.fromstring(xml_text)
    out: List[Dict[str, Any]] = []
    for entry in root.findall("atom:entry", ATOM_NS):
        title = _clean_text((entry.findtext("atom:title", default="", namespaces=ATOM_NS)))
        summary = _clean_text((entry.findtext("atom:summary", default="", namespaces=ATOM_NS)))
        published = _clean_text((entry.findtext("atom:published", default="", namespaces=ATOM_NS)))
        updated = _clean_text((entry.findtext("atom:updated", default="", namespaces=ATOM_NS)))
        entry_id = _clean_text((entry.findtext("atom:id", default="", namespaces=ATOM_NS)))

        authors = []
        for a in entry.findall("atom:author", ATOM_NS):
            name = _clean_text(a.findtext("atom:name", default="", namespaces=ATOM_NS))
            if name:
                authors.append(name)

        primary_url = ""
        for link in entry.findall("atom:link", ATOM_NS):
            rel = link.attrib.get("rel", "")
            href = link.attrib.get("href", "")
            if rel == "alternate" and href:
                primary_url = href
                break
        if not primary_url:
            primary_url = entry_id

        out.append(
            {
                "id": entry_id,
                "url": primary_url,
                "title": title,
                "summary": summary,
                "authors": authors,
                "published": published,
                "updated": updated,
            }
        )
    return out


async def arxiv_search(query: str, max_results: int = 5) -> Dict[str, Any]:
    query = (query or "").strip()
    if not query:
        return {"status": "error", "message": "Thieu query"}

    max_results = max(1, min(int(max_results), 10))
    url = "https://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }

    def _req():
        r = requests.get(url, params=params, timeout=20, headers={"user-agent": "xiaozhi-vn/1.0"})
        r.raise_for_status()
        return r.text

    try:
        xml_text = await asyncio.to_thread(_req)
        entries = _parse_feed(xml_text)
        return {"status": "success", "query": query, "results": entries}
    except Exception as e:
        return {"status": "error", "message": f"arXiv search error: {e}"}


async def arxiv_fetch(arxiv_id_or_url: str) -> Dict[str, Any]:
    raw = (arxiv_id_or_url or "").strip()
    if not raw:
        return {"status": "error", "message": "Thieu id/url"}

    # Normalize to arxiv id.
    arxiv_id = raw
    m = re.search(r"arxiv\.org/abs/([^?#/]+)", raw)
    if m:
        arxiv_id = m.group(1)
    arxiv_id = arxiv_id.replace("arXiv:", "").strip()

    url = "https://export.arxiv.org/api/query"
    params = {"id_list": arxiv_id}

    def _req():
        r = requests.get(url, params=params, timeout=20, headers={"user-agent": "xiaozhi-vn/1.0"})
        r.raise_for_status()
        return r.text

    try:
        xml_text = await asyncio.to_thread(_req)
        entries = _parse_feed(xml_text)
        if not entries:
            return {"status": "error", "message": f"Khong tim thay bai: {arxiv_id}"}
        return {"status": "success", "id": arxiv_id, "result": entries[0]}
    except Exception as e:
        return {"status": "error", "message": f"arXiv fetch error: {e}"}

