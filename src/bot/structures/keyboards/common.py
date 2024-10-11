from aiogram import types


# def show_keyboard():
#     kb = [
#         [types.InlineKeyboardButton(text="Do'kon", web_app=types.WebAppInfo(url='https://alolabot-web.vercel.app/'))],
#     ]
#     keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)

#     return keyboard

def show_keyboard(user_id: int):
    kb = [
        [types.KeyboardButton(text="Do'kon", web_app=types.WebAppInfo(url=f'https://alola.uzvip.uz/{user_id}'))],
        [types.KeyboardButton(text="Murojaat")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard

def send_contact():
    kb = [
        [types.KeyboardButton(text="Yuborish", request_contact=True)],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard

def show_approve_btn(order_id: str, total_amount: str):
    kb = [
        [types.InlineKeyboardButton(text="❌ Отменить", callback_data='cancel'),
        types.InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"confirm,{order_id},{total_amount}")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)

    return keyboard

def show_admin_buttons():
    kb = [
        [
            types.KeyboardButton(text="➕ Добавить клиента", request_users=types.KeyboardButtonRequestUsers(
                    request_id=1, user_is_bot=False, request_username=True, request_name=True, max_quantity=10
                )
            )
        ],
        [
            types.KeyboardButton(text="➖ Удалить клиента")
        ],
        [types.KeyboardButton(text="Рассылка")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard

def show_users_inline():
    kb = [
        [types.InlineKeyboardButton(text="Клиенты", switch_inline_query_current_chat='clients')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)

    return keyboard

def delete(user_id: int):
    kb = [
        [types.InlineKeyboardButton(text="Удалить", callback_data=f'delete,{user_id}')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)

    return keyboard

def cancel():
    kb = [
        [types.KeyboardButton(text="Завершить")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard
