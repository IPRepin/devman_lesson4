import logging
import os

import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from misc.open_quiz import get_quiz_data_vk
from vk_bot.vk_keyboard import main_menu_keyboard


def send_message(user_id, message, keyboard=None):
    post = {
        'user_id': user_id,
        'message': message,
        'random_id': 0,
    }
    if keyboard is not None:
        post['keyboard'] = keyboard.get_keyboard()
    session.method('messages.send', post)


def vk_hendler(
        question: str,
        answer: str,
        current: int,
        points: int,
        quiz_start: bool,
        user_id: int,
        message: str,
) -> None:
    if message == 'старт':
        send_message(
            user_id=user_id,
            message='Викторина началась! Вот первый вопрос:\n' + question[current],
            keyboard=main_menu_keyboard
        )
    elif message == 'мои результаты':
        send_message(
            user_id=user_id,
            message=f"Ваш результат: {points}"
        )
    elif quiz_start:
        if message.lower() == 'сдаться':
            current += 1
            if current < len(question):
                send_message(
                    user_id=user_id,
                    message='Правильный ответ: ' + answer[
                        current - 1] + '\nСледующий вопрос: ' +
                            question[current], keyboard=main_menu_keyboard
                )
            else:
                send_message(
                    user_id=user_id,
                    message='Вопросы закончились\nВаш итоговый результат: ' + str(points),
                    keyboard=main_menu_keyboard
                )
        elif message.lower() == answer[current].lower():
            points += 1
            current += 1
            if current < len(question):
                send_message(
                    user_id=user_id,
                    message='Ответ верный! Следующий вопрос: ' + question[current],
                    keyboard=main_menu_keyboard
                )
            else:
                send_message(
                    user_id=user_id,
                    message='Вопросы закончились\nВаш итоговый результат: ' + str(points),
                    keyboard=main_menu_keyboard
                )

        else:
            send_message(
                user_id=user_id,
                message='Ответ не верный, попробуйте еще раз',
                keyboard=main_menu_keyboard
            )


def main() -> None:
    logger.info('Start VK bot')
    try:
        for event in VkLongPoll(session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                user_id = event.user_id
                message = event.text.lower()
                vk_hendler(
                    questions,
                    answers,
                    current_question,
                    score, quiz_started,
                    user_id, message
                )
    except vk_api.exceptions.VkApiError as e:
        logger.error(e)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    quiz_started = True
    current_question = 0
    score = 0
    questions, answers = get_quiz_data_vk()
    load_dotenv()
    session = vk_api.VkApi(token=os.getenv("VK_TOKEN"))
    main()
