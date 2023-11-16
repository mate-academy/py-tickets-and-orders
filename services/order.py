from typing import Optional
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.query import QuerySet
from db.models import Ticket, Order, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[datetime] = None
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        movie_session = MovieSession.objects.get(
            pk=ticket.pop("movie_session")
        )
        Ticket.objects.create(
            **ticket, movie_session=movie_session, order=order
        )


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
