from typing import List
from datetime import datetime

from db.models import User
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, MovieSession, Ticket


def create_order(
        tickets: List[dict],
        username: str,
        date: datetime = None
) -> None:
    with transaction.atomic():
        user, _ = User.objects.get_or_create(username=username)

        order = Order.objects.create(user=user, created_at=date)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            row = ticket["row"]
            seat = ticket["seat"]
            movie_session_id = ticket["movie_session"]

            movie_session = MovieSession.objects.get(id=movie_session_id)
            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=row,
                seat=seat)


def get_orders(username: str = None) -> QuerySet[Order]:
    if username is not None:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
