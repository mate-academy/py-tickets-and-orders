import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.datetime = None,
) -> Order:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username),
    )
    if date:
        order.created_at = date
    Ticket.objects.bulk_create(
        [
            Ticket(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=MovieSession.objects.get(
                    pk=ticket["movie_session"]
                ),
                order=order
            )
            for ticket in tickets
        ]
    )
    order.save()
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
