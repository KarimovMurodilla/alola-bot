"""User model file."""
import datetime
from typing import Annotated, Optional
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped, mapped_column

from src.bot.structures.role import Role

from .base import Base
from ...language.enums import Locales


class User(Base):
    """User model."""

    user_id: Mapped[int] = mapped_column(
        sa.BigInteger, unique=True, nullable=False, primary_key=True
    )
    """ Telegram user id """
    user_name: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    """ Telegram user name """
    first_name: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    """ Telegram profile first name """
    second_name: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    language_code: Mapped[Locales] = mapped_column(sa.Enum(Locales), unique=False, nullable=True)
    """ Telegram profile second name """
    is_premium: Mapped[bool] = mapped_column(
        sa.Boolean, unique=False, nullable=False
    )
    """ Telegram user premium status """
    role: Mapped[Role] = mapped_column(sa.Enum(Role), default=Role.USER)
    created_at: Mapped[Optional[Annotated[datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)]]]

    def __str__(self):
        return f"{self.first_name}"
