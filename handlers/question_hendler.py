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
        await message.answer('Вопросы закончились, вы прошли тест!')
        await score_reply(message, state)
        await state.clear()


@router_question.message(F.text == "Сдаться")
async def surrender(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    right_answer = data.get('right_answer')
    await state.set_state(States.next_answers)
    await message.answer(f'Правильный ответ: {right_answer}')
    await question_next(message, state)


@router_question.message(States.next_questions)
async def answer_next_question(message: types.Message, state: FSMContext) -> None:
    if message.text == "Мой счет":
        await score_reply(message, state)
    data = await state.get_data()
    right_answer = data.get('right_answer')
    user_answer = message.text
    score = data.get("score", 0)  # Получаем значение по умолчанию 0, если нет ключа "score"
    if right_answer == user_answer:
        score += 1
        await state.update_data(score=score)
        await message.answer("Правильно! Поздравляю! Для следующего вопроса нажмите «Новый вопрос»",
                             reply_markup=main_keyboard)
        await state.set_state(States.next_answers)
    else:
        await message.answer("Неправильно. Попробуйте еще раз?",
                             reply_markup=main_keyboard)


@router_question.message(F.text == "Мой счет")
async def score_reply(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    score = data.get("score", 0)
    await message.answer(f"Ваш счет: {score}", reply_markup=main_keyboard)
