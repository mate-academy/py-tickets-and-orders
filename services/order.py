from datetime import datetime
from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[datetime] = None
) -> Order:

    with transaction.atomic():
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise ValueError(f"User {username} does not exist")

        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            movie_session_id = ticket.get("movie_session")
            movie_session = MovieSession.objects.get(id=movie_session_id)
            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=ticket["row"],
                seat=ticket["seat"],
            )
        return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
