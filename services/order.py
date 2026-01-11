from django.db import transaction
from django.db.models import QuerySet
from typing import Optional

from db.models import Ticket, Order, User, MovieSession


def create_order(
    tickets: list, username: str, date: Optional[str] = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        Ticket.objects.bulk_create(
            [
                Ticket(
                    row=ticket["row"],
                    seat=ticket["seat"],
                    movie_session=MovieSession.objects.get(
                        id=ticket["movie_session"]
                    ),
                    order=order,
                )
                for ticket in tickets
            ]
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
