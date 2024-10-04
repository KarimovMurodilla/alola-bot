from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.db.database import Database
from src.bot.filters.admin_filter import AdminFilter
from src.bot.structures.keyboards import common
from src.bot.structures.fsm.admin_states import AdminStatesGroup
from .router import admin_router
from .broadcast import broadcaster


@admin_router.message(F.text=='/admin', AdminFilter())
async def process_registration(
    message: Message, 
    state: FSMContext,
    db: Database
):
    await message.answer(
        "Добро пожаловать в админ-панель!",
        reply_markup=common.show_admin_buttons()
    )


@admin_router.message(F.users_shared, AdminFilter())
async def process_registration(
    message: Message, 
    state: FSMContext, 
    db: Database
):
    for user in message.users_shared.users:
        if not await db.user.get_me(user.user_id):
            await db.user.new(
                user_id=user.user_id,
                user_name=user.username,
                first_name=user.first_name,
            )
    await message.answer("Клиенты добавлены в базу! Теперь они могут пользоваться ботом ✅")


@admin_router.message(F.text=='Завершить', AdminFilter())
async def process_registration(
    message: Message, 
    state: FSMContext,
    db: Database
):
    await state.clear()
    await message.answer("Завершено!", reply_markup=common.show_admin_buttons())


@admin_router.message(F.text=='Рассылка', AdminFilter())
async def process_registration(
    message: Message, 
    state: FSMContext,
    db: Database
):
    await message.answer(
        "Отправьте сообщение для рассылки",
        reply_markup=common.cancel()
    )

    await state.set_state(AdminStatesGroup.broadcast)


@admin_router.message(AdminStatesGroup.broadcast, AdminFilter())
async def process_registration(
    message: Message, 
    state: FSMContext,
    db: Database
):
    count = await broadcaster(message)
    await message.answer(
        f"Отправлено к {count} клиентам",
        reply_markup=common.cancel()
    )
