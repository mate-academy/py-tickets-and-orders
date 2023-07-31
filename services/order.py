from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from typing import Optional

from db.models import Order, Ticket


def create_order(
    tickets: list[dict[str]],
    username: str,
    date: Optional[str] = None
) -> Order:

    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        new_order = Order.objects.create(user=user)

        if date:
            new_order.created_at = date
            new_order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=new_order,
                row=ticket.get("row"),
                seat=ticket.get("seat"),
                movie_session_id=ticket.get("movie_session"),
            )

        return new_order


def get_orders(username: Optional[str] = None) -> QuerySet:
    orders_queryset = Order.objects.all()

    if username:
        orders_queryset = orders_queryset.filter(user__username=username)

    return orders_queryset
