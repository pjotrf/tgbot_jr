import asyncio
from datetime import datetime, UTC

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode, ContentType
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from tgtoken import BOT_TOKEN
from storage import add_ad, list_ads, like_ad, delete_ad
from keyboards import main_menu, confirm_text_kb, ad_controls_kb, photo_caption_kb


bot = Bot(
    BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

class AddStates(StatesGroup):
    awaiting_content = State()
    awaiting_text_confirm = State()
    awaiting_photo_caption = State()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот-объявления.\n\n"
        "Используй меню ниже или команды:\n"
        "/add — создать объявление\n"
        "/list — показать объявления\n"
        "/help — помощь",
        reply_markup=main_menu()
    )

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📖 Возможности:\n"
        "• Отправь текст — предложу сохранить как объявление.\n"
        "• Отправь фото — спрошу про описание и сохраню file_id.\n"
        "• Отправь аудио/голос — сохраню file_id.\n\n"
        "Команды:\n"
        "/add — начать создание\n"
        "/list — показать все\n"
        "/start — приветствие"
    )

@dp.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext):
    await state.set_state(AddStates.awaiting_content)
    await message.answer("Окей! Отправь <b>текст</b>, <b>фото</b> или <b>аудио/голос</b> для объявления.")

@dp.message(Command("list"))
async def cmd_list(message: Message):
    ads = await list_ads()
    if not ads:
        await message.answer("Пока объявлений нет. Добавь первое через /add 🙂")
        return
    for ad in ads:
        ad_id = ad.get("id")
        likes = int(ad.get("likes", 0))
        kb = ad_controls_kb(ad_id, likes)
        if ad["type"] == "text":
            await message.reply(f"📝 <b>Текст:</b> {ad['content']}", reply_markup=kb)
        elif ad["type"] == "photo":
            caption = ad.get("caption") or "📷 Фото-объявление"
            await message.answer_photo(ad["file_id"], caption=caption, reply_markup=kb)
        elif ad["type"] in ("audio", "voice"):
            label = "🎶 Аудио" if ad["type"] == "audio" else "🎙 Голос"
            text = ad.get("caption") or f"{label}-объявление"
            if ad["type"] == "audio":
                await message.answer_audio(ad["file_id"], caption=text, reply_markup=kb)
            else:
                await message.answer_voice(ad["file_id"], caption=text, reply_markup=kb)
        else:
            await message.answer(f"❓ Неизвестный тип объявления: {ad['type']}", reply_markup=kb)

@dp.message(F.text == "📝 Создать объявление")
async def menu_add(message: Message, state: FSMContext):
    await cmd_add(message, state)

@dp.message(F.text == "📋 Список объявлений")
async def menu_list(message: Message):
    await cmd_list(message)

@dp.message(F.content_type == ContentType.TEXT, ~F.text.startswith("/"))
async def handle_text(message: Message, state: FSMContext):
    cur = await state.get_state()
    if cur == AddStates.awaiting_photo_caption.state:
        data = await state.get_data()
        file_id = data.get("pending_photo_id")
        if not file_id:
            await message.answer("Что-то пошло не так. Попробуй ещё раз /add.")
            await state.clear()
            return
        ad = {
            "user_id": message.from_user.id,
            "type": "photo",
            "file_id": file_id,
            "caption": message.text,
            "likes": 0,
            "created_at": datetime.now(UTC).isoformat()
        }
        ad_id = await add_ad(ad)
        await message.answer_photo(file_id, caption=f"✅ Сохранено! (ID {ad_id})\n{message.text}")
        await state.clear()
        return
    await state.update_data(draft_text=message.text)
    await state.set_state(AddStates.awaiting_text_confirm)
    await message.answer(
        f"Ты написал:\n\n<blockquote>{message.text}</blockquote>\n\nСохранить как объявление?",
        reply_markup=confirm_text_kb()
    )

@dp.message(F.photo)
async def handle_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    caption = message.caption
    if caption:
        ad = {
            "user_id": message.from_user.id,
            "type": "photo",
            "file_id": file_id,
            "caption": caption,
            "likes": 0,
            "created_at": datetime.now(UTC).isoformat()
        }
        ad_id = await add_ad(ad)
        await message.answer_photo(file_id, caption=f"✅ Фото-объявление сохранено (ID {ad_id})")
        await state.clear()
        return
    await state.set_state(AddStates.awaiting_photo_caption)
    await state.update_data(pending_photo_id=file_id)
    await message.answer(
        "Добавить описание к фото? Отправь текст одним сообщением.\nИли сохрани без описания:",
        reply_markup=photo_caption_kb()
    )

@dp.message(F.audio)
async def handle_audio(message: Message, state: FSMContext):
    ad = {
        "user_id": message.from_user.id,
        "type": "audio",
        "file_id": message.audio.file_id,
        "caption": message.caption,
        "likes": 0,
        "created_at": datetime.now(UTC).isoformat()
    }
    await add_ad(ad)
    await message.answer("🎶 Аудио-объявление добавлено.")
    await state.clear()

@dp.message(F.voice)
async def handle_voice(message: Message, state: FSMContext):
    ad = {
        "user_id": message.from_user.id,
        "type": "voice",
        "file_id": message.voice.file_id,
        "caption": message.caption,
        "likes": 0,
        "created_at": datetime.now(UTC).isoformat()
    }
    await add_ad(ad)
    await message.answer("🎶 Аудио-объявление добавлено.")
    await state.clear()

@dp.callback_query(F.data.startswith("confirm_text:"))
async def cb_confirm_text(call: CallbackQuery, state: FSMContext):
    action = call.data.split(":", 1)[1]
    data = await state.get_data()
    draft = data.get("draft_text")
    if action == "save" and draft:
        ad = {
            "user_id": call.from_user.id,
            "type": "text",
            "content": draft,
            "likes": 0,
            "created_at": datetime.now(UTC).isoformat()
        }
        ad_id = await add_ad(ad)
        await call.message.edit_text(f"✅ Сохранено! (ID {ad_id})\n\n<blockquote>{draft}</blockquote>")
        await state.clear()
    else:
        await call.message.edit_text("❌ Отменено.")
        await state.clear()
    await call.answer()

@dp.callback_query(F.data.startswith("photo:"))
async def cb_photo(call: CallbackQuery, state: FSMContext):
    action = call.data.split(":", 1)[1]
    data = await state.get_data()
    file_id = data.get("pending_photo_id")
    if action == "save_no_caption" and file_id:
        ad = {
            "user_id": call.from_user.id,
            "type": "photo",
            "file_id": file_id,
            "caption": None,
            "likes": 0,
            "created_at": datetime.now(UTC).isoformat()
        }
        await add_ad(ad)
        await call.message.answer_photo(file_id, caption=f"✅ Фото-объявление сохранено")
        await state.clear()
        await call.message.delete()
    else:
        await call.message.edit_text("❌ Отменено.")
        await state.clear()
    await call.answer()

@dp.callback_query(F.data.startswith("ad:like:"))
async def cb_like(call: CallbackQuery):
    new_likes = await like_ad(int(call.data.split(":")[-1]))
    if new_likes is None:
        await call.answer("Объявление не найдено.", show_alert=True)
        return
    kb = ad_controls_kb(int(call.data.split(":")[-1]), new_likes)
    try:
        await call.message.edit_reply_markup(reply_markup=kb)
    except Exception:
        pass
    await call.answer("❤️ Спасибо!")

@dp.callback_query(F.data.startswith("ad:del:"))
async def cb_delete(call: CallbackQuery):
    ok = await delete_ad(int(call.data.split(":")[-1]), call.from_user.id)
    if not ok:
        await call.answer("Удалить может только автор.", show_alert=True)
        return
    await call.answer("🗑 Удалено.")
    try:
        await call.message.delete()
    except Exception:
        pass

def main():
    asyncio.run(dp.start_polling(bot))

if __name__ == "__main__":
    main()
