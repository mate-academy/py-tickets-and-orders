from datetime import datetime
from typing import List, Dict

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: List[Dict],
        username: str,
        date: str | None = None,
) -> None:
    with (transaction.atomic()):
        order = Order.objects.create(
            user=get_user_model().objects.get(username=username),
        )
        if date:
            order.created_at = datetime.fromisoformat(date)
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )


def get_orders(username: str | None = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
