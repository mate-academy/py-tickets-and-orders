from typing import Optional

from django.contrib.auth import get_user_model

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> None:
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


def get_orders(username: Optional[str] = None) -> QuerySet:
    orders_set = Order.objects.all()

    if username:
        orders_set = orders_set.filter(user__username=username)

    return orders_set
