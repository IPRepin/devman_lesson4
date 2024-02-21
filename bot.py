import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv

from handlers.main_handlers import main_router
from handlers.question_hendler import router_question

logger = logging.getLogger(__name__)


async def on_startup(telegram_token: str) -> None:
    storage = RedisStorage.from_url("redis://localhost:6379/0")
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
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    try:
        asyncio.run(on_startup(telegram_token))
    except KeyboardInterrupt:
        logger.info('Bot interrupted')


if __name__ == '__main__':
    main()
