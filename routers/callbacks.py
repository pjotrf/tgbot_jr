from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from ..keyboards.inline import ad_controls
from ..services import repo

router = Router()

@router.callback_query(F.data.startswith("confirm:"))
async def cb_confirm(call: CallbackQuery, state: FSMContext):
    action = call.data.split(":")[1]
    data = await state.get_data()
    draft = data.get("draft_text")
    if action == "save" and draft:
        from ..models import Ad
        ad = Ad(id=0, user_id=call.from_user.id, type="text", content=draft, likes=0)
        new_id = await repo.add(ad)
        await call.message.edit_text(f"✅ Сохранено! (ID {new_id})\n\n<blockquote>{draft}</blockquote>")
        await state.clear()
    else:
        await call.message.edit_text("❌ Отменено.")
        await state.clear()
    await call.answer()

@router.callback_query(F.data.startswith("photo:"))
async def cb_photo(call: CallbackQuery, state: FSMContext):
    action = call.data.split(":")[1]
    data = await state.get_data()
    file_id = data.get("pending_photo_id")

    if action == "no_caption" and file_id:
        from ..models import Ad
        ad = Ad(id=0, user_id=call.from_user.id, type="photo", file_id=file_id, caption=None, likes=0)
        new_id = await repo.add(ad)
        await call.message.answer_photo(file_id, caption=f"✅ Фото-объявление сохранено (ID {new_id})")
        await state.clear()
        try:
            await call.message.delete()
        except Exception:
            pass
    else:
        await call.message.edit_text("❌ Отменено.")
        await state.clear()
    await call.answer()

@router.callback_query(F.data.startswith("ad:like:"))
async def cb_like(call: CallbackQuery):
    ad_id = int(call.data.split(":")[-1])
    new_likes = await repo.like(ad_id)
    if new_likes is None:
        await call.answer("Объявление не найдено.", show_alert=True)
        return
    try:
        await call.message.edit_reply_markup(reply_markup=ad_controls(ad_id, new_likes))
    except Exception:
        pass
    await call.answer("❤️ Спасибо!")

@router.callback_query(F.data.startswith("ad:del:"))
async def cb_del(call: CallbackQuery):
    ad_id = int(call.data.split(":")[-1])
    ok = await repo.delete(ad_id, call.from_user.id)
    if not ok:
        await call.answer("Удалить может только автор.", show_alert=True)
        return
    await call.answer("🗑 Удалено.")
    try:
        await call.message.delete()
    except Exception:
        pass
