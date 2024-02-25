from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from handlers.question_hendler import question_next
from keyboards.reply_kb import main_keyboard

main_router = Router()


@main_router.message(CommandStart())
async def start_command(message: types.Message) -> None:
    await message.answer(f"Здравствуйте {message.from_user.first_name}!", reply_markup=main_keyboard)


@main_router.message(F.text == "Новый вопрос")
async def new_question(message: types.Message, state: FSMContext) -> None:
    await question_next(message, state)
