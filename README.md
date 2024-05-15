# Бот знакомств для Telegram с функцией сбора данных (анкет) пользователей. #
# Version 0.4 #

![Static Badge](https://img.shields.io/badge/Python-3.11-blue)
![Static Badge](https://img.shields.io/badge/Aiogram-3.3.0-blue)
![Static Badge](https://img.shields.io/badge/Opencv--python-4.9.0.80-blue)
![Static Badge](https://img.shields.io/badge/urllib3-2.2-blue)
![Static Badge](https://img.shields.io/badge/Vk_api-3.45.2-blue)
![Static Badge](https://img.shields.io/badge/Redis-5.0.3-blue)


## Описание проекта ##

Бот для Telegram и ВК викторина для пользователей.
Чат-бот с каверзными вопросами и единственным правильным вариантом ответа. За каждый правильный ответ добавляется 1 бал.
Есть возможность сдаться если не знаешь ответа на вопрос. Бот отправляет логи о своей работе в телеграм.




## Требования к окружению ##

* Python==3.11, 
* aiogram==3.3.0, 
* python-dotenv==1.0.0,
* urllib3==2.2.1
* Vk_api-3.45.2
* redis==5.0.3

## Структура проекта ##

📦devman_lesson4
 * ┣ 📦data _(пакет модулей для работы с БД)_
 * ┣ 📦handlers _(пакет работы с hendlrs бота)_
 * ┣ 📦keyboards _(пакет работы с клавиатурами бота)_
 * ┣ 📦misc _(вспомогательный пакет с дополнительными модулями)_
 * ┣ 📦vk_bot _(вспомогательный пакет с дополнительными модулями)_
 * ┣ 📜bot.py _(модуль запуска телеграм бота)_
 * ┣ 📜.gitignore
 * ┗ 📜requirements.txt

## Как установить ##

1. Создаем бота в телеграм при помощи [BotFather](https://t.me/BotFather)
2. Для вконтакте создаем группу во вкладке [управление](https://vk.com/groups?tab=admin)
   * В Настройках группы в пункте "Работа с API" создаем ключ доступа
   
   ![screenshot_from_2019-04-29_20-10-16](https://github.com/IPRepin/devnan_support_bot/assets/76727704/4a9487c8-8723-4e9a-a3e9-bffb6067f827)

   * В пункте Сообщения --> Настройки для бота Разрешаем боту отправку сообщений
   
   ![screenshot_from_2019-04-29_20-15-54](https://github.com/IPRepin/devnan_support_bot/assets/76727704/538055b5-77be-4ddc-8a5b-b3e3b4762bcf)

3. Скачиваем репозиторий с ботом при помощи команды: 
   * `git clone https://github.com/IPRepin/devman_lesson4.git`
4. Устанавливаем библиотеки из файла [requirements.txt](https://github.com/IPRepin/devman_lesson4.git/requirements.txt)
5. В корневой папке проекта содаем файл с именем  `.env`
6. Помещаем в него:
    * Токен API ВКонтакте `VK_TOKEN='Ваш_токен_ВКонтакте'`
    * Токен Telegram для бота `TELEGRAM_TOKEN='Ваш_телеграмм_токен'`
    * Токен Telegram для отправки сообщений о ошибках `TELEGRAM_LOGS_TOKEN='Телеграмм_токен_бота_сообщений_о_ошибках'`
    * Chat id Телеграм бота сообщений о ошибках `TG_CHAT_ID='Ваш_chat_id_бота_сообщений_о_ошибках'`


## Запуск бота Телеграм ##
`python bot.py`

## Пример работы Телеграм бота ##
Работающего телеграм бота можно посмотреть [тут](https://t.me/devman_sup_bot)

## Запуск бота ВКонтакте ##
`python vk_bot/vk_bot.py`
