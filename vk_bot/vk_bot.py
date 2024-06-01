import logging

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from config import VK_TOKEN
from misc.redis_conn import get_redis_conn
from vk_bot.vk_keyboard import main_menu_keyboard

logger = logging.getLogger(__name__)
session = vk_api.VkApi(token=VK_TOKEN)


def send_message(user_id, message, keyboard=None):
    post = {
        'user_id': user_id,
        'message': message,
        'random_id': 0,
    }
    if keyboard is not None:
        post['keyboard'] = keyboard.get_keyboard()
    session.method('messages.send', post)


def open_questions(user_id: int, message: str) -> None:
    redis_connect = get_redis_conn()
    user_key = f"user:{user_id}"
    quiz_start_key = f"{user_key}:quiz_start"
    current_key = f"{user_key}:current"
    points_key = f"{user_key}:points"

    if not redis_connect.exists(quiz_start_key):
        redis_connect.set(quiz_start_key, False)
        redis_connect.set(current_key, 0)
        redis_connect.set(points_key, 0)

    quiz_start = redis_connect.get(quiz_start_key) == b'True'
    current = int(redis_connect.get(current_key))
    points = int(redis_connect.get(points_key))

    total_questions = int(redis_connect.get("quiz:total_questions"))

    if message.lower() == 'старт':
        redis_connect.set(quiz_start_key, True)
        redis_connect.set(current_key, 0)
        redis_connect.set(points_key, 0)
        question = redis_connect.get(f"quiz:question:1:question").decode("utf-8")
        send_message(
            user_id=user_id,
            message='Викторина началась! Вот первый вопрос:\n' + question,
            keyboard=main_menu_keyboard
        )
    elif message.lower() == 'мои результаты':
        send_message(
            user_id=user_id,
            message=f"Ваш результат: {points}"
        )
    elif quiz_start:
        question_key = f"quiz:question:{current + 1}:question"
        answer_key = f"quiz:question:{current + 1}:answer"

        if redis_connect.exists(question_key):
            answer = redis_connect.get(answer_key).decode("utf-8")

            if message.lower() == 'сдаться':
                current += 1
                if current < total_questions:
                    next_question = redis_connect.get(f"quiz:question:{current + 1}:question").decode("utf-8")
                    send_message(
                        user_id=user_id,
                        message=f'Правильный ответ: {answer}\nСледующий вопрос: {next_question}',
                        keyboard=main_menu_keyboard
                    )
                    redis_connect.set(current_key, current)
                else:
                    send_message(
                        user_id=user_id,
                        message=f'Вопросы закончились\nВаш итоговый результат: {points}',
                        keyboard=main_menu_keyboard
                    )
                    redis_connect.set(quiz_start_key, False)
            elif message.lower() == answer.lower():
                points += 1
                current += 1
                if current < total_questions:
                    next_question = redis_connect.get(f"quiz:question:{current + 1}:question").decode("utf-8")
                    send_message(
                        user_id=user_id,
                        message=f'Ответ верный! Следующий вопрос: {next_question}',
                        keyboard=main_menu_keyboard
                    )
                    redis_connect.set(current_key, current)
                    redis_connect.set(points_key, points)
                else:
                    send_message(
                        user_id=user_id,
                        message=f'Вопросы закончились\nВаш итоговый результат: {points}',
                        keyboard=main_menu_keyboard
                    )
                    redis_connect.set(quiz_start_key, False)
                    redis_connect.set(points_key, points)
            else:
                send_message(
                    user_id=user_id,
                    message='Ответ не верный, попробуйте еще раз',
                    keyboard=main_menu_keyboard
                )
        else:
            send_message(
                user_id=user_id,
                message=f'Вопросы закончились\nВаш итоговый результат: {points}',
                keyboard=main_menu_keyboard
            )
            redis_connect.set(quiz_start_key, False)


def run_vk_bot() -> None:
    logger.info('Start VK bot')
    try:
        for event in VkLongPoll(session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                user_id = event.user_id
                message = event.text.lower()
                open_questions(
                    user_id, message
                )
    except vk_api.exceptions.VkApiError as e:
        logger.error(e)
