"""A-Z sorting of home-screen pages, shared by ``iconshuffle sort`` and the editor.

Sorting redeals every movable item over all pages: each page keeps its length and
widgets keep their cells, while apps, folders, web clips and web apps fill the free
slots in name order. The dock and folder contents never move.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .state import is_widget, item_name, split_state, to_payload


def _redeal(pages, key, pinned) -> list[list[Any]]:
    """Sort the non-pinned items of ``pages`` and put them back in the same slots."""
    slots = [
        (p, i) for p, page in enumerate(pages) for i, item in enumerate(page) if not pinned(item)
    ]
    ordered = sorted((pages[p][i] for p, i in slots), key=key)
    out = [list(page) for page in pages]
    for (p, i), item in zip(slots, ordered, strict=True):
        out[p][i] = item
    return out


def sort_state(state) -> dict[str, Any]:
    """The phone's state with every page A-Z by item name; dock and widgets kept."""
    payload = to_payload(state)
    _, pages = split_state(payload)
    payload["iconLists"] = _redeal(
        pages, key=lambda item: item_name(item).casefold(), pinned=is_widget
    )
    return payload


def sort_view(layout: Mapping[str, Any]) -> dict[str, Any]:
    """An editor view-layout (``{dock, pages: [{items}]}``) with pages sorted A-Z."""
    pages = [list(page.get("items", [])) for page in layout.get("pages", [])]
    return {
        "dock": list(layout.get("dock", [])),
        "pages": [
            {"items": items}
            for items in _redeal(
                pages,
                key=lambda item: str(item.get("name") or "").casefold(),
                pinned=lambda item: item.get("type") == "widget",
            )
        ],
    }
