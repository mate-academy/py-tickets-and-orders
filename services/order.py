from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


User = get_user_model()


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None
                 ) -> None:
    user = User.objects.get(username=username)
    kwargs = {"user": user}
    if date is not None:
        kwargs["created_at"] = date
    order = Order.objects.create(**kwargs)

    for ticket in tickets:
        ticket["movie_session"] = MovieSession.objects.get(
            id=ticket["movie_session"]
        )
        Ticket.objects.create(**ticket, order=order)


def get_orders(username: str = None) -> QuerySet[Order]:
    if username is not None:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
