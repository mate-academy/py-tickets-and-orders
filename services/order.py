import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list[dict], username: str, date: datetime = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        this_order = Order.objects.create(user=user)

        if date:
            this_order.created_at = date
            this_order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                order=this_order,
                row=ticket["row"],
                seat=ticket["seat"]
            )

        return this_order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        user = get_user_model().objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
