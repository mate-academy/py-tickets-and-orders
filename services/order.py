from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

import init_django_orm  # noqa: F401

from db.models import Order, Ticket, User, MovieSession


@transaction.atomic()
def create_order(
        tickets: Optional[list[dict]],
        username: str,
        date: Optional[str] = None
) -> None:
    user = User.objects.get(username=username)
    new_order = Order.objects.create(user=user)

    if date:
        new_order.created_at = date
        new_order.save()

    for ticket in tickets:
        movie_session = MovieSession.objects.get(id=ticket["movie_session"])
        Ticket.objects.create(
            movie_session=movie_session,
            order=new_order,
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
