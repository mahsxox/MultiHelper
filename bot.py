import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from storage.database import init_db
from storage.reminder_scheduler import check_reminders
from handlers.start_help import router as start_help_router
from handlers.weather import router as weather_router
from handlers.motivation import router as motivation_router
from handlers.reminder import router as reminder_router
from handlers.language import router as language_router
from middlewares.logging_middleware import OuterLoggerMiddleware


logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(OuterLoggerMiddleware())

    dp.include_routers(
        start_help_router,
        weather_router,
        motivation_router,
        reminder_router,
        language_router
    )

    await init_db()
    asyncio.create_task(check_reminders(bot))

    logger.info("Bot started")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())