from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list[dict[str, Any]],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )
        if date:
            order.created_at = date

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            row = ticket["row"]
            seat = ticket["seat"]
            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=row,
                seat=seat
            )
        order.save()
    return order


def get_orders(
        username: str = None
) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(
            user=get_user_model().objects.get(
                username=username
            )
        )
    return Order.objects.all().order_by("-created_at")
