from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import User, Order, Ticket, MovieSession


def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None
                 ) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        kwargs = {"user": user}
        if date is not None:
            kwargs["created_at"] = date
        order = Order.objects.create(**kwargs)

        for ticket in tickets:
            ticket["movie_session"] = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            Ticket.objects.create(**ticket, order=order)


def get_orders(username: str = None) -> QuerySet:
    if username is not None:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
