from datetime import datetime
from typing import Dict
from typing import Optional

from db.models import Ticket, Order, User
from django.db import transaction
from django.db.models import QuerySet


def create_order(
        tickets: list[Dict],
        username: str,
        date: Optional[datetime] = None
) -> None:
    with transaction.atomic():
        new_order = Order.objects.create(
            user=User.objects.get(username__exact=username)
        )
        if date:
            new_order.created_at = date
            new_order.save()
        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=new_order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(
        username: Optional[str] = None
) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
