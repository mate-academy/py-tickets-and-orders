from __future__ import annotations
from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, User


def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date

        for ticket_data in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket_data["movie_session"],
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )
        order.save()
        return order


def get_orders(username: Optional[str] = None) -> Order | QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
