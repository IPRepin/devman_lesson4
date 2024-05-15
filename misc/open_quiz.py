import re


def read_quiz_file() -> list:
    with open("misc/quiz.txt", 'r', encoding="KOI8-R") as file:
        data = file.read()
    matches = re.findall(r"Вопрос \d+:.*?Ответ:.*?(?:Автор:|Источник:|$)", data, re.DOTALL)
    result = []
    for match in matches:
        question_match = re.search(r"Вопрос \d+:(.*?)Ответ:", match, re.DOTALL)
        answer_match = re.search(r"Ответ:(.*?)(?:Автор:|Источник:|$)", match, re.DOTALL)
        if question_match and answer_match:
            question = question_match.group(1).strip()
            answer = answer_match.group(1).strip()
            result.append({"Вопрос": question, "Ответ": answer})
    return result


def get_quiz_data_vk():
    questions = []
    answers = []

    with open("misc/quiz.txt", 'r', encoding="KOI8-R") as file:
        data = file.read().split('\n\n')
        for item in data:
            if item.startswith('Вопрос'):
                questions.append(item[8:])
            elif item.startswith('Ответ'):
                answers.append(item[7:])

    return questions, answers
