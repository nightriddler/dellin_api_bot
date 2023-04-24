from contextlib import suppress
from json import JSONDecodeError

import api
from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import CallbackQuery, Message
from callback import OrdersCallbackData
from contains import COUNT_ORDER_IN_PAGE
from db.base import counteragents_crud, order_crud
from keyboards import get_keyboadrs_start, get_keyboard_cancel, get_orders_keyboard
from magic_filter import F
from middlewares import ChatIdPermissionMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from templates import render_template
from utils import clear_duplicate, get_order_count_in_menu

router = Router()
router.callback_query.middleware(ChatIdPermissionMiddleware())
router.message.middleware(ChatIdPermissionMiddleware())


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Команда /start."""
    with suppress(TelegramBadRequest):
        await message.answer(text="Выберите:", reply_markup=get_keyboadrs_start())


@router.callback_query(Text("cancel"))
async def cmd_cancel(callback: CallbackQuery):
    """Команда /cancel."""
    await callback.message.edit_text(
        text="Выберите:", reply_markup=get_keyboadrs_start()
    )


@router.callback_query(Text("client"))
async def about(callback: CallbackQuery, session: AsyncSession):
    """Кнопка получения информации о контрагенте."""
    response = await counteragents_crud.get_or_create(session)
    response = response.data
    for counteragent in response.get("data").get("counteragents"):
        if counteragent.get("isCurrent"):
            curr_cont = counteragent
    prepare_answer = render_template("contact.j2", {"counteragent": curr_cont})
    await callback.message.edit_text(prepare_answer, reply_markup=get_keyboard_cancel())


@router.callback_query(OrdersCallbackData.filter(F.status == "all"))
async def all_orders(callback: CallbackQuery, session: AsyncSession):
    """Стартовая кнопка для получения информации о заказах."""
    response = await order_crud.get_or_create(session)
    response = response.data

    orders = response.get("orders")[:COUNT_ORDER_IN_PAGE]
    count_orders = len(list(response.get("orders")))
    menu_count_orders = get_order_count_in_menu(count_orders, COUNT_ORDER_IN_PAGE)
    orders_id = [order["orderId"] for order in orders]

    prepare_answer = render_template("all_orders.j2", {"orders": orders})
    await callback.message.edit_text(
        prepare_answer,
        reply_markup=get_orders_keyboard(
            current_orders_index=0,
            orders_count=menu_count_orders,
            orders=orders_id,
        ),
    )


@router.callback_query(OrdersCallbackData.filter(F.status == "page"))
async def index_orders(
    callback: CallbackQuery, callback_data: OrdersCallbackData, session: AsyncSession
):
    """Кнопка в карусели для получения информации о заказах."""
    index = callback_data.index

    response = await order_crud.get_or_create(session)
    response = response.data

    start = index * COUNT_ORDER_IN_PAGE
    finish = index * COUNT_ORDER_IN_PAGE + COUNT_ORDER_IN_PAGE
    orders = response.get("orders")[start:finish]

    count_orders = len(list(response.get("orders")))
    menu_count_orders = get_order_count_in_menu(count_orders, COUNT_ORDER_IN_PAGE)
    orders_id = [order.get("orderId") for order in orders]

    prepare_answer = render_template("all_orders.j2", {"orders": orders})
    await callback.message.edit_text(
        prepare_answer,
        reply_markup=get_orders_keyboard(
            current_orders_index=index,
            orders_count=menu_count_orders,
            orders=orders_id,
        ),
    )


@router.callback_query(OrdersCallbackData.filter(F.status == "single"))
async def index_orders(callback: CallbackQuery, callback_data: OrdersCallbackData):
    """Кнопка получения информации об изменении дат в статусах заказа."""
    order = callback_data.order

    try:
        response = api.dl.get_order_history(order)
        status_order = response.get("data").get("statusHistory").get(order)
        clear_status = clear_duplicate(status_order)
        prepare_answer = render_template(
            "order_history.j2", {"status_order": clear_status}
        )
    except AttributeError:
        prepare_answer = "История перемещения отсутствует."
    except JSONDecodeError:
        prepare_answer = "Сервис временно недоступен."

    await callback.answer(text=prepare_answer, show_alert=True)
