from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, User


def create_order(
        tickets: list[dict],
        username: datetime,
        date: str = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
                order=order
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        user_id = User.objects.get(username=username).id
        return Order.objects.filter(user_id=user_id)

    return Order.objects.all()
