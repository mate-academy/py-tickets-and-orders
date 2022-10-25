from django.db import transaction
from django.db.models import QuerySet

from db.models import User, Order, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:

    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            movie_session = ticket["movie_session"]

            Ticket.objects.create(
                movie_session=MovieSession.objects.get(id=movie_session),
                row=ticket["row"],
                seat=ticket["seat"],
                order=order,
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
