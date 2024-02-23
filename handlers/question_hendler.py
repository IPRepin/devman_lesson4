from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from keyboards.reply_kb import main_keyboard
from misc.open_quiz import read_quiz_file
from misc.state import States

router_question = Router()


@router_question.message(F.text == "Новый вопрос")
async def question_next(message: types.Message, state: FSMContext) -> None:
    await state.set_state(States.next_questions)
    question_counter = await state.get_data()
    current_value = question_counter.get('current_value', 0)
    questions = read_quiz_file()
    if current_value < len(questions):
        await state.update_data(current_value=current_value + 1)
        question = questions[current_value]
        await state.update_data(right_answer=question["Ответ"])
        await message.answer(f'Вопрос:\n{question["Вопрос"]}')
    else:
        await message.reply('Вопросы закончились, вы прошли тест!')
        await state.clear()


@router_question.message(States.next_questions)
async def any_message(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    right_answer = data.get('right_answer')
    await state.update_data(message_answer=message.text)
    while right_answer == message.text:
        await message.answer("Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»",
                             reply_markup=main_keyboard)
        await state.set_state(States.next_answers)
        break
    else:
        await message.answer("Неправильно. Попробуйте еще раз?",
                             reply_markup=main_keyboard)

