from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order


def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> None:
    with transaction.atomic():

        user = get_user_model().objects.get(username=username)

        order = Order.objects.create(user=user)
        if date is not None:
            order.created_at = date
        order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket.get("movie_session"),
                order=order,
                row=ticket.get("row"),
                seat=ticket.get("seat")
            )


def get_orders(username: Optional[str] = None) -> QuerySet:
    orders = Order.objects.all()

    if username is not None:
        orders = orders.filter(user__username=username)

    return orders
