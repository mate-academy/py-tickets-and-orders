from typing import Optional

from django.db.models import QuerySet
from django.db import transaction
from db.models import Order, Ticket, MovieSession
from django.contrib.auth import get_user_model


@transaction.atomic()
def create_order(
        tickets: list,
        username: str,
        date: Optional[str] = None,
) -> None:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )
    if date:
        order.created_at = date
    order.save()

    Ticket.objects.bulk_create(
        [
            Ticket(
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            ) for ticket in tickets
        ]
    )


def get_orders(username: Optional[str] = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
