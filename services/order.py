from typing import Any, List

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import MovieSession, Order, Ticket


def create_order(
        tickets: List[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )


def get_orders(username: str = None) -> Any:
    queryset = Order.objects.all().order_by("-user")

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
