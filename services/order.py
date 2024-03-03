from typing import Optional
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession

User = get_user_model()


def create_order(
        tickets: list, username: str, date: Optional[str] = None) -> None:
    user = User.objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(
            user=user, created_at=date)
        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]),
                order=order
            )


def get_orders(username: Optional[str] = None) -> "QuerySet[Order]":
    if username is not None:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    else:
        return Order.objects.all()
