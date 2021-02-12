from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_subscribe = KeyboardButton('Подписаться! 👋')


greet_kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(button_subscribe)


