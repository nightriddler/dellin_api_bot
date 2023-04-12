from typing import Generic, Type, TypeVar

import api
from db.models import Base, Counteragents, Orders
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=Base)


class Repository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def get(self, session: AsyncSession) -> ModelType | None:
        """Получить запись из БД."""
        stmt = await session.execute(select(self._model))
        instance = stmt.scalars().first()
        return instance

    async def create(self, session: AsyncSession, **kwargs) -> ModelType | None:
        """Создать в БД запись."""
        instance = self._model(**kwargs)
        session.add(instance)
        await session.commit()
        return instance

    async def update(self, session: AsyncSession, instance):
        """Обновить запись из БД."""
        await session.commit()

    async def get_or_create(self, session: AsyncSession):
        """Получить или создать в БД запись."""
        instance = await self.get(session)
        return instance if instance else await self.create(session)

    async def create_or_update(self, session: AsyncSession):
        """Создать или обновить в БД запись о заказах."""
        instance = await self.get(session)
        await self.update(session, instance) if instance else await self.create(session)


class RepositoryApiOrders(Repository):
    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def create(self, session: AsyncSession, **kwargs) -> ModelType | None:
        """Создать в БД запись."""
        data = api.dl.get_orders()
        return await super().create(session, data=data)

    async def update(self, session: AsyncSession, instance):
        """Обновить запись из БД."""
        response = api.dl.get_orders()
        instance.data = response
        await session.commit()


class RepositoryApiCounteragents(Repository):
    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def create(self, session: AsyncSession, **kwargs) -> ModelType | None:
        """Создать в БД запись."""
        data = api.dl.get_counteragents()
        return await super().create(session, data=data)

    async def update(self, session: AsyncSession, instance):
        """Обновить запись из БД."""
        instance.data = api.dl.get_counteragents()
        await session.commit()


order_crud = RepositoryApiOrders(Orders)
counteragents_crud = RepositoryApiCounteragents(Counteragents)
