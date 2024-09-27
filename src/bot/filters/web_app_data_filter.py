from aiogram import types
from aiogram.filters import BaseFilter

class IsWebAppData(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return bool(message.web_app_data)