from django.db import transaction
from django.db.models import QuerySet

import init_django_orm  # noqa: F401

from db.models import Order, Ticket, User, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        new_order = Order.objects.create(user=user)
        if date:
            new_order.created_at = date
            new_order.save()
        for ticket in tickets:
            session = MovieSession.objects.get(id=ticket["movie_session"])
            Ticket.objects.create(
                movie_session=session,
                order=new_order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = Order.objects.filter(user__username=username)
    return orders
