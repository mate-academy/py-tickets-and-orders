from typing import List

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.db.models.functions import datetime

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: List[dict],
        username: str,
        date: datetime = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            row = ticket["row"]
            seat = ticket["seat"]
            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=row,
                seat=seat
            )
        order.save()
        return order


def get_orders(username: str = None) -> QuerySet:
    order = Order.objects.all()
    if username is not None:
        order = order.filter(user__username=username)

    return order
