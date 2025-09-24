from aiogram import Router, F
from aiogram.types import Message
from ..services import repo
from ..models import Ad

router = Router()

@router.message(F.audio)
async def on_audio(message: Message):
    ad = Ad(id=0, user_id=message.from_user.id, type="audio", file_id=message.audio.file_id, caption=message.caption, likes=0)
    await repo.add(ad)
    await message.answer("🎶 Аудио-объявление добавлено.")

@router.message(F.voice)
async def on_voice(message: Message):
    ad = Ad(id=0, user_id=message.from_user.id, type="voice", file_id=message.voice.file_id, caption=message.caption, likes=0)
    await repo.add(ad)
    await message.answer("🎶 Аудио-объявление добавлено.")
