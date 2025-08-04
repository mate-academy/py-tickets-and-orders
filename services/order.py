from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list[dict[str, Any]],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        created_at = parse_datetime(date) if date else None
        order = Order.objects.create(user=user)
        if created_at:
            order.created_at = created_at
            order.save()

        Ticket.objects.bulk_create(
            [
                Ticket(
                    order=order,
                    movie_session=MovieSession.objects.get(
                        pk=ticket["movie_session"]
                    ),
                    row=ticket["row"],
                    seat=ticket["seat"]
                )
                for ticket in tickets
            ]
        )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.select_related("user").prefetch_related("tickets")
    return orders.filter(user__username=username) if username else orders
