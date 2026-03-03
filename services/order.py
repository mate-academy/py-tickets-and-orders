from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Ticket, Order, MovieSession


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: datetime = None,
) -> None:

    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )

    for ticket in tickets:
        if date:
            order.created_at = date
            order.save()

        movie_session = MovieSession.objects.get(id=ticket["movie_session"])
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(
            user=get_user_model().objects.get(username=username)
        )

    return Order.objects.all()
