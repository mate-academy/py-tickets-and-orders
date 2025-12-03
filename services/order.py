from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import (Order, Ticket, MovieSession, User)


def get_user(username: str) -> User:
    user = get_user_model().objects.get(username=username)
    return user


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> None:
    order = Order.objects.create(
        user=get_user(username)
    )
    if date:
        order.created_at = date

    order.save()

    for ticket in tickets:
        movie_session = MovieSession.objects.get(pk=ticket["movie_session"])
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=movie_session,
            order=order
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    if not username:
        return Order.objects.all()
    else:
        user = get_user(username)
        return Order.objects.filter(user=user)
