from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:

    try:
        user = get_user_model().objects.get(username=username)
    except get_user_model().DoesNotExist:
        raise ValueError(f"User with username '{username}' does not exist")

    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    sessions = MovieSession.objects.in_bulk(
        [ticket["movie_session"] for ticket in tickets]
    )

    Ticket.objects.bulk_create(
        [
            Ticket(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=sessions.get(ticket["movie_session"])
            ) for ticket in tickets
        ]
    )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
