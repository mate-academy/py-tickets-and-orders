from datetime import datetime

from django.db import transaction

import init_django_orm  # noqa: F401
from db.models import Ticket, Order, User, MovieSession


@transaction.atomic
def create_order(tickets: dict,
                 username: str = None,
                 date: datetime = None, order: Order = None) -> Order:
    user = User.objects.get(username=username)
    new_order = Order.objects.create(user=user)
    if date:
        new_order.created_at = date
        new_order.save()
    Ticket.objects.bulk_create(
        [Ticket(
            order=new_order,
            movie_session=MovieSession.objects.get(
                id=ticket["movie_session"]
            ),
            row=ticket["row"],
            seat=ticket["seat"]
        ) for ticket in tickets]
    )
    return order


def get_orders(username: str = None) -> Order:
    order = Order.objects.all()
    if username:
        order = Order.objects.filter(user__username=username)
    return order
