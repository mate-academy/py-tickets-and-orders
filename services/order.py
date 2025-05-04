from datetime import datetime

from typing import Any

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
        tickets: list[dict[str, Any]],
        username: str,
        date: datetime = None
) -> Order:
    with transaction.atomic():
        order = Order.objects.create(
            user=User.objects.get(username=username),
        )
        if date:
            order.created_at = date

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"])
            ticket = Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )
        return ticket


def get_orders(
        username: str = None
) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user=User.objects.get(username=username))

    return queryset
