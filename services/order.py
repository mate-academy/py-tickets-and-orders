from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    user = User.objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            ticket["order"] = order
            ticket["movie_session"] = (
                MovieSession.objects.get(id=ticket["movie_session"])
            )
            Ticket.objects.create(**ticket)


def get_orders(
        username: str = None
) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
