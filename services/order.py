from datetime import datetime
from typing import Union

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket

from django.db import transaction


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: Union[str, datetime] = None,
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        Order.objects.filter(id=order.id).update(created_at=date)
    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username is None:
        return orders
    return orders.filter(user__username=username)
