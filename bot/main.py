import asyncio
from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook
from bot.config import BotConfig
from bot.handlers import image, commands
from bot.logger import logger

async def main():
    bot_config = BotConfig.load()
    bot = Bot(token=bot_config.token)
    dp = Dispatcher()

    dp.include_router(image.router)
    dp.include_router(commands.router)
    logger.info("Bot is started!")
    try:
        await bot(DeleteWebhook(drop_pending_updates=True))
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("✅ Correct bot stop")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Stopping program")