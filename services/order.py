from datetime import datetime
from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from db.models import Order, MovieSession, Ticket


User = get_user_model()


def create_order(
    tickets: list[dict[str, int]],
    username: str,
    date: Optional[datetime] = None
) -> None:
    user = get_object_or_404(User, username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            movie_session = get_object_or_404(
                MovieSession,
                id=ticket["movie_session"]
            )

            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
