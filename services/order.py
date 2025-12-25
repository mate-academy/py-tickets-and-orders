from datetime import datetime
from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


def create_order(
        tickets: list[dict], username: str, date: Optional[str] = None
) -> None:
    with transaction.atomic():
        order = Order.objects.create(
            user=User.objects.get(username=username)
        )

        if date is not None:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
                order=order
            )


def get_orders(username: Optional[str] = None) -> QuerySet:
    queryset = Order.objects.all()

    if username is not None:
        queryset = queryset.filter(user__username=username)

    return queryset
