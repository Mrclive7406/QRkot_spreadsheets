from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: int = Column(Integer, primary_key=True)
    invested_amount: int = Column(Integer, default=0)
    fully_invested: bool = Column(Boolean, default=False)
    create_date: datetime = Column(DateTime, default=datetime.now)
    close_date: datetime | None = Column(DateTime, nullable=True)


Base = declarative_base(cls=PreBase)
engine = create_async_engine(settings.database_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as async_session:
        yield async_session