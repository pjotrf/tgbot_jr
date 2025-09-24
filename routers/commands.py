from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from ..keyboards.reply import main_menu
from ..services import repo

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! Я бот-объявления.\n\n"
        "Команды:\n"
        "/add — создать объявление\n"
        "/list — показать объявления\n"
        "/help — помощь",
        reply_markup=main_menu()
    )

@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        "📖 Возможности:\n"
        "• Текст: сохраню после подтверждения.\n"
        "• Фото: можно с описанием или без, храню file_id.\n"
        "• Аудио/Голос: храню file_id.\n\n"
        "Команды: /add, /list, /start"
    )

@router.message(Command("list"))
async def list_cmd(message: Message):
    items = await repo.list_all()
    if not items:
        await message.answer("Пока объявлений нет. Добавь первое через /add 🙂")
        return
    from ..keyboards.inline import ad_controls
    for ad in items:
        ad_id = ad.get("id")
        likes = int(ad.get("likes", 0))
        kb = ad_controls(ad_id, likes)
        t = ad.get("type")
        if t == "text":
            await message.answer(f"📝 <b>Текст:</b> {ad.get('content')}", reply_markup=kb)
        elif t == "photo":
            await message.answer_photo(ad["file_id"], caption=ad.get("caption") or "📷 Фото-объявление", reply_markup=kb)
        elif t in ("audio", "voice"):
            label = "🎶 Аудио" if t == "audio" else "🎙 Голос"
            text = ad.get("caption") or f"{label}-объявление"
            if t == "audio":
                await message.answer_audio(ad["file_id"], caption=text, reply_markup=kb)
            else:
                await message.answer_voice(ad["file_id"], caption=text, reply_markup=kb)
        else:
            await message.answer(f"❓ Неизвестный тип объявления: {t}", reply_markup=kb)
