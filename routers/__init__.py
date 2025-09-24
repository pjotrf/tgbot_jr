from .commands import router as commands_router
from .text import router as text_router
from .media_photo import router as photo_router
from .media_audio import router as audio_router
from .callbacks import router as callbacks_router

__all__ = [
    "commands_router",
    "text_router",
    "photo_router",
    "audio_router",
    "callbacks_router",
]
