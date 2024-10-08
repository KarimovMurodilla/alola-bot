"""User model file."""
import datetime
from typing import Annotated, Optional
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped, mapped_column

from src.bot.structures.role import Role

from .base import Base


class AdminMessage(Base):
    """AdminMessage model."""

    message_id: Mapped[int] = mapped_column(
        sa.BigInteger, unique=True, nullable=False, primary_key=True
    )
    created_at: Mapped[Optional[Annotated[
        datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)
    ]]]
    def __str__(self):
        return f"{self.message_id}"


class BroadcastMessage(Base):
    """AdminMessage model."""
    broadcast_message_id: Mapped[int] = mapped_column(
        sa.BigInteger, unique=True, nullable=False, primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        sa.BigInteger, unique=False, nullable=False
    )
    admin_message_id: Mapped[int] = mapped_column(
        sa.ForeignKey('adminmessage.message_id', ondelete='CASCADE'),
        unique=False,
        nullable=False
    )
    created_at: Mapped[Optional[Annotated[
        datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)
    ]]]
    def __str__(self):
        return f"{self.broadcast_message_id}"
