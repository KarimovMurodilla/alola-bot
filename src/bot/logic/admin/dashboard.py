from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.db.database import Database
from src.bot.structures.keyboards import common
from src.bot.structures.fsm.admin_states import AdminStatesGroup
from .router import admin_router
from .broadcast import broadcaster, cleaner


@admin_router.message(F.text=='/admin')
async def process_registration(
    message: Message, 
    state: FSMContext,
    db: Database
):
    await message.answer(
        "Добро пожаловать в админ-панель!",
        reply_markup=common.show_admin_buttons()
    )


@admin_router.message(F.users_shared)
async def process_registration(
    message: Message, 
    state: FSMContext, 
    db: Database
):
    request_id = message.users_shared.request_id

    if request_id == 1:
        for user in message.users_shared.users:
            if not await db.user.get_me(user.user_id):
                await db.user.new(
                    user_id=user.user_id,
                    user_name=user.username,
                    first_name=user.first_name,
                )
        await message.answer("Клиенты добавлены в базу! Теперь они могут пользоваться ботом ✅")

    elif request_id == 2:
        for user in message.users_shared.users:
            if await db.user.get_me(user.user_id):
                await db.user.delete_one(user_id = user.user_id)
                await message.bot.set_chat_menu_button(user.user_id, menu_button=types.MenuButtonDefault())
                msg = await message.bot.send_message(user.user_id, '.', reply_markup=types.ReplyKeyboardRemove())
                await msg.delete()
            else:
                return await message.answer("Такого клиента на базе не существует 🤷‍♂️")

        await message.answer("Клиент удален из базы. Теперь он не может пользоваться ботом ⛔️")

@admin_router.message(F.text=='Завершить')
async def process_registration(
    message: Message, 
    state: FSMContext,
    db: Database
):
    await state.clear()
    await message.answer("Завершено!", reply_markup=common.show_admin_buttons())


@admin_router.message(F.text == '!delete')
async def handle_delete(message: Message, db: Database):
    target_message = message.reply_to_message

    if not target_message:
        return await message.answer("Укажите сообщение")
    
    messages = await db.broadcast_message.get_broadcast_message_ids(target_message.message_id)
    
    if messages:
        await cleaner(messages)

        await message.answer(
            f"Рассылка удалена 🧹",
            reply_markup=common.cancel()
        )
    else:
        await message.answer("Указанное сообщение не рассылался клиентам!")

@admin_router.message(F.text=='Рассылка')
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


@admin_router.message(AdminStatesGroup.broadcast)
async def process_registration(
    message: Message, 
    state: FSMContext,
    db: Database
):
    await db.admin_message.new(message_id=message.message_id)
    count = await broadcaster(message)
    await message.answer(
        f"Отправлено к {count} клиентам 🚀",
        reply_markup=common.cancel()
    )
