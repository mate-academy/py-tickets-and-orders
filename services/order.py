from typing import Optional

from django.db import transaction
from db.models import Order, Ticket, User
from django.db.models import QuerySet


def create_order(
        tickets: dict,
        username: str,
        date: Optional[str] = None
) -> None:
    with transaction.atomic():
        new_order = Order.objects.create(
            user=User.objects.get(
                username=username
            )
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


def get_orders(
        username: Optional[str] = None
) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
