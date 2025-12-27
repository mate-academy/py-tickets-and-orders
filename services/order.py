from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from typing import Optional
from datetime import datetime
from db.models import Order, Ticket, MovieSession
from django.db import transaction


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[datetime] = None
) -> Order:

    user = get_user_model().objects.get(username=username)

    if date:
        order = Order.objects.create(user=user)
        order.created_at = date
        order.save(update_fields=["created_at"])
    else:
        order = Order.objects.create(user=user)

    for ticket in tickets:
        movie_session = MovieSession.objects.get(
            id=ticket["movie_session"]
        )
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        orders = Order.objects.filter(user__username=username)
    else:
        orders = Order.objects.all()

    return orders
