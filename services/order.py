from datetime import datetime as dt

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Ticket, Order


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = dt.strptime(date, "%Y-%m-%d %H:%M")
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
                order=order)


def get_orders(username: str = None) -> list[Order]:
    if username is not None:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
