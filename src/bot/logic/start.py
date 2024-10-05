"""This file represents a start logic."""

import random
import json

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from src.db.database import Database
from src.language.translator import LocalizedTranslator
from src.bot.structures.keyboards import common
from src.bot.structures.fsm.registration import RegisterGroup
from src.bot.filters.web_app_data_filter import IsWebAppData
from src.bot.filters.client_filter import ClientFilter
from src.configuration import conf
from src.bot.utils.billz_api import BillzAPI

start_router = Router(name='start')


@start_router.message(CommandStart(), ClientFilter())
async def start_handler(message: types.Message, state: FSMContext):
    """Start command handler."""
    await state.clear()

    billz = BillzAPI()
    user: dict = await billz.get_user(message.from_user.id)
    
    if not user:
        await message.answer(
            f"Assalomu aleykum {message.from_user.first_name}, Alola botiga hush kelibsiz!\n\n"
            "Botdan foydalanish uchun telefon raqamingizni yuboring",
            reply_markup=common.send_contact(),
            parse_mode=None
        )
        await state.set_state(RegisterGroup.phone_number)
    else:
        await message.answer(
            f"Assalomu aleykum {message.from_user.first_name}, Alola botiga hush kelibsiz!",
            reply_markup=common.show_keyboard(user_id=message.from_user.id),
            parse_mode=None
        )
        await message.bot.set_chat_menu_button(
            chat_id=message.from_user.id, 
            menu_button=types.MenuButtonWebApp(text="Do'kon", web_app=types.WebAppInfo(
                url=f'https://alolabot-web.vercel.app/{message.from_user.id}'
            ))
        )


@start_router.message(F.contact, RegisterGroup.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    msg = await message.answer('.', reply_markup=types.ReplyKeyboardRemove())
    await msg.delete()

    billz = BillzAPI()

    await billz.set_user(
        chat_id=str(message.from_user.id),
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        phone_number=message.contact.phone_number
    )

    await message.answer(
        f"Saqlandi ✅",
        reply_markup=common.show_keyboard(user_id=message.from_user.id),
        parse_mode=None
    )

    await message.bot.set_chat_menu_button(
        chat_id=message.from_user.id, 
        menu_button=types.MenuButtonWebApp(text="Do'kon", web_app=types.WebAppInfo(
            url=f'https://alolabot-web.vercel.app/{message.from_user.id}'
        ))
    )

    await state.clear()


@start_router.message(IsWebAppData(), ClientFilter())
async def check_data_handler(message: types.Message):
    data = json.loads(message.web_app_data.data)
    
    billz = BillzAPI()
    client = await billz.get_user(message.from_user.id)

    result = ""
    client_result = ""
    status = "Статус: 🟡 Проверяется\n\n"
    client_data = f"Клиент:\n- Имя: {client['first_name']}\n- Телефон: {client['phone_numbers'][0]}\n\n"

    msg1 = "Ваш заказ отправлен на проверку\n\n"
    details = "Детали заказа:\n"

    result += status
    result += client_data

    client_result += msg1
    client_result += details

    total_amount = 0
    total_count = 0

    for product in data['products']:
        colors = "".join([f"• {data['color']} - {data['count']}\n" for data in product['colors']])
        product_count = sum([data['count'] for data in product['colors']])

        result += f"{product['product_name']}\n"
        result += f"{colors}\n"

        client_result += f"{product['product_name']}\n"
        client_result += f"{colors}\n"

        total_amount += product['amount']
        total_count += product_count

        for i in product['colors']:
            await billz.add_item(data['order_id'], i['product_id'], i['count'])

    formatted_price = f"{total_amount:,}".replace(",", " ")
    result += f"Общее количество: {total_count}\n"
    result += f"Общая сумма: {formatted_price}"

    client_result += f"Общее количество: {total_count}\n"
    client_result += f"Общая сумма: {formatted_price}"

    await message.bot.send_message(
        chat_id=conf.CHAT_ID,  
        text=result,
        reply_markup=common.show_approve_btn(order_id=data['order_id'], total_amount=total_amount)
    ) # Gruppaga boradigani
    await message.answer(client_result) # Klientga boradigani
    

@start_router.callback_query(ClientFilter())
async def order_complete(c: types.CallbackQuery):    
    if c.data == 'cancel':
        old_text = c.message.text
        new_text = old_text.replace('🟡 Проверяется', '🔴 Отменён')
        await c.message.edit_text(new_text, reply_markup=None)
    
    else:
        data = c.data.split(',')
        order_id = data[0]
        total_amount = int(data[1])

        billz = BillzAPI()
        # await billz.make_payment(order_id, total_amount)
        old_text = c.message.text
        new_text = old_text.replace('🟡 Проверяется', '🟢 Подтверждён')
        await c.message.edit_text(new_text, reply_markup=None)
