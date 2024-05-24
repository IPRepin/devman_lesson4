import re

import redis

from config import FILE_PATH


def read_quiz_file(redis_connect: redis.Redis) -> None:
    with open(FILE_PATH, 'r', encoding="KOI8-R") as file:
        data = file.read()
    matches = re.findall(r"Вопрос \d+:.*?Ответ:.*?(?:Автор:|Источник:|$)", data, re.DOTALL)
    for index, match in enumerate(matches):
        question_match = re.search(r"Вопрос \d+:(.*?)Ответ:", match, re.DOTALL)
        answer_match = re.search(r"Ответ:(.*?)(?:Автор:|Источник:|$)", match, re.DOTALL)
        if question_match and answer_match:
            question = question_match.group(1).strip()
            answer = answer_match.group(1).strip()
            redis_connect.set(f"quiz:question:{index + 1}:question", question)
            redis_connect.set(f"quiz:question:{index + 1}:answer", answer)
    redis_connect.set("quiz:total_questions", len(matches))
