from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )
        if date:
            order.created_at = date
            order.save()
        Ticket.objects.bulk_create(
            [
                Ticket(
                    order=order,
                    row=ticket["row"],
                    seat=ticket["seat"],
                    movie_session=MovieSession.objects.get(
                        id=ticket["movie_session"])
                )
                for ticket in tickets
            ]
        )


def get_orders(username: str = None) -> Order | QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
