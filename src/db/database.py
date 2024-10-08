"""Database class with all-in-one features."""

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine

from src.configuration import conf

from .repositories import (
    UserRepo, AdminMessageRepo, BroadcastMessageRepo
)


def create_async_engine(url: URL | str) -> AsyncEngine:
    """Create async engine with given URL.

    :param url: URL to connect
    :return: AsyncEngine
    """
    return _create_async_engine(url=url, echo=conf.debug, pool_pre_ping=True, connect_args={"prepared_statement_cache_size": 0})


class Database:
    """Database class.

    is the highest abstraction level of database and
    can be used in the handlers or any others bot-side functions.
    """

    user: UserRepo
    admin_message: AdminMessageRepo
    broadcast_message: BroadcastMessageRepo

    session: AsyncSession

    def __init__(
        self,
        session: AsyncSession,
        user: UserRepo = None,
        admin_message: AdminMessageRepo = None,
        broadcast_message: BroadcastMessageRepo = None,
    ):
        """Initialize Database class.

        :param session: AsyncSession to use
        """
        self.session = session
        self.user = user or UserRepo(session=session)
        self.admin_message = admin_message or AdminMessageRepo(session=session)
        self.broadcast_message = broadcast_message or BroadcastMessageRepo(session=session)
