import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list[dict[str, int]],
        username: str,
        date: datetime.datetime = None
) -> Order:
    with transaction.atomic():
        order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )
        if date:
            order.created_at = date
        order.save()
        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                row=ticket["row"],
                seat=ticket["seat"],
            ).save()
        return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
