from typing import Optional

from django.contrib.auth import get_user_model

from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order


def create_order(
        tickets: list,
        username: str,
        date: Optional[str] = None
) -> None:
    with transaction.atomic():
        new_order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )

        if date:
            new_order.created_at = date
            new_order.save()

        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
                order=new_order
            )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
