from typing import Optional
from django.db.models import QuerySet
from django.db import transaction
from django.contrib.auth import get_user_model
from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.filter(username=username).get()
        order = Order.objects.create(
            user=user
        )
        if date:
            order.created_at = date
        order.save()
        [Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        ) for ticket in tickets]


def get_orders(username: Optional[str] = None) -> QuerySet:
    if username is not None:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
