def get_order_count_in_menu(all_counts, count_on_page):
    """
    Количество страниц необходимое для пролистывания всех заказов.
    Используется в меню карусели.
    """
    skip = all_counts // count_on_page
    if all_counts % count_on_page != 0:
        skip += 1
    return skip


def clear_duplicate_status(statuses):
    """
    Убирает повторяющиеся статусы в заказах.
    """
    without_duplicate_statuses = []
    unique_status = set()
    for status in statuses:
        if status.get("detailedStatusRus"):
            if status["detailedStatusRus"] not in unique_status:
                without_duplicate_statuses.append(status)
                unique_status.add(status["detailedStatusRus"])
        else:
            if status["stateName"] not in unique_status:
                without_duplicate_statuses.append(status)
                unique_status.add(status["stateName"])
    return without_duplicate_statuses
