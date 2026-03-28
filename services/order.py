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
        user = get_user_model().objects.get(username=username)
        order_queryset = Order.objects.create(user=user)

        if date:
            order_queryset.created_at = date

        order_queryset.save()

        for ticket in tickets:
            movie_session_id_of_ticket = ticket["movie_session"]
            Ticket.objects.create(
                order_id=order_queryset.id,
                movie_session_id=movie_session_id_of_ticket,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: Optional[str] = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
