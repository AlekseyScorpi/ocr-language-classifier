import asyncio
from aiogram import Bot, Dispatcher
from bot.config import BotConfig
from bot.handlers import image
from bot.logger import logger

async def main():
    config = BotConfig.load()
    bot = Bot(token=config.token)
    dp = Dispatcher()

    dp.include_router(image.router)
    logger.info("Bot is started!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())