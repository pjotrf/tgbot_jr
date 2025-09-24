from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from ..keyboards.inline import confirm_text

router = Router()

class AddStates(StatesGroup):
    awaiting_content = State()
    awaiting_text_confirm = State()
    awaiting_photo_caption = State()

@router.message(F.text == "📝 Создать объявление")
@router.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext):
    await state.set_state(AddStates.awaiting_content)
    await message.answer("Окей! Отправь <b>текст</b>, <b>фото</b> или <b>аудио/голос</b> для объявления.")

@router.message(F.text == "📋 Список объявлений")
async def menu_list(message: Message):
    from .commands import list_cmd
    await list_cmd(message)

# generic text
@router.message(F.text & ~F.text.startswith("/"))
async def on_text(message: Message, state: FSMContext):
    cur = await state.get_state()
    if cur == AddStates.awaiting_photo_caption.state:
        return
    await state.update_data(draft_text=message.text)
    await state.set_state(AddStates.awaiting_text_confirm)
    await message.answer(
        f"Ты написал:\n\n<blockquote>{message.text}</blockquote>\n\nСохранить как объявление?",
        reply_markup=confirm_text()
    )