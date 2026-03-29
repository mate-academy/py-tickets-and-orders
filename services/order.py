from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list,
        username: str,
        date: Optional[str] = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
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
    return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    order = Order.objects.all()
    if username is not None:
        order = order.filter(
            user=get_user_model().objects.get(username=username)
        )
    return order
