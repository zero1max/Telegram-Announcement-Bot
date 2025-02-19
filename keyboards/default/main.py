from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Sherik kerak'), KeyboardButton(text='Ish joyi kerak')],
        [KeyboardButton(text='Hodim kerak'), KeyboardButton(text='Ustoz kerak')],
        [KeyboardButton(text='Shogird kerak')]
    ]
)