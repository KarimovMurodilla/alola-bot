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

    # billz = BillzAPI()
    
    # user = billz.get_user()
    await message.answer(
        f"Assalomu aleykum {message.from_user.first_name}, Alola botiga hush kelibsiz!\n\n"
        "Botdan foydalanish uchun telefon raqamingizni yuboring",
        reply_markup=common.send_contact(),
        parse_mode=None
    )
    await state.set_state(RegisterGroup.phone_number)


@start_router.message(F.contact, RegisterGroup.phone_number)
async def start_handler(message: types.Message, db: Database, translator: LocalizedTranslator, state: FSMContext):
    """Start command handler."""
    await state.clear()

    msg = await message.answer('.', reply_markup=types.ReplyKeyboardRemove())
    await msg.delete()

    await message.answer(
        f"Saqlandi ✅",
        reply_markup=common.show_keyboard(),
        parse_mode=None
    )

@start_router.message(IsWebAppData())
async def check_data_handler(message: types.Message):
    # data = json.loads(message.web_app_data.data)
    data = message.web_app_data.data
    await message.answer(data)
    # print(data)
    # order_id = random.randint(1000, 9999)
    # color_and_count = ''.join([f"\n - {color['color']} - {color['count']}" for color in data['colors']])

    # for admin in conf.ADMINS:
    #     await message.bot.send_message(
    #         chat_id=admin,
    #         text =  f"Заказ #{order_id}\n"
    #                 f"Наименование товара: {data['product_name']}\n"
    #                 f"Цвет и количество: {color_and_count}\n"
    #                 f"Общее количество: {data['count_products']}\n"
    #                 f"Общая сумма: {data['amount']}"
    #     )
    # await message.answer(f"Sizning buyurtmangiz qabul qilindi ✅")

