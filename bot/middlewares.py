import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from contains import TELEGRAM_CHAT_ID
from sqlalchemy.ext.asyncio import async_sessionmaker


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)


class ChatIdPermissionMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.allowed_chat_id = TELEGRAM_CHAT_ID

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if data["event_from_user"].id in self.allowed_chat_id:
            return await handler(event, data)
        else:
            logging.warning(
                f"Попытка пользователя получить доступ {data['event_from_user']}"
            )
            await event.answer("Доступ закрыт, это частный бот.")
