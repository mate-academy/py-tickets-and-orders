from django.db import transaction
from django.contrib.auth import get_user_model
from datetime import datetime
from typing import Optional
from django.db.models import QuerySet
from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: datetime | None = None
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        movie_session = MovieSession.objects.get(
            id=ticket["movie_session"]
        )
        ticket = Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )
        ticket.save()


def get_orders(username: Optional[str] = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        user = get_user_model().objects.get(username=username)
        orders = orders.filter(user=user)
    return orders
