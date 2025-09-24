from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def confirm_text() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Сохранить", callback_data="confirm:save")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="confirm:cancel")],
    ])

def photo_caption_choice() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💾 Сохранить без описания", callback_data="photo:no_caption")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="photo:cancel")],
    ])

def ad_controls(ad_id: int, likes: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"❤️ {likes}", callback_data=f"ad:like:{ad_id}"),
            InlineKeyboardButton(text="🗑 Удалить", callback_data=f"ad:del:{ad_id}")
        ]
    ])
