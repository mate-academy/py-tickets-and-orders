from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User
from datetime import datetime


def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[datetime] = None
) -> Order:
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))

        if date is not None:
            order.created_at = date

        order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )

        return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    orders = Order.objects.all()

    if username is not None:
        orders = orders.filter(user=User.objects.get(username=username))

    return orders
