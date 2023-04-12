def get_order_count_in_menu(all_counts, count_on_page):
    """
    Количество страниц необходимое для пролистывания всех заказов.
    Используется в меню карусели.
    """
    skip = all_counts // count_on_page
    if all_counts % count_on_page != 0:
        skip += 1
    return skip


def clear_duplicate(orders):
    """
    Убирает повторяющиеся статусы в заказах.
    """
    without_duplicate = []
    check = set()
    for status in orders:
        if status.get("stateName") not in check:
            without_duplicate.append(status)
            check.add(status.get("stateName"))
    return without_duplicate
