from datetime import datetime
from typing import List, Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: List[Ticket],
        username: str,
        date: Optional[datetime]
) -> None:
    with transaction.atomic():
        order_queryset = Order.objects.create(user__username=username)

        if date:
            order_queryset.created_at = date

        order_queryset.save()

        for ticket in tickets:
            Ticket.objects.create(
                order_id=order_queryset.id,
                movie_session_id=ticket.movie_session.id,
                row=ticket.row,
                seat=ticket.seat
            )


def get_orders(username: Optional[str] = None) -> Optional[QuerySet, Order]:
    if username:
        return Order.objects.filter(order__user__username=username)
    return Order.objects.all()
