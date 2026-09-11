from typing import List
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.query import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: List[Ticket],
        username: str,
        date: datetime = None) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(created_at=date, user=user)
    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        m_session = MovieSession.objects.get(
            id=ticket.get("movie_session")
        )
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=m_session,
            order=order
        )
    return order


def get_orders(username: str = "") -> QuerySet[Order]:
    if username:
        user = get_user_model().objects.get(username=username)
        orders = Order.objects.filter(user=user)
        return orders
    else:
        return Order.objects.all()
