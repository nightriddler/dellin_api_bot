from typing import Optional

from aiogram.filters.callback_data import CallbackData


class OrdersCallbackData(CallbackData, prefix="order"):
    status: str
    order: Optional[str]
    index: Optional[int]
