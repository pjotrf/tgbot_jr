from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Создать объявление")],
            [KeyboardButton(text="📋 Список объявлений")],
        ],
        resize_keyboard=True
    )
