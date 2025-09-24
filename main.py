import asyncio
import logging
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from .config import load_settings
from .routers import (
    commands_router,
    text_router,
    photo_router,
    audio_router,
    callbacks_router,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

def build_dp() -> Dispatcher:
    dp = Dispatcher()
    dp.include_router(commands_router)
    dp.include_router(text_router)
    dp.include_router(photo_router)
    dp.include_router(audio_router)
    dp.include_router(callbacks_router)
    return dp

async def _main():
    settings = load_settings()
    bot = Bot(
        settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = build_dp()
    await dp.start_polling(bot)

def main():
    asyncio.run(_main())

if __name__ == "__main__":
    main()
