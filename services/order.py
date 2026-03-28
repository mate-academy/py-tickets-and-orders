from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date

        for ticket in tickets:
            ticket["movie_session"] = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            Ticket.objects.create(**ticket, order=order)

        order.save()
        return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        user = get_user_model().objects.get(username=username)
        queryset = queryset.filter(user=user)

    return queryset
