from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Ticket, Order


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        new_order = Order.objects.create(user=user)
        if date:
            new_order.created_at = date
        new_order.save()
        for ticket in tickets:
            Ticket.objects.create(
                order=new_order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"]
            )


def get_orders(username: str = None) -> Order.objects:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
