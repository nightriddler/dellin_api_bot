from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callback import OrdersCallbackData


def get_keyboadrs_start() -> InlineKeyboardBuilder:
    """Стартовая клавиатура."""
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Информация о заказах", callback_data=OrdersCallbackData(status="all")
    )
    builder.button(text="Информация о клиенте", callback_data="client")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_orders_keyboard(
    current_orders_index: int,
    orders_count: int,
    orders: list[int] = None,
) -> InlineKeyboardMarkup:
    """Клавиатура для заказов."""
    builder = InlineKeyboardBuilder()

    if orders:
        for order in orders:
            builder.button(
                text="История перемещения",
                callback_data=OrdersCallbackData(
                    status="single", order=order, index=current_orders_index
                ),
            )

    prev_index = current_orders_index - 1
    if prev_index < 0:
        prev_index = orders_count - 1
    next_index = current_orders_index + 1
    if next_index > orders_count - 1:
        next_index = 0

    builder.button(
        text="<", callback_data=OrdersCallbackData(status="page", index=prev_index)
    )
    builder.button(text=f"{current_orders_index + 1}/{orders_count}", callback_data=" ")
    builder.button(
        text=">", callback_data=OrdersCallbackData(status="page", index=next_index)
    )
    builder.button(text="Меню", callback_data="cancel")
    builder.adjust(len(orders), 3)
    return builder.as_markup(resize_keyboard=True)


def get_keyboard_cancel() -> InlineKeyboardMarkup:
    """Клавиатура возврата к меню."""
    builder = InlineKeyboardBuilder()
    builder.button(text="< Назад", callback_data="cancel")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_keyboard_cancel_from_status(
    current_orders_index: int,
) -> InlineKeyboardMarkup:
    """Клавиатура возврата к меню."""
    builder = InlineKeyboardBuilder()
    builder.button(
        text="< Назад",
        callback_data=OrdersCallbackData(status="page", index=current_orders_index),
    )
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
