from typing import List

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: List[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        order = Order.objects.create(
            user_id=get_user_model().objects.get(username=username).id
        )

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            row, seat, movie_session_id = ticket.values()
            Ticket.objects.create(
                movie_session_id=movie_session_id,
                order_id=order.id,
                row=row,
                seat=seat
            )


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(
            user_id=get_user_model().objects.get(username=username).id
        )

    return orders
