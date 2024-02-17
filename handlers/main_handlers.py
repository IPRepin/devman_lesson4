from aiogram import types, Router
from aiogram.filters import CommandStart

from keyboards.reply_kb import main_keyboard

main_router = Router()


@main_router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(f"Здравствуйте {message.from_user.first_name}!", reply_markup=main_keyboard)


@main_router.message()
async def any_message(message: types.Message):
    await message.answer(message.text)
