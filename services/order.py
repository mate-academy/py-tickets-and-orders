from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Ticket, Order


def create_order(
    tickets: list[dict],
    username: str,
    date: Optional[str] = None,
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        new_order = Order.objects.create(
            user=user
        )

        if date:
            new_order.created_at = date
            new_order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
                order=new_order
            )


def get_orders(username: Optional[str] = None) -> None:
    queryset = Order.objects.all().select_related("user")
    if username:
        user = get_user_model().objects.get(username=username)
        queryset = queryset.filter(user_id=user.id)
    return queryset
