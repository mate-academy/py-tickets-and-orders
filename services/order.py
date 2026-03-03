import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import User, Order, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.datetime = None
) -> Order:
    user = User.objects.get(username=username)

    if not date:
        date = datetime.datetime(2020, 11, 10, 14, 40)

    with transaction.atomic():
        order = Order.objects.create(user=user)
        order.created_at = date
        order.save()

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=ticket["row"], seat=ticket["seat"]
            )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    order = Order.objects.all()

    if username:
        order = order.filter(user=User.objects.get(username=username))

    return order
