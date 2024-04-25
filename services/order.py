from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order
from services.user import get_user_id_by_username


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        user_id = get_user_id_by_username(username)
        order = Order.objects.create(user_id=user_id)
        if date is not None:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order_id=order.id,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"]
            )


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()

    if username is not None:
        user_id = get_user_id_by_username(username)
        orders = orders.filter(user_id=user_id)

    return orders
