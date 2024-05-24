import asyncio
import logging

import redis
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError, TelegramRetryAfter
from aiogram.fsm.storage.redis import RedisStorage

from config import REDIS_URL, TELEGRAM_TOKEN, REDIS_HOST, REDIS_PORT, REDIS_DB
from handlers.main_handlers import main_router
from handlers.question_hendler import router_question
from misc.logs_hendler_telegram import setup_bot_logger
from misc.open_quiz import read_quiz_file
from vk_bot.vk_bot import run_vk_bot

logger = logging.getLogger(__name__)


async def on_startup(telegram_token: str) -> None:
    storage = RedisStorage.from_url(REDIS_URL)
    bot = Bot(token=telegram_token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)
    dp.include_routers(
        main_router,
        router_question,
    )
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except TelegramNetworkError as error:
        logger.error(error)


def main() -> None:
    setup_bot_logger()
    read_quiz_file(redis_connect)
    try:
        asyncio.run(on_startup(TELEGRAM_TOKEN))
    except TelegramRetryAfter as retry_error:
        logger.error(retry_error)
    except KeyboardInterrupt:
        logger.info('Bot interrupted')


if __name__ == '__main__':
    redis_connect = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    main()
    run_vk_bot()
