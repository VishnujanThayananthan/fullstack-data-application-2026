# app/routers/items.py
import unicodedata
from typing import Any

from fastapi import APIRouter, HTTPException, Path, Query, Response

from app.schemas.item import ItemCreate, ItemRead, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])

FAKE_DB: dict[int, dict[str, Any]] = {}


def _normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value.lower())
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def _next_id() -> int:
    return max(FAKE_DB, default=0) + 1


# --- CREATE (POST) ---
@router.post("", response_model=ItemRead, status_code=201)
def create_item(payload: ItemCreate):
    item_id = _next_id()
    item = {"id": item_id, **payload.model_dump()}
    FAKE_DB[item_id] = item
    return item


# --- READ (GET Liste avec filtres) ---
@router.get("", response_model=list[ItemRead])
def list_items(
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=20, ge=1, le=100),
        q: str | None = None,
        disponible: bool | None = None,
):
    results = list(FAKE_DB.values())
    if q:
        normalized_query = _normalize_text(q)
        results = [
            item for item in results if normalized_query in _normalize_text(item["titre"])
        ]
    if disponible is not None:
        results = [item for item in results if item["disponible"] == disponible]
    return results[skip: skip + limit]


# --- READ (GET Un seul item) ---
@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int = Path(ge=1)):
    item = FAKE_DB.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} introuvable")
    return item


# --- UPDATE (PATCH - Modification partielle) ---
@router.patch("/{item_id}", response_model=ItemRead)
def update_item_partially(payload: ItemUpdate, item_id: int = Path(ge=1)):
    if item_id not in FAKE_DB:
        raise HTTPException(status_code=404, detail=f"Item {item_id} introuvable")

    item = FAKE_DB[item_id]
    # Les fameuses lignes qui posaient problème sont maintenant au bon endroit !
    data = payload.model_dump(exclude_unset=True)
    item.update(data)
    return item


# --- DELETE (Suppression) ---
@router.delete("/{item_id}", status_code=204, response_class=Response)
def delete_item(item_id: int = Path(ge=1)):
    if item_id not in FAKE_DB:
        raise HTTPException(status_code=404, detail=f"Item {item_id} introuvable")
    del FAKE_DB[item_id]
    return Response(status_code=204)