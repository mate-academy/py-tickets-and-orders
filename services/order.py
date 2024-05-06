from __future__ import annotations

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> None:
    order = Order.objects.create(user=User.objects.get(username=username))

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(movie_session_id=ticket["movie_session"],
                              order=order, row=ticket["row"],
                              seat=ticket["seat"])


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user=User.objects.get(username=username))

    return Order.objects.all()
