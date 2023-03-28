from datetime import datetime
from django.db import transaction
from django.db.models import QuerySet
from typing import Optional

from db.models import Order, Ticket, User


def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> None:
    with transaction.atomic():
        order = Order(user=User.objects.get(username=username))
        order.save()
        if date is not None:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: Optional[str] = None) -> QuerySet:
    queryset = Order.objects.all()
    if username is not None:
        return queryset.filter(user__username=username)
    return queryset
