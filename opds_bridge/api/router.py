from urllib.parse import quote
from fastapi import APIRouter, Depends, Query, Response
from fastapi.responses import Response as FastAPIResponse
from lxml import etree

from opds_bridge.config import get_settings
from opds_bridge.security.basic import basic_auth_guard
from opds_bridge.services import abs_client as abs
from opds_bridge.opds.atom import atom_root, add_nav_entry
from opds_bridge.opds.builders import make_book_entry, add_pagination_links

router = APIRouter()

@router.get("/opds", response_class=FastAPIResponse, summary="Root OPDS catalog")
def opds_root(_=Depends(basic_auth_guard), settings=Depends(get_settings)):
    libs = [l for l in abs.list_libraries() if l.get("mediaType") == "book"]
    feed = atom_root("Audiobookshelf OPDS", "/opds", kind="navigation")
    for l in libs:
        add_nav_entry(feed, l["name"], f"/opds/library/{l['id']}?page=1")
    xml = etree.tostring(feed, xml_declaration=True, encoding="UTF-8")
    return Response(content=xml, media_type="application/atom+xml;profile=opds-catalog;kind=navigation")

@router.get("/opds/library/{lib_id}", response_class=FastAPIResponse,
            summary="Books in library (ebooks only)")
def opds_library(lib_id: str,
                 page: int = Query(1, ge=1),
                 limit: int = Query(100, ge=1, le=500),
                 _=Depends(basic_auth_guard),
                 settings=Depends(get_settings)):
    raw_items = abs.fetch_page_items(lib_id, page, limit)
    feed = atom_root(f"Library {lib_id}", f"/opds/library/{lib_id}?page={page}&limit={limit}")
    has_next = len(raw_items) == limit

    for it in raw_items:
        item_id = it.get("id")
        if not item_id:
            continue
        detail = it
        media = (detail.get("media") or {})
        if not media.get("ebookFile"):
            detail = abs.item_details(item_id)
            media = (detail.get("media") or {})
        if media.get("ebookFile") or media.get("ebookFormat"):
            make_book_entry(feed, detail, str(settings.ABS_BASE))

    add_pagination_links(feed, f"/opds/library/{lib_id}", page, limit, has_next)
    xml = etree.tostring(feed, xml_declaration=True, encoding="UTF-8")
    return Response(content=xml, media_type="application/atom+xml;profile=opds-catalog;kind=acquisition")
