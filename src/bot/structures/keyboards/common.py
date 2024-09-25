from aiogram import types


def show_keyboard():
    kb = [
        [types.KeyboardButton(text="Do'kon", web_app=types.WebAppInfo(url='https://alola.uzvip.uz'))],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard
