import datetime
from typing import List, Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: List[Ticket],
        username: str,
        date: datetime = None
) -> None:

    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user_id=user.id)
        if date:
            order.created_at = date
        if tickets:
            for ticket in tickets:
                Ticket.objects.get_or_create(
                    movie_session_id=ticket["movie_session"],
                    order=order,
                    row=ticket["row"],
                    seat=ticket["seat"]
                )
        if date:
            order.created_at = date
        order.save()


def get_orders(username: Optional[str] = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
