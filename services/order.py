from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession
from django.contrib.auth import get_user_model


@transaction.atomic()
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> Order:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )
    if date:
        order.created_at = date
    tickets_objects = [
        Ticket(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=MovieSession.objects.get(
                id=ticket["movie_session"]
            )
        ) for ticket in tickets
    ]
    Ticket.objects.bulk_create(tickets_objects)
    order.save()
    return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    order = Order.objects.all()
    if username:
        order = order.filter(user__username=username)
    return order
