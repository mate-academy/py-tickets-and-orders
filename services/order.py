from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
        tickets: list,
        username: str,
        date: str = None) -> None:
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))
        if date is not None:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                row=ticket["row"],
                seat=ticket["seat"],
                order=order
            )


def get_orders(username: str = None) -> QuerySet:
    if username is not None:
        return Order.objects.all().filter(user_id__username=username)
    return Order.objects.all()
