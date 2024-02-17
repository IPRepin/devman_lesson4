from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Новый вопрос'),
        KeyboardButton(text='Сдаться')
    ],
    [
        KeyboardButton(text='Мой счет')
    ]
], resize_keyboard=True,
)
