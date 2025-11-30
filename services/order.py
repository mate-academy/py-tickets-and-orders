from __future__ import annotations

import datetime as dt
from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


UserModel = get_user_model()


@transaction.atomic
def create_order(
    tickets: list[dict[str, int]],
    username: str,
    date: Optional[str] = None,
) -> Order:
    user = UserModel.objects.get(username=username)

    if date:
        created_at = dt.datetime.fromisoformat(date)
        order = Order.objects.create(
            user=user,
            created_at=created_at
        )
    else:
        order = Order.objects.create(user=user)

    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
