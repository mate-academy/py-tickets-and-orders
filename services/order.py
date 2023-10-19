import datetime
from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(
    tickets: list[dict],
    username: str,
    date: Optional[datetime.datetime] = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        new_order = Order.objects.create(user=user)

        if date:
            new_order.created_at = date
            new_order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                order=new_order,
                row=ticket["row"],
                seat=ticket["seat"]
            )

        return new_order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    orders = Order.objects.all()

    if username:
        return Order.objects.filter(user__username=username)
    return orders
