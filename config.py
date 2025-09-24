from pydantic import BaseModel
import os

class Settings(BaseModel):
    bot_token: str

def load_settings() -> Settings:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN env var is not set")
    return Settings(bot_token=token)
