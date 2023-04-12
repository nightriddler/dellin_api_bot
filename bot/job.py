import logging

from db.base import counteragents_crud, order_crud


async def update_db(session):
    """
    Обновляет или создает данные в БД.
    """
    logging.info("Запрос к API для наполнения данными БД заказов.")
    await order_crud.create_or_update(session)
    logging.info("Данные в БД по заказам обновлены.")

    logging.info("Запрос к API для наполнения данными БД контрагента.")
    await counteragents_crud.create_or_update(session)
    logging.info("Данные в БД по контрагенту обновлены.")
