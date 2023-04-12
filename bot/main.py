import asyncio
import logging
import sys
from logging.handlers import RotatingFileHandler

import handlers
import job
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contains import BASE_DIR, BOT_TELEGRAM_TOKEN, DB_URL, UPDATE_TIME
from middlewares import DbSessionMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s [%(levelname)s] - "
            "(%(filename)s).%(funcName)s:%(lineno)d - %(message)s"
        ),
        handlers=[
            RotatingFileHandler(
                f"{BASE_DIR}/output.log", maxBytes=50000000, backupCount=10
            ),
            logging.StreamHandler(sys.stdout),
        ],
    )

    bot = Bot(token=BOT_TELEGRAM_TOKEN)

    engine = create_async_engine(url=DB_URL, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        job.update_db,
        trigger="interval",
        seconds=UPDATE_TIME,
        kwargs={"session": sessionmaker()},
    )
    scheduler.start()

    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.include_router(handlers.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
