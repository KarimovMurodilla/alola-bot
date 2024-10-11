from aiogram import F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.utils.billz_api import BillzAPI
from src.db.database import Database
from src.bot.structures.keyboards import common
from src.bot.structures.fsm.admin_states import AdminStatesGroup
from src.configuration import conf

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

    for user in message.users_shared.users:
        if not await db.user.get_me(user.user_id):
            await db.user.new(
                user_id=user.user_id,
                user_name=user.username,
                first_name=user.first_name,
            )
    await message.answer("Клиенты добавлены в базу! Теперь они могут пользоваться ботом ✅")


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


@admin_router.message(F.text == '➖ Удалить клиента')
async def delete_client_cmd(
    message: Message
):
    await message.answer(
        "Нажав на кнопку, выберите клиента",
        reply_markup=common.show_users_inline()
    )
    

@admin_router.inline_query(F.query == 'clients')
async def show_clients(inline_query: types.InlineQuery, db: Database):
    if inline_query.from_user.id not in conf.ADMINS:
        return
    
    clients = await db.user.get_all_users()
    
    results = []
    for client in clients:
        results.append(types.InlineQueryResultArticle(
            id=str(client.user_id),
            title=f"{client.first_name} - {client.phone_number}",
            description=f"@{client.user_name}",
            input_message_content=types.InputTextMessageContent(
                message_text=f"Данные о клиенте\n\n"
                             f"- Имя: {client.first_name}\n"
                             f"- Телефон: {client.phone_number}\n"
                             f"- Телеграм аккаунт: @{client.user_name}",
                parse_mode=None
            ),
            reply_markup=common.delete(client.user_id)
        ))

    await inline_query.answer(results, is_personal=True, cache_time=0)


@admin_router.callback_query(F.data == 'cancel')
async def order_cancel(c: types.CallbackQuery):    
    # if c.data == 'cancel':
    old_text = c.message.text
    new_text = old_text.replace('🟡 Проверяется', '🔴 Отменён')
    await c.message.edit_text(new_text, reply_markup=None)
    

@admin_router.callback_query(F.data.contains('confirm'))
async def order_confirm(c: types.CallbackQuery): 
    data = c.data.split(',')
    order_id = data[1]
    total_amount = int(data[2])

    billz = BillzAPI()
    # await billz.make_payment(order_id, total_amount)
    old_text = c.message.text
    new_text = old_text.replace('🟡 Проверяется', '🟢 Подтверждён')
    await c.message.edit_text(new_text, reply_markup=None)


@admin_router.callback_query(F.data.contains('delete'))
async def order_confirm(c: types.CallbackQuery, db: Database):
    await c.answer()
    data = c.data.split(',')
    user_id = int(data[1])

    bot = Bot(token=conf.bot.token)

    if await db.user.get_me(user_id):
        await db.user.delete_one(user_id = user_id)
        await bot.set_chat_menu_button(user_id, menu_button=types.MenuButtonDefault())
        msg = await bot.send_message(user_id, '.', reply_markup=types.ReplyKeyboardRemove())
        await msg.delete()
    else:
        return await bot.send_message(c.from_user.id, "Такого клиента на базе не существует 🤷‍♂️")

    await bot.send_message(c.from_user.id, "Клиент удалён из базы. Теперь он не может пользоваться ботом ⛔️")
    await bot.session.close()