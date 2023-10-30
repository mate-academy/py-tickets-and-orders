from datetime import datetime

from db.models import Order, Ticket

from django.contrib.auth import get_user_model
from django.db import transaction

from typing import List


@transaction.atomic
def create_order(
        tickets: List[dict],
        username: str,
        date: datetime = None
) -> None:

    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date is not None:
        order.created_at = date
        order.save()
    for new_ticket in tickets:
        Ticket.objects.create(
            order=order,
            row=new_ticket["row"],
            seat=new_ticket["seat"],
            movie_session_id=new_ticket["movie_session"]
        )


def get_orders(username: str = None) -> None:

    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
