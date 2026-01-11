from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Ticket, Order, User
from django.db import transaction


def get_user(username: str) -> User:
    return get_user_model().objects.get(username=username)


def create_order(tickets: list, username: str, date: str = None) -> None:
    user = get_user(username)
    with transaction.atomic():
        order = Order.objects.create(
            user=user
        )

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
                order=order
            )


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user=get_user(username))

    return orders.values("created_at")
