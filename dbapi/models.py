import enum

from datetime import datetime, UTC
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated

from database import Base


intpk = Annotated[int, mapped_column(primary_key=True)]
utc_created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
utc_updated_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.now(UTC))]


class GenderEnum(enum.Enum):
    non_binary = "non_binary"
    female = "female"
    male = "male"


class FormsOrm(Base):
    __tablename__ = "forms"

    form_id: Mapped[intpk]
    user_id: Mapped[str] = mapped_column(unique=True)
    lat: Mapped[float]
    long: Mapped[float]
    goal: Mapped[str] # enum
    city: Mapped[str] # enum
    gender: Mapped[str] # enum
    preference: Mapped[str] # enum
    name: Mapped[str]
    age: Mapped[int]
    description: Mapped[str]
    first_photo_id: Mapped[str]
    second_photo_id: Mapped[str | None]
    third_photo_id: Mapped[str | None]
    utc_created_at: Mapped[utc_created_at]
    utc_updated_at: Mapped[utc_updated_at]


class Likes(Base):
    __tablename__ = "likes"

    like_id: Mapped[intpk]
    user_id_from: Mapped[str] = mapped_column(ForeignKey("forms.user_id", ondelete="CASCADE"), unique=True)
    user_id_to: Mapped[str] = mapped_column(ForeignKey("forms.user_id", ondelete="CASCADE"),  unique=True)
    is_like: Mapped[bool] # enum
    utc_created_at: Mapped[utc_created_at]
    utc_updated_at: Mapped[utc_updated_at]
    

class Matches(Base):
    __tablename__ = "matches"

    match_id: Mapped[intpk]
    user_id_1: Mapped[str] = mapped_column(ForeignKey("forms.user_id"),  unique=True)
    user_id_2: Mapped[str] = mapped_column(ForeignKey("forms.user_id"),  unique=True)
    utc_created_at: Mapped[utc_created_at]
    utc_updated_at: Mapped[utc_updated_at]
