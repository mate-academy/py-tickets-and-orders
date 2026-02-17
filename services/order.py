from datetime import datetime
from typing import Dict, List, Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket, MovieSession


def create_order(
    tickets: List[Dict],
    username: str,
    date: Optional[datetime] = None,
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        if date is not None:
            order.created_at = date
            order.save()

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket.pop("movie_session"),
            )
            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                **ticket,
            )

        return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    if username is not None:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
