from sqlalchemy import Column, Integer, String, Date, Text
from db import Base, engine


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), index=True, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    birthday = Column(Date, nullable=True)
    additional_data = Column(Text, nullable=True)


Base.metadata.create_all(bind=engine)
