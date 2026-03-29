from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, User


def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> None:

    with transaction.atomic():

        order = Order.objects.create(user=User.objects.get(username=username))

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return User.objects.get(username=username).order_set.all()
    return Order.objects.all()
