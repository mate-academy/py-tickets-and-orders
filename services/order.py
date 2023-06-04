from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:
    with transaction.atomic():

        my_order = Order.objects.create(
            user=User.objects.get(username=username)
        )

        if date:
            my_order.created_at = date
            my_order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=my_order,
                movie_session_id=ticket.get("movie_session"),
                seat=ticket.get("seat"),
                row=ticket.get("row")
            )

    return my_order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = Order.objects.filter(
            user=User.objects.get(username=username)
        )

    return queryset
