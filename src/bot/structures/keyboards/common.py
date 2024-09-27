from aiogram import types


def show_keyboard():
    kb = [
        [types.InlineKeyboardButton(text="Do'kon", web_app=types.WebAppInfo(url='https://alolabot-web.vercel.app/'))],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)

    return keyboard

def send_contact():
    kb = [
        [types.KeyboardButton(text="Yuborish", request_contact=True)],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard
