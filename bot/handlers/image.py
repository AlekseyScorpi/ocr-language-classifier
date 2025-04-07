from aiogram import Router, F
from aiogram.types import Message
from PIL import Image
from io import BytesIO
from ocr_engine.config import get_ocr_engine
from ocr_engine.classifier import predict
from bot.logger import logger
from ocr_engine.lang_map import LANG_ID_TO_NAME

from bot.config import BotConfig

router = Router()
config = BotConfig.load()
ocr_engine = get_ocr_engine(config.tessdata_dir)

@router.message(F.photo)
async def handle_image(message: Message):
    photo = message.photo[-1]
    
    photo_bytes = BytesIO()
    await message.bot.download(photo, destination=photo_bytes)
    photo_bytes.seek(0)

    try:
        img = Image.open(photo_bytes)
        result = predict(ocr_engine.predict(img))
        lang_name = LANG_ID_TO_NAME.get(result, "Неизвестный язык")
        await message.reply(f"📄 Предполагаемый язык {lang_name}")
    except Exception as e:
        await message.reply("⚠️ Ошибка при обработке изображения.")
        logger.exception(f"Error {e}")