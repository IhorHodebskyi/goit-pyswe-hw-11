from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    birthday: Mapped[str] = mapped_column(Date, nullable=True)
    additional_data: Mapped[str] = mapped_column(Text, nullable=True)


