from datetime import datetime
from typing import Dict

from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, User


def create_order(
        tickets: list[Dict],
        username: str,
        date: datetime = None
) -> None:
    with transaction.atomic():
        new_order = Order.objects.create(
            user=User.objects.get(username__exact=username
                                  )
        )
        if date:
            new_order.created_at = datetime.strptime(
                date, "%Y-%m-%d %H:%M"
            )
            new_order.save()
        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=new_order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(
        username: str = None
) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
