from datetime import datetime
from typing import Optional

from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from db.models import Order, User, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict[str, int]],
        username: str,
        date: Optional[datetime.date] = None
) -> Order:
    user = get_object_or_404(User, username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date

    for ticket in tickets:
        Ticket.objects.create(
            row=ticket.get("row"),
            seat=ticket.get("seat"),
            movie_session=get_object_or_404(
                MovieSession,
                id=ticket.get("movie_session")
            ),
            order=order
        )

    order.save()

    return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
