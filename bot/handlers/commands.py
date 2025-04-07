from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from ocr_engine.utils import get_list_languages

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "👋 Привет! Отправь мне изображение с текстом, и я попробую определить язык текста на нём."
    )

@router.message(Command("list"))
async def start_handler(message: Message):
    await message.answer(
        "📝 Вот список языков, которые я определяю:\n"
        f"{', '.join(get_list_languages())}"
    )

@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "📌 Просто пришли фото с текстом, и я определю язык. "
        "Поддерживаются изображения с печатным текстом на популярных языках.\n\n"
        "Команды:\n"
        "/start — приветствие\n"
        "/help — помощь\n"
        "/list - список определяемых языков языков"
    )