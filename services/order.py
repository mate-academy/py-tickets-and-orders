from django.db import transaction
from django.db.models import QuerySet
from datetime import datetime
from typing import Optional

from db.models import Order, User, Ticket


def create_order(tickets: list[dict],
                 username: str,
                 date: Optional[datetime]) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
        order.save()
        for ticket in tickets:
            Ticket.objects.create(order=order,
                                  seat=ticket["seat"],
                                  row=ticket["row"],
                                  movie_session=ticket["movie_session"],)


def get_orders(username: Optional[str]) -> QuerySet:
    if username:
        return Order.objects.filter(user=User.objects.get(username=username))
    return Order.objects.all()
