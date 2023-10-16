from datetime import datetime
from typing import List, Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: List[Ticket],
        username: str,
        date: Optional[datetime] = None
) -> None:
    with transaction.atomic():
        user_to_create = get_user_model().objects.get(username=username)
        order_queryset = Order.objects.create(user=user_to_create)

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


def get_orders(username: Optional[str] = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
