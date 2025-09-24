from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from ..keyboards.inline import photo_caption_choice
from ..services import repo
from ..models import Ad
from .text import AddStates

router = Router()

@router.message(F.photo)
async def on_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    caption = message.caption

    if caption:
        ad = Ad(id=0, user_id=message.from_user.id, type="photo", file_id=file_id, caption=caption, likes=0)
        new_id = await repo.add(ad)
        await message.answer_photo(file_id, caption=f"✅ Фото-объявление сохранено (ID {new_id})")
        await state.clear()
        return

    await state.set_state(AddStates.awaiting_photo_caption)
    await state.update_data(pending_photo_id=file_id)
    await message.answer("Добавить описание к фото? Отправь текст. Или сохрани без описания:", reply_markup=photo_caption_choice())
