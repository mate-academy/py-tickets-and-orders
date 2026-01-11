import datetime
from typing import Optional

from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import (
    Ticket,
    Order,
    MovieSession
)


def create_order(
    tickets: list[dict],
    username: str,
    date: Optional[datetime.datetime] = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(
            user=user
        )

        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    pk=ticket_data["movie_session"]
                ),
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )


def get_orders(
        username: Optional[str] = None
) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
