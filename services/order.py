from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket, MovieSession
from datetime import datetime
from django.db.models.query import QuerySet


def create_order(
        tickets: list[dict],
        username: str, date:
        datetime = None) -> Order:
    with transaction.atomic():
        user = get_user_model()
        user, _ = user.objects.get_or_create(username=username)

        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                order=order
            )
        return order


def get_orders(username: str = None) -> QuerySet[Order] | None:
    if username:
        user = get_user_model().objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
