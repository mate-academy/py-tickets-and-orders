from datetime import datetime

from django.contrib.auth.models import User
from django.db import transaction
from django.utils.timezone import make_aware

from db.models import Order, Ticket


def create_order(tickets: list[dict], username: str, date: str = None) -> Order:
    """
    Створює замовлення для користувача з переданими квитками.

    Args:
        tickets (list[dict]): Список квитків з ключами "row", "seat", "movie_session".
        username (str): Ім'я користувача, який створює замовлення.
        date (str, optional): Дата створення замовлення у форматі "YYYY-MM-DD HH:MM".

    Returns:
        Order: Створене замовлення.

    Raises:
        ValueError: Якщо користувач або кінопоказ не існують.
    """
    user = User.objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user)

        if date:
            order.created_at = make_aware(datetime.strptime(date, "%Y-%m-%d %H:%M"))
            order.save()

        ticket_objects = [
            Ticket(order=order, row=t["row"], seat=t["seat"], movie_session_id=t["movie_session"])
            for t in tickets
        ]
        Ticket.objects.bulk_create(ticket_objects)

    return order


def get_orders(username=None):
    try:
        if username != None:
            return Order.objects.filter(user__username=username)
        return Order.objects.all()
    except Order.DoesNotExist:
        raise "Some mistake"
