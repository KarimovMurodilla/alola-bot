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
from src.configuration import conf
from src.bot.utils.billz_api import BillzAPI

start_router = Router(name='start')


@start_router.message(CommandStart())
async def start_handler(message: types.Message, db: Database, translator: LocalizedTranslator, state: FSMContext):
    """Start command handler."""
    await state.clear()

    billz = BillzAPI()
    user: dict = await billz.get_user(message.from_user.id)
    
    if not user.get('clients'):
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

@start_router.message(F.contact, RegisterGroup.phone_number)
async def start_handler(message: types.Message, db: Database, translator: LocalizedTranslator, state: FSMContext):
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

    await state.clear()

@start_router.message(IsWebAppData())
async def check_data_handler(message: types.Message):
    data = json.loads(message.web_app_data.data)
    billz = BillzAPI()

    result = "Заказ - #1234\n\n"

    for product in data['products']:
        name = f"Наименование товара: {product['product_name']}\n"
        amount = f"Общая сумма: {product['amount']}\n"
        colors = "".join([f"• {data['color']} - {data['count']}\n" for data in product['colors']])
        product_count = sum([data['count'] for data in product['colors']])

        result += name
        result += f"Цвет и количество:\n{colors}"
        result += f"Общее количество: {product_count}\n"
        result += amount

        for i in product['colors']:
            await billz.add_item(data['order_id'], i['product_id'], i['count'])

    await message.bot.send_message(
        chat_id=conf.CHAT_ID,  
        text=result,
        reply_markup=common.show_approve_btn(order_id=data['order_id'])
    )
    await message.answer(f"Sizning buyurtmangiz qabul qilindi ✅")
    
