import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None,
) -> Order:
    with (transaction.atomic()):
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = datetime.datetime.strptime(
                date, "%Y-%m-%d %H:%M"
            )
        order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                movie_session=MovieSession.objects.get(
                    pk=ticket["movie_session"]
                ),
                row=ticket["row"],
                seat=ticket["seat"]
            )

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user=User.objects.get(username=username))
    return Order.objects.all()
