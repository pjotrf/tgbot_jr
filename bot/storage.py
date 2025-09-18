import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

ADS_PATH = Path(__file__).resolve().parent.parent / "ads.json"
_lock = asyncio.Lock()

def _ensure_file():
    if not ADS_PATH.exists():
        ADS_PATH.write_text("[]", encoding="utf-8")

async def load_ads() -> List[Dict[str, Any]]:
    _ensure_file()
    async with _lock:
        data = ADS_PATH.read_text(encoding="utf-8")
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            ADS_PATH.write_text("[]", encoding="utf-8")
            return []

async def save_ads(ads: List[Dict[str, Any]]) -> None:
    async with _lock:
        ADS_PATH.write_text(json.dumps(ads, ensure_ascii=False, indent=2), encoding="utf-8")

async def add_ad(ad: Dict[str, Any]) -> int:
    ads = await load_ads()
    ad_id = (max((a.get("id", 0) for a in ads), default=0) + 1) if ads else 1
    ad["id"] = ad_id
    ads.append(ad)
    await save_ads(ads)
    return ad_id

async def get_ad(ad_id: int) -> Optional[Dict[str, Any]]:
    ads = await load_ads()
    for a in ads:
        if a.get("id") == ad_id:
            return a
    return None

async def like_ad(ad_id: int) -> Optional[int]:
    ads = await load_ads()
    for a in ads:
        if a.get("id") == ad_id:
            a["likes"] = int(a.get("likes", 0)) + 1
            await save_ads(ads)
            return a["likes"]
    return None

async def delete_ad(ad_id: int, by_user: int) -> bool:
    ads = await load_ads()
    for i, a in enumerate(ads):
        if a.get("id") == ad_id and a.get("user_id") == by_user:
            ads.pop(i)
            await save_ads(ads)
            return True
    return False

async def list_ads() -> List[Dict[str, Any]]:
    return await load_ads()
