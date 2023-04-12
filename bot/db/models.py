import time

from sqlalchemy import JSON, Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Orders(Base):
    __tablename__ = "orders"

    time = Column(
        Integer,
        default=int(time.time()),
        onupdate=int(time.time()),
        primary_key=True,
        unique=True,
        autoincrement=False,
    )
    data = Column(JSON)


class Counteragents(Base):
    __tablename__ = "counteragents"

    time = Column(
        Integer,
        default=int(time.time()),
        onupdate=int(time.time()),
        primary_key=True,
        unique=True,
        autoincrement=False,
    )
    data = Column(JSON)
