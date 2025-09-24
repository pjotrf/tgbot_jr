import asyncio, json
from pathlib import Path
from typing import List, Optional, Dict, Any
from ..models import Ad

ADS_PATH = Path(__file__).resolve().parents[2] / "ads.json"
_lock = asyncio.Lock()

def _ensure_file():
    if not ADS_PATH.exists():
        ADS_PATH.write_text("[]", encoding="utf-8")

async def _load() -> List[Dict[str, Any]]:
    _ensure_file()
    async with _lock:
        data = ADS_PATH.read_text(encoding="utf-8")
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            ADS_PATH.write_text("[]", encoding="utf-8")
            return []

async def _save(items: List[Dict[str, Any]]) -> None:
    async with _lock:
        ADS_PATH.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

async def add(ad: Ad) -> int:
    items = await _load()
    new_id = (max((i.get("id", 0) for i in items), default=0) + 1) if items else 1
    ad.id = new_id
    items.append(ad.to_dict())
    await _save(items)
    return new_id

async def list_all() -> List[Dict[str, Any]]:
    return await _load()

async def like(ad_id: int) -> Optional[int]:
    items = await _load()
    for it in items:
        if it.get("id") == ad_id:
            it["likes"] = int(it.get("likes", 0)) + 1
            await _save(items)
            return it["likes"]
    return None

async def delete(ad_id: int, by_user: int) -> bool:
    items = await _load()
    for idx, it in enumerate(items):
        if it.get("id") == ad_id and it.get("user_id") == by_user:
            items.pop(idx)
            await _save(items)
            return True
    return False

async def get(ad_id: int) -> Optional[Dict[str, Any]]:
    items = await _load()
    for it in items:
        if it.get("id") == ad_id:
            return it
    return None
