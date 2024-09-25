"""This file represents a start logic."""

from sqlalchemy.exc import IntegrityError
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from src.db.database import Database
from src.language.translator import LocalizedTranslator
from src.bot.structures.keyboards import common

start_router = Router(name='start')


@start_router.message(CommandStart())
async def start_handler(message: types.Message, db: Database, translator: LocalizedTranslator, state: FSMContext):
    """Start command handler."""
    await state.clear()

    await message.answer(
        f"Assalomu aleykum {message.from_user.first_name}, Alola botiga hush kelibsiz!",
        reply_markup=common.show_keyboard()
    )
