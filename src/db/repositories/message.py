"""User repository file."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.structures.role import Role

from ..models import Base, AdminMessage, BroadcastMessage
from .abstract import Repository


class AdminMessageRepo(Repository[AdminMessage]):
    """User repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=AdminMessage, session=session)

    async def new(
        self,
        message_id: int
    ) -> None:
        """Insert a new admin_message into the database.

        :param message_id: Sent message id
        """
        await self.session.merge(
            AdminMessage(
                message_id=message_id,
            )
        )
        await self.session.commit()


class BroadcastMessageRepo(Repository[BroadcastMessage]):
    """User repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=BroadcastMessage, session=session)

    async def new(
        self,
        broadcast_message_id: int,
        user_id: int,
        admin_message_id: int

    ) -> None:
        """Insert a new broadcast_message into the database.

        :param broadcast_message_id: Sent broadcast message id
        :param user_id: User id
        :param admin_message_id: Sent admin message id
        """
        await self.session.merge(
            BroadcastMessage(
                broadcast_message_id=broadcast_message_id,
                user_id=user_id,
                admin_message_id=admin_message_id,
            )
        )
        await self.session.commit()


    async def get_broadcast_message_ids(self, admin_message_id: int):        
        stmt = (
            select(BroadcastMessage)
            .filter(BroadcastMessage.admin_message_id == admin_message_id)
        )
        
        result = await self.session.execute(stmt)
        message_ids = result.scalars().all()
        
        return message_ids