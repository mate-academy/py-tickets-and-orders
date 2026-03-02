from datetime import datetime

from typing import Optional

from django.contrib.auth import get_user_model

from django.db import transaction

from django.db.models import QuerySet

from django.shortcuts import get_object_or_404

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[datetime] = None,
) -> Order:
    user = get_object_or_404(get_user_model(), username=username)
    order = Order.objects.create(
        user=user
    )

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            row=ticket.get("row"),
            seat=ticket.get("seat"),
            movie_session_id=ticket.get("movie_session"),
            order=order
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        user = get_object_or_404(get_user_model(), username=username)
        return Order.objects.filter(user=user)

    return Order.objects.all()
