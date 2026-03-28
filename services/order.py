from datetime import datetime
from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Ticket, Order, MovieSession


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: Optional[datetime] = None
) -> None:
    user = get_user_model().objects.filter(username=username).first()
    order = Order.objects.create(user=user)

    if date:
        Order.objects.filter(id=order.id).update(created_at=date)

    for ticket in tickets:
        movie_session = MovieSession.objects.filter(
            id=ticket["movie_session"]
        ).first()
        Ticket.objects.create(
            movie_session=movie_session,
            row=ticket["row"],
            seat=ticket["seat"],
            order=order
        )


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:

    if not username:
        return Order.objects.all()

    return Order.objects.filter(user__username=username)
