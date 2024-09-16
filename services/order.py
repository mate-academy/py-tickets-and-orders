from django.contrib.auth import get_user_model
from django.db import transaction
from typing import List

from db.models import Ticket, Order


def create_order(
        tickets: List[dict],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user, created_at=date)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )
    return order


def get_orders(username: str = None) -> None:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
