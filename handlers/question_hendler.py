from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from misc.open_quiz import read_quiz_file
from misc.state import States

router_question = Router()


@router_question.message(F.text == "Новый вопрос")
async def question_next(message: types.Message, state: FSMContext):
    await state.set_state(States.next_questions)
    question_counter = await state.get_data()
    current_value = question_counter.get('current_value', 0)
    questions = read_quiz_file()
    if current_value < len(questions):
        await state.update_data(current_value=current_value + 1)
        question = questions[current_value]
        await message.answer(f'Вопрос:\n{question["Вопрос"]}')
    else:
        await message.reply('Вопросы закончились, вы прошли тест!')


@router_question.message(States.next_questions)
async def any_message(message: types.Message, state: FSMContext) -> None:
    pass
