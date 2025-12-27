from datetime import datetime
from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict[str, Any]],
        username: str,
        date: str = ""
) -> Order:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username),
    )
    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")

    order.save()

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
        )

    return order


def get_orders(username: str = "") -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
