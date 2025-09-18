from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
)

def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Создать объявление")],
            [KeyboardButton(text="📋 Список объявлений")]
        ],
        resize_keyboard=True
    )

def confirm_text_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Сохранить", callback_data="confirm_text:save")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="confirm_text:cancel")]
    ])

def photo_caption_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💾 Сохранить без описания", callback_data="photo:save_no_caption")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="photo:cancel")]
    ])

def ad_controls_kb(ad_id: int, likes: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"❤️ {likes}", callback_data=f"ad:like:{ad_id}"),
            InlineKeyboardButton(text="🗑 Удалить", callback_data=f"ad:del:{ad_id}")
        ]
    ])
