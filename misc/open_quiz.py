import re


def read_quiz_file():
    # Открываем файл и читаем его
    with open("quiz.txt", 'r', encoding="KOI8-R") as file:
        data = file.read()
    # Используем регулярные выражения для извлечения данных вопросов и ответов
    matches = re.findall(r'Вопрос \d+:.*?Ответ:.*?(?:Автор:|Источник:|$)', data, re.DOTALL)
    # Создаем список словарей с данными вопросов и ответов
    result = []
    for match in matches:
        question_match = re.search(r'Вопрос \d+:(.*?)Ответ:', match, re.DOTALL)
        answer_match = re.search(r'Ответ:(.*?)(?:Автор:|Источник:|$)', match, re.DOTALL)
        if question_match and answer_match:
            question = question_match.group(1).strip()
            answer = answer_match.group(1).strip()
            result.append({"Вопрос": question, "Ответ": answer})
    # Выводим полученные данные
    return result


def next_question():
    '''
    TODO Создать функцию итератора, которая будет возвращать следующий вопрос
    '''
    questions = read_quiz_file()
    for question in questions:
        print(question)


next_question()
