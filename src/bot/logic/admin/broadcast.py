import asyncio
import logging

from aiogram import Bot, exceptions, types
from sqlalchemy.ext.asyncio import AsyncSession

from src.configuration import conf
from src.db.database import Database
from src.db.database import create_async_engine
from src.configuration import conf

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')

bot = Bot(token=conf.bot.token)
engine = create_async_engine(
    url=conf.db.build_connection_str()
)


async def get_users():
    """
    Return users list

    In this example returns some random ID's
    """
    async with AsyncSession(engine) as session:
        db = Database(session)

        result = await db.user.get_all_users()
        users = [user.user_id for user in result]
        return users


async def send_message(user_id: int, message: types.Message, disable_notification: bool = False) -> bool:
    """
    Safe messages sender

    :param user_id:
    :param message:
    :param disable_notification:
    :return:
    """
    try:
        await bot.copy_message(
            chat_id=user_id, 
            from_chat_id=message.from_user.id,
            message_id=message.message_id,
            disable_notification=disable_notification
        )
    except exceptions.TelegramForbiddenError:
        log.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.TelegramNotFound:
        log.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.TelegramRetryAfter as e:
        log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds.")
        await asyncio.sleep(e.retry_after)
        return await bot.send_message(user_id, message)  # Recursive call
    except exceptions.TelegramBadRequest as tbr:
        print(tbr)
        log.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{user_id}]: failed")
    else:
        log.info(f"Target [ID:{user_id}]: success")
        return True
    finally:
        await bot.session.close()
    return False


async def broadcaster(message: types.Message) -> int:
    """
    Simple broadcaster

    :return: Count of messages
    """
    count = 0
    try:
        users = await get_users()
        for user_id in users:
            if await send_message(user_id, message):
                count += 1
            await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
    finally:
        log.info(f"{count} messages successful sent.")

    return count