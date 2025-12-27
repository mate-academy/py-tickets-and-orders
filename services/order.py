from datetime import datetime
from typing import Dict

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


@transaction.atomic
def create_order(
        tickets: list[Dict],
        username: str,
        date: datetime = None
) -> None:
    order = Order.objects.create(
        user=User.objects.get(username=username)
    )
    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
            order=order
        )


def get_orders(
        username: str = None
) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        user = User.objects.get(username=username)
        return orders.filter(user_id=user.id)
    return orders
