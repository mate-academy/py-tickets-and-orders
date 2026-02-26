from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
        tickets: list,
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))

        if date:
            date_time = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.created_at = date_time
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    pk=ticket["movie_session"]
                ),
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
