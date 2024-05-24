import redis
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from keyboards.reply_kb import main_keyboard
from misc.redis_conn import get_redis_conn
from misc.state import States

router_question = Router()


@router_question.message(F.text == "Новый вопрос")
async def get_question_next(message: types.Message, state: FSMContext) -> None:
    redis_connect = get_redis_conn()
    await state.set_state(States.next_questions)
    question_counter = await state.get_data()
    current_value = question_counter.get('current_value', 0)
    total_questions = int(redis_connect.get("quiz:total_questions"))
    if current_value < total_questions:
        await state.update_data(current_value=current_value + 1)
        question_key = f"quiz:question:{current_value}:question"
        answer_key = f"quiz:question:{current_value}:answer"
        question = redis_connect.get(question_key).decode("utf-8")
        answer = redis_connect.get(answer_key).decode("utf-8")

        await state.update_data(right_answer=answer)
        await message.answer(f'Вопрос:\n{question}')
    else:
        await message.answer('Вопросы закончились, вы прошли тест!')
        await is_score_reply(message, state)
        await state.clear()


@router_question.message(F.text == "Сдаться")
async def is_surrender(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    right_answer = data.get('right_answer')
    await state.set_state(States.next_answers)
    await message.answer(f'Правильный ответ: {right_answer}')
    await get_question_next(message, state)


@router_question.message(States.next_questions)
async def get_next_answer(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    right_answer = data.get('right_answer')
    user_answer = message.text
    score = data.get("score", 0)
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
async def is_score_reply(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    score = data.get("score", 0)
    await message.answer(f"Ваш счет: {score}", reply_markup=main_keyboard)
