from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(tickets: dict[str: int],
                 username: str,
                 date: str | datetime | None = None) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]),
                row=ticket["row"],
                seat=ticket["seat"],
                order=order,
                )


def get_orders(username: str | None = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if get_user_model().objects.filter(username=username).exists():
        orders = orders.filter(user__username=username)
    return orders
