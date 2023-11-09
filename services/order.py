from datetime import datetime
from typing import List

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order


def create_order(
    tickets: List[dict],
    username: str,
    date: datetime = None
) -> None:
    user = get_user_model().objects.get(username=username)
    with transaction.atomic():
        order = Order(user=user)
        order.save()

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            ticket = Ticket(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
            ticket.save()


def get_orders(username: str = None) -> QuerySet:
    orders_queryset = Order.objects.all()

    if username:
        orders_queryset = orders_queryset.filter(user__username=username)

    return orders_queryset
