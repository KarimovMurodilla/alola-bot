from sqlalchemy.exc import IntegrityError

from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.cache import Cache
from src.db.database import Database
from src.bot.filters.admin_filter import AdminFilter
from src.language.translator import LocaleScheme, LocalizedTranslator
from .router import admin_router


@admin_router.message(F.text=='/admin', AdminFilter())
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
    cache: Cache
):
    await message.answer(
        "Welcome to admin panel"
    )
